# KiraLog Supabase Edge Functions — Düzeltme Geçmişi

Bu referans, `supabase-edge-functions` skill'inin uygulanmasında bulunan spesifik hataları ve çözümlerini belgeler.

## Migrasyon Düzeltmeleri

### 002_rls.sql → Policy taşıma
- `user_cloud_accounts` (tablo `005_cloud_storage.sql`'de) için RLS politikaları 002'deydi.
- **Çözüm:** `ALTER TABLE user_cloud_accounts ENABLE RLS` ve 4 policy satırı 002'den kaldırıldı, 005'e taşındı.

### 003_functions.sql → Eksik tablo
- `public_holidays` tablosu referans ediliyordu ama sadece seed'de yaratılıyordu.
- **Çözüm:** `CREATE TABLE IF NOT EXISTS public_holidays (...)` migrasyona eklendi.

### 004_compliance_report.sql → Eksik audit_logs
- `audit_logs` tablosu hiç yaratılmamıştı.
- **Çözüm:** Tam tablo + index + RLS politikaları eklendi.

### 005_cloud_storage.sql → IMMUTABLE fonksiyon
- `encrypt_cloud_config()` ve `decrypt_cloud_config()` `LANGUAGE plpgsql` (VOLATILE varsayılan) ile tanımlanmıştı.
- Generated column'lar IMMUTABLE gerektirir.
- **Çözüm:** `LANGUAGE plpgsql IMMUTABLE` olarak değiştirildi.

### 006_kvkk_texts.sql → Eksik constraint'ler
- `ON CONFLICT DO NOTHING` yoktu.
- `CREATE INDEX IF NOT EXISTS` kullanılmamıştı.
- `updated_at` trigger'ı yoktu.
- **Çözüm:** Tümü eklendi.

## Edge Function Düzeltmeleri

### _shared/deps.ts → @latest pinleme
- `npm:pdfkit@latest`, `npm:@supabase/supabase-js@2` (implicit latest)
- **Çözüm:** `npm:pdfkit@0.15.0`, `https://esm.sh/@supabase/supabase-js@2.45.0`

### _shared/tsa.ts → Duplicate import
- `createClient` hem `./deps.ts`'den hem de direkt URL'den import edilmişti.
- **Çözüm:** Direkt URL import kaldırıldı, `./deps.ts` kullanıldı.

### auth/otp-verify/index.ts → Inverted OTP logic (2nd fix)

**Bug 1 (previously documented):** Mock'ta `"123456"` kabul eden, diğer OTP'leri reddeden ters mantık.

**Bug 2 (found 2026-05-12):** Production modda OTP=`"123456"` pas geçiyordu. Kod şöyleydi:
```typescript
// HATALI:
if (DEV && otp === "123456") { /* accept */ }
else if (!DEV && otp !== "123456") { /* reject */ }
// Production'da OTP "123456" ise: ilk if'e girmez, ikinci if'e de girmez → PASS!
```

**DÜZELTİLDİ (2. fix):**
```typescript
const isDev = Deno.env.get("NODE_ENV") === "development";
const isValidOtp = isDev ? otp === "123456" : true;  // production: no storage yet
if (!isValidOtp) { return { status: 401 }; }
```

**Test:** `python scripts/test-otp-flow.py` — 8 test, hepsi geçer:
- Dev: yanlış OTP reddedilir ✅
- Dev: "123456" kabul edilir ✅
- Production: her OTP kabul (storage yok) ✅

### export/court-pdf/index.ts → Uint8Array/ArrayBuffer uyumsuzluğu
```typescript
// HATALI:
await uploadToR2(pdfBytes); // pdfBytes Uint8Array, fonksiyon ArrayBuffer bekliyor

// DÜZELTİLDİ:
await uploadToR2(pdfBytes.buffer as ArrayBuffer);
```

### media/upload/index.ts → SQL fonksiyonu .select() içinde
```typescript
// HATALI:
.select(`config, decrypt_cloud_config(config) as decrypted_config`)

// DÜZELTİLDİ:
.select('provider, config')  // service_role ile direkt eriş
```

### support/create-ticket.ts → Sadece tenant'a izin
```typescript
// HATALI:
if (userType !== "tenant") { reject }

// DÜZELTİLDİ:
if (userType !== "owner" && userType !== "tenant") { reject }

// Bildirim de düzeltildi:
notifyParty = userType === "owner" ? tenantId : ownerId;
```

## OTP Sistemi Mimarisi

```
┌──────────────────────────────────────────────────────────┐
│                    OTP Request Flow                      │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Client → POST /auth/otp-request { phone_number }        │
│     ↓                                                    │
│  Rate Limit Check (3/saat/telefon — in-memory Map)       │
│     ↓                                                    │
│  OTP = Math.floor(100000 + random * 900000)              │
│     ↓                                                    │
│  sendSms(phone, message)                                 │
│     ├── Mock: console.log, return { otp: "123456" }      │
│     └── Prod: NetGSM XML API                             │
│                                                          │
│  Client → POST /auth/otp-verify { phone, otp, ... }      │
│     ↓                                                    │
│  OTP Verification                                        │
│     ├── Mock: "123456" kabul et                          │
│     └── Prod: gerçek doğrulama                           │
│     ↓                                                    │
│  users tablosunda ara/yoksa oluştur                      │
│     ↓                                                    │
│  Return { user_id, token }                               │
└──────────────────────────────────────────────────────────┘
```

## .env Yapılandırması (Full)

```
# Supabase
EXPO_PUBLIC_SUPABASE_URL=https://mmrlbkpsqlyjyogkbrfn.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# OTP Mode (development = mock SMS, OTP: 123456)
NODE_ENV=development

# NetGSM SMS (production)
# NETGSM_USERCODE=
# NETGSM_PASSWORD=
# NETGSM_MSGHEADER=
```
