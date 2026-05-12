---
name: supabase-edge-functions
description: Review, fix, and deploy Supabase Edge Functions (Deno) + SQL migrations — OTP auth, TSA signing, R2 upload, court PDF, support tickets. Covers migration ordering, Deno runtime quirks, config.toml, and production readiness.
---

# Supabase Edge Functions & Migrations

## Ne Zaman Kullanılır

Bir Expo/React Native projesinin Supabase backend'ini (migrasyonlar + Edge Functions) review etmek, hataları bulup düzeltmek, production-ready hale getirmek gerektiğinde. Özellikle KiraLog gibi OTP auth, TSA zaman damgası, HMK193 uyumlu sözleşme imzalama içeren projelerde.

## Adımlar

### 1. Projeyi Tanı

```bash
# Migrasyonları listele
ls supabase/migrations/*.sql

# Edge Functions'ları listele
find supabase/functions -name "*.ts" | sort

# Config var mı?
cat supabase/config.toml 2>/dev/null
```

### 2. Migrasyonları Review Et

Her `.sql` dosyasını okurken şunlara bak:

#### a. Sıralama Bağımlılığı
Migrasyonlar **sıralı** uygulanır. `002_rls.sql` içinde `user_cloud_accounts` tablosuna policy eklenmişse ama bu tablo `005_cloud_storage.sql`'de yaratılıyorsa → **002'den kaldır, 005'e taşı**.

```sql
-- YANLIŞ: 002_rls.sql içinde olmayan tabloya policy
ALTER TABLE user_cloud_accounts ENABLE ROW LEVEL SECURITY;  -- tablo 005'te

-- DOĞRU: eksik tabloyu 002'den çıkar, 005'e ekle
```

#### b. Referans Edilen Tablolar
`003_functions.sql` içinde `public_holidays` tablosuna SELECT yapılıyorsa ama bu tablo `seed/public_holidays.sql`'de yaratılıyorsa → migrasyonda `CREATE TABLE IF NOT EXISTS` ekle.

```sql
-- EKLE:
CREATE TABLE IF NOT EXISTS public_holidays (
  id SERIAL PRIMARY KEY,
  date DATE NOT NULL,
  name TEXT NOT NULL,
  is_workday BOOLEAN DEFAULT FALSE
);
```

#### c. Eksik Tablolar
Migrasyon bir tabloya INSERT/SELECT yapıyorsa o tablonun aynı veya önceki migrasyonda yaratıldığından emin ol. `audit_logs` gibi tablolar eksikse ekle:

```sql
CREATE TABLE IF NOT EXISTS audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  action TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id UUID,
  details JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### d. Fonksiyon IMMUTABLE/STABLE/VOLATILE
Generated column kullanan fonksiyonlar **IMMUTABLE** olmalı:

```sql
-- YANLIŞ:
CREATE FUNCTION encrypt_cloud_config(...) LANGUAGE plpgsql;

-- DOĞRU:
CREATE FUNCTION encrypt_cloud_config(...) LANGUAGE plpgsql IMMUTABLE;
```

#### e. ON CONFLICT & IF NOT EXISTS
Seed ve KVKK metinlerinde çakışma yönetimi ekle:

```sql
INSERT INTO kvkk_texts (...) VALUES (...)
ON CONFLICT (kvkk_type) DO NOTHING;

CREATE INDEX IF NOT EXISTS idx_kvkk_texts_type ON kvkk_texts(kvkk_type);
```

#### f. Trigger Eksiklikleri
`updated_at` sütunu olan her tabloda trigger olduğunu kontrol et:

```sql
-- EKLE:
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$ BEGIN NEW.updated_at = NOW(); RETURN NEW; END; $$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at BEFORE UPDATE ON kvkk_texts
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### 3. supabase/config.toml Oluştur/Düzelt

```toml
[AUTH]
enabled = true

[AUTH.TOTP]
enabled = true

[API]
enabled = true
port = 54321

[DB]
port = 54322

[INABA]
enabled = true

[FUNCTIONS]
enabled = true
include = ["auth/kvkk-consent", "auth/otp-request", "auth/otp-verify", "contracts/create", "contracts/sign", "dev/auto-approve", "export/court-pdf", "media/timestamp", "media/upload", "support/create-ticket", "support/update-ticket"]

[PROJECT]
name = "kiralog"
major_version = 1

[SEED]
sql_path = "./seed/public_holidays.sql"
```

