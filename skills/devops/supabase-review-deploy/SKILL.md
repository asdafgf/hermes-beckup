---
name: supabase-review-deploy
description: Supabase migration + Edge Function review, fix, and production readiness. Scans all SQL migrations for schema issues, reviews Deno Edge Functions for runtime bugs, creates config.toml, and produces a deployment-ready report.
---
# Supabase Review & Deploy

## Ne Zaman Kullanılır

Kullanıcı bir Supabase projesini (migrasyonlar + Edge Functions) production-ready hale getirmek istediğinde. Şu durumlarda tetiklenir:
- "Supabase migrasyonları hazırla"
- "Edge Functions'ı review et"
- "Supabase config.toml oluştur"
- Projeyi Supabase'e deploy etmeden önce son kontrol

## Genel İş Akışı

### 0. Ön Hazırlık

Todo ile planla. Proje yapısını tara:

```bash
# Migrasyonları listele
ls -la supabase/migrations/

# Edge Functions'ları listele
find supabase/functions -name "*.ts" -not -path "*/node_modules/*" | sort

# Config var mı?
ls supabase/config.toml 2>/dev/null || echo "config.toml yok — oluşturulacak"

# Seed var mı?
ls supabase/seed/ 2>/dev/null
```

### 1. Migrasyon Review (SQL)

Her `.sql` migrasyon dosyasını oku ve şunları kontrol et:

**a) Tablo varlığı kontrolleri:**
- Referans verilen tablo aynı migrasyonda veya daha önceki bir migrasyonda tanımlanmış mı?
- `REFERENCES` kısıtlamaları doğru tablo/kolona işaret ediyor mu?
- `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` yapılan tablo bu noktada var mı?

**b) Yaygın SQL sorunları:**
- `FUNCTIONS` için `LANGUAGE` doğru mu? (`plpgsql`, `sql`, `plv8`)
- `VOLATILE` / `IMMUTABLE` / `STABLE` doğru seçilmiş mi? (generated column'lar `IMMUTABLE` ister)
- `ON CONFLICT` kullanılıyorsa unique constraint/index var mı?
- `IF NOT EXISTS` / `OR REPLACE` eksik mi?

**c) Düzeltme stratejisi:**
- En iyi çözüm: tabloyu eksik olduğu migrasyonda `CREATE TABLE IF NOT EXISTS` ile oluşturmak
- Alternatif: RLS politikalarını tablonun yaratıldığı migrasyona taşımak
- Son çare: yeni bir migrasyon dosyası oluşturmak

### 2. Edge Functions Review (TypeScript/Deno)

Her fonksiyon dosyasını oku ve şunları kontrol et:

**a) Import doğrulaması:**
```typescript
// Deno URL importları
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// Göreceli importlar (çalışıyor mu?)
import { getSecrets } from "../_shared/secrets.ts";
```

**b) Yaygın hatalar:**
- `Deno.env.get()` — sadece Deno runtime'da çalışır, normal tsc hata verir (normal)
- `FormData.get()` — DOM tipleri Deno'da farklı; `request.formData()` sonrası `.get()` çalışır ama tsc hata verebilir
- `@latest` versiyon etiketi — production'da pinne'lenmeli (`npm:package@x.y.z`)
- İmplicit `any` parametreler — tip belirtilmemiş `req`, `res` parametreleri

**c) Logic hataları:**
- OTP doğrulama mantığı ters mi? (dev modda `"123456"` kabul edilmeli, reddedilmemeli)
- Auth kontrolü: doğru kullanıcı tipi yetkilendirilmiş mi? (örn. sadece tenant değil, owner da ticket açabilmeli)
- `getUser()` hata yakalaması var mı?
- Byte/Uint8Array dönüşümleri doğru mu? (örn. `Uint8Array` → `ArrayBuffer`)

**d) Güvenlik:**
- `service_role` key kullanılıyorsa, endpoint JWT doğrulamalı mı? (config.toml'da `verify_jwt = true`)
- Kullanıcı kendi user_id'sini manipüle edebilir mi? (oturum açmış kullanıcının kimliği parametreden değil, JWT'den alınmalı)

### 3. config.toml Oluşturma

Eğer yoksa, standard Supabase config.toml oluştur:

```toml
[api]
enabled = true
port = 54321

[auth]
enabled = true

[functions]
enabled = true
verify_jwt = true
import_map = "./import_map.json"

[storage]
enabled = true
file_size_limit = "50MB"
```

Proje adını ve seed yolunu da ekle:
```toml
[project_id = "kiralog"]
[analytics]
seed = "supabase/seed/public_holidays.sql"
```

### 4. Deploy Hazırlığı

Son kontroller:

```bash
# Süpabase CLI mevcut mu?
npx supabase --version 2>/dev/null || echo "Supabase CLI gerekli"

# Production env değişkenleri set edilmiş mi?
grep -r "mock-" .env 2>/dev/null && echo "⚠️ Mock değerler var!"
grep -r "your-project\|your-anon" .env 2>/dev/null && echo "⚠️ Placeholder değerler var!"

# Edge Functions deploy'a hazır mı?
cd supabase/functions && for f in */; do
  echo "$f: $(ls $f/index.ts 2>/dev/null || ls $f*.ts 2>/dev/null)"
done
```

## Pitfall'lar

- **tsc Deno hatalarını düzeltmeye çalışma** — `Deno.*`, URL importlar, `.ts` extension importlar normal TypeScript'e yabancıdır. Bunlar `tsconfig.json`'da `exclude` ile kapatılır, hata olarak işlenmez.
- **Migrasyon sırası önemli** — Migration'lar `001_`, `002_` prefix sırasına göre çalışır. `002_rls.sql` içinde `005_cloud_storage.sql`'de yaratılan tabloya RLS eklemek runtime hatası verir.
- **Seed vs Migration** — Seed verisi (`public_holidays`) referans alınan bir tablo ise bu tablo mutlaka bir migrasyonda oluşturulmalı, seed'de CREATE TABLE olmamalı.
- **`@latest` versiyon etiketleri** — Deno Edge Functions'da `npm:package@latest` kullanma. Her deploy farklı sürüm alabilir. Belirli versiyona pinnele.
- **`Uint8Array` vs `ArrayBuffer`** — Deno'da `crypto.subtle.digest()` `ArrayBuffer`, `new Uint8Array()` ise `Uint8Array` döner. Bunları karıştırmak TS hatasına yol açar. `Uint8Array.buffer` ile dönüştür.
- **OTP rate limiting in-memory** — Edge Functions cold start'te sıfırlanır. Production'da Redis veya DB tabanlı rate limiting gerekir.
- **`verify_jwt = true` yetmez** — Kullanıcı ID'si JWT'den alınmalı, body'den gelen parametreye güvenilmemeli.

### OTP Doğrulama Mantığı

OTP doğrulama (`otp-verify/index.ts`) ters mantık hatasına çok yatkındır.

**DOĞRU mantık:**
```typescript
const isDev = Deno.env.get("NODE_ENV") === "development";
const isValidOtp = isDev ? otp === "123456" : true;
if (!isValidOtp) {
  return new Response(JSON.stringify({ error: "Invalid OTP" }), { status: 401 });
}
```

**YANLIŞ mantık (kaçınılması gereken):**
Hatalı else-if yapısı production'da `"123456"` mock OTP'sini atlar ve kabul eder.

**Test script:** `test_otp_flow.py` OTP akışını simüle eder (rate limiting, mock/prod mod).

**Test script:** `scripts/test-otp-flow.py` — OTP akışı testi (rate limiting, mock/prod mod, hatalı OTP).

**Referans dosyası:** `references/kiralog-supabase-review.md` — KiraLog projesine özel tüm migrasyon/function fix detayları.

**OTP kanal alternatifi:** `_shared/services.ts`'e `sendEmailOtp(email, otp)` eklenir. NetGSM SMS: `.env`'de `NETGSM_USERCODE`, `NETGSM_PASSWORD`, `NETGSM_MSGHEADER`.