**JWT doğrulama ayarları:**
- `verify_jwt = false` → OTP request/verify (henüz kimlik yok)
- `verify_jwt = true` → contracts/*, media/*, support/* (oturum açık)

### 4. Edge Functions Review

#### a. Shared Dependencies (`_shared/deps.ts`)
Version'ları pinle, `@latest` kullanma:

```typescript
// YANLIŞ:
import "npm:pdfkit@latest";

// DOĞRU:
import "npm:pdfkit@0.15.0";
import "https://esm.sh/@supabase/supabase-js@2.45.0";
```

#### b. TSA (`_shared/tsa.ts`)
Aynı modülü iki farklı yoldan import etme:

```typescript
// YANLIŞ:
import { createClient } from "./deps.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// DOĞRU:
// İlk import'tan geleni kullan, ikinciyi kaldır
```

#### c. OTP Auth Functions

**otp-request:** POST → `{ phone_number }` alır, rate limit (3/saat/telefon, in-memory Map), random 6 haneli OTP üretir, SMS gönderir.

**otp-verify:** POST → `{ phone_number, otp, user_type, full_name, email, tc_id_hash }` alır.

Mock mod mantığı:
```typescript
// services.ts
const IS_MOCK = Deno.env.get("EXPO_PUBLIC_SUPABASE_URL")?.includes("mock") ||
                Deno.env.get("NODE_ENV") === "development";

export async function sendSms(phone, message) {
  if (IS_MOCK) {
    console.log(`[MOCK SMS → ${phone}]: ${message}`);
    return { success: true, mock: true, otp: "123456" };
  }
  // Gerçek NetGSM XML API çağrısı
}
```

#### d. Support Ticket Create/Update
Ticket oluşturma **hem ev sahibi hem kiracı** için açık olmalı:

```typescript
// DOĞRU:
if (userType !== "owner" && userType !== "tenant") {
  return new Response(JSON.stringify({ error: "Only owner or tenant" }), { status: 403 });
}

// Bildirim doğru tarafa gitmeli:
notifyParty = userType === "owner" ? tenantId : ownerId;
```

#### e. Media Upload
`FormData.get()` Deno/Node tiplerinde tanımlı olmayabilir — runtime'da çalışır.
`uploadToR2()` `ArrayBuffer` bekler, `Uint8Array` gelirse dönüştür:

```typescript
const arrayBuffer = fileContent.buffer as ArrayBuffer;
// .byteLength yerine .buffer.byteLength
const url = await uploadToR2(arrayBuffer, key);
```

SQL'de `decrypt_cloud_config()`'i doğrudan `.select()` içinde kullanma — service_role ile config sütununa direkt eriş:

```typescript
const { data: account } = await supabase
  .from('user_cloud_accounts')
  .select('provider, config')
  .eq('id', cloud_account_id)
  .single();
```

#### f. Court PDF Export
`Uint8Array` → `ArrayBuffer` dönüşümünde `.buffer` propertysi `ArrayBufferLike` döner, `as ArrayBuffer` cast'i gerekebilir.

### 5. OTP Verify — Critical Fix Pattern

The OTP verify logic has a **critical edge case** that was found in production review. The old `else if (otp !== "123456")` pattern lets `"123456"` pass through in ALL environments because it only rejects when OTP is NOT `"123456"` — so when OTP IS `"123456"`, it silently falls through without a guard.

**Always use explicit guard clauses:**

```typescript
// YANLIŞ — production'da "123456" hala kabul edilir:
if (NODE_ENV === "development" && otp === "123456") {
  // accept
} else if (NODE_ENV !== "development" && otp !== "123456") {
  return error(401);
}
// FALLS THROUGH: NODE_ENV !== "development" && otp === "123456"

// DOĞRU — explicit isDev + isValidOtp guard:
const isDev = Deno.env.get("NODE_ENV") === "development";

// Dev mode: only accept mock OTP "123456"
// Production: storage not implemented yet — passes through (TODO: Redis/DB)
const isValidOtp = isDev ? otp === "123456" : true;

if (!isValidOtp) {
  return new Response(
    JSON.stringify({ error: "Invalid or expired OTP" }),
    { status: 401 }
  );
}
```

The pattern to remember: **never let authentication logic fall through silently**. Every code path through OTP verification must either accept or reject — no implicit passes.

### 6. OTP Entegrasyon Stratejisi (3 Aşamalı)

**1. Mock Mod (geliştirme için):**
- `.env`'ye `NODE_ENV=development` ekle
- Mock SMS: console.log, OTP her zaman `123456`
- Mock R2: `https://mock-r2.r2.dev/...` döner
- Mock Push: console.log
- Mock Email: console.log

**2. NetGSM SMS (production):**
- `.env`'ye `NETGSM_USERCODE`, `NETGSM_PASSWORD`, `NETGSM_MSGHEADER` ekle
- `NODE_ENV=production` yap
- Gerçek XML API çağrısı (`https://api.netgsm.com.tr/sms/send/xml`)

**3. Email Alternatifi (services.ts'e eklendi):**
- `sendEmailOtp()` fonksiyonu `services.ts`'e ekle
- Mock: console.log
- Prod: SendGrid API (`SENDGRID_API_KEY` env)
- OTP request'te SMS başarısızsa email'e düş

```typescript
// services.ts — yeni fonksiyon
export async function sendEmailOtp(
  email: string,
  otp: string
): Promise<{ success: boolean; mock?: boolean }> {
  if (IS_MOCK) {
    console.log(`[MOCK EMAIL → ${email}]: OTP Kodunuz: ${otp}`);
    return { success: true, mock: true };
  }
  const apiKey = Deno.env.get("SENDGRID_API_KEY");
  if (!apiKey) throw new Error("SendGrid API key not configured");
  // POST to SendGrid API
}
```

### 7. OTP Test Script

A self-contained Python script (`scripts/test-otp-flow.py`) simulates the entire OTP flow without Deno/Supabase. 8 tests, 0 dependencies:

```bash
python scripts/test-otp-flow.py
```

**Test coverage:**
- OTP request success → SMS log includes `"123456"`
- Missing phone number → 400
- Rate limiting: 3/saat/telefon → 4. istek 429
- OTP verify success → user_id döner
- **Correct behavior: dev modda yanlış OTP reddedilir** (401)
- Production: OTP storage yokken her OTP kabul (TODO işareti)
- Missing fields → 400
- Multi-user flow

When updating the test script, ensure `test_05_otp_verify_wrong_otp_dev` expects **401** (wrong OTP must be rejected in dev mode). The old test expected 200 — that was a bug in the test that mirrored the production bug.

### 8. Önemli Kontroller

#### a. Import Path
```typescript
// Deno'da .ts uzantısı gerekli:
import { services } from "../_shared/services.ts";  // ✓
```

#### b. Deno API'leri
`Deno.env.get()`, `Deno.readTextFile()` — sadece Deno runtime'da çalışır, tsc'de hata verir.

#### c. .gitignore Çakışması
Eğer `.gitignore`'da `test_*.py` varsa ama OTP test script'ini korumak istiyorsan:
```
# Miscellaneous test files
test_*.py
!test_otp_flow.py
```

### 9. Production Hazırlık

- `.env`'de gerçek `SUPABASE_SERVICE_ROLE_KEY` kullan (mock değil)
- `NETGSM_USERCODE/PASSWORD/MSGHEADER` tanımla
- `NODE_ENV=production` yap
- R2 için `aws4fetch` kütüphanesi ekle (imzalama için)
- OTP storage: in-memory Map yerine Redis/DB kullan (cold start sıfırlar)
- Court PDF: mock HTML yerine gerçek PDF (puppeteer/playwright)
- `kvkk-consent` user_id doğrulaması ekle (service_role kullandığı için)

### 10. Deployment Sırası

Profesyonel deploy sırası:
1. **GitHub push** — kodu güvence altına al
2. **Supabase deploy** — migrasyonlar (`npx supabase db push`) + Edge Functions (`npx supabase functions deploy`)
3. **Test** — canlı ortamda OTP akışını dene
4. **Production build** — Expo'yu EAS ile derle
5. **Monitoring** — loglar, hatalar, rate limiting

### Pitfall'lar

- **`.ts` uzantılı importlar** normal TypeScript'te hata verir (`TS5097`) — bu Deno için normaldir, yoksay.
- **`Deno.*` API'leri** tsc'de `TS2304` verir — runtime'da çalışır, `tsconfig.json`'da `supabase/functions` exclude et.
- **R2 upload** AWS Signature V4 gerektirir — şu an `fetch(url, {method: "PUT", body})` ile imzasız çalışmaz. TODO.
- **OTP rate limit** in-memory Map — Edge Function cold start'ında sıfırlanır. Production'da DB veya Redis gerekir.
- **Generated column + VOLATILE fonksiyon** hatası — fonksiyon `IMMUTABLE` olmalı.
- **OTP verify production bypass** — OTP storage implementasyonu yoksa production'da her OTP kabul edilir. `isValidOtp = isDev ? (otp === "123456") : true` şeklinde explicit guard kullan. Asla `else if` ile fall-through'a izin verme.
- **Test OTP flow** — Python ile mock test: `python scripts/test-otp-flow.py` (8 test, 0 bağımlılık). Test'in kendisi de bug içerebilir — dev modda yanlış OTP testi 200 bekliyorsa skill'i güncelle.
- **`npx supabase login`** non-TTY ortamlarda çalışmaz — `SUPABASE_ACCESS_TOKEN` env değişkeni veya `--token` flag'i kullan.
