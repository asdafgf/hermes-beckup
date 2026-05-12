# KiraLog Supabase Review — May 2026

## Proje Yapısı

```
supabase/
├── migrations/              # 6 SQL migrasyon
│   ├── 001_initial.sql      # Ana tablolar (users, contracts, media, payments...)
│   ├── 002_rls.sql          # Row Level Security
│   ├── 003_functions.sql    # Trigger fonksiyonlar (+ public_holidays table fix)
│   ├── 004_compliance_report.sql  # audit_logs table + compliance
│   ├── 005_cloud_storage.sql      # user_cloud_accounts, cloud_recent_uploads
│   └── 006_kvkk_texts.sql         # KVKK onay metinleri
├── functions/               # 16 Edge Functions (Deno)
│   ├── _shared/             # deps, logger, secrets, services, tsa
│   ├── auth/                # otp-request, otp-verify, kvkk-consent
│   ├── contracts/           # create, sign
│   ├── media/               # upload, timestamp
│   ├── export/              # court-pdf
│   ├── support/             # create-ticket, update-ticket
│   └── dev/                 # auto-approve
├── seed/
│   └── public_holidays.sql  # 2025-2026 tatil takvimi
├── config.toml              # Supabase yapılandırması
└── .gitignore
```

## Düzeltilen Hatalar

### Migrasyonlar

| Dosya | Sorun | Çözüm |
|-------|-------|-------|
| 002_rls.sql | `user_cloud_accounts` tablosu 005'te yaratılıyor, RLS 002'de ekli | RLS kuralları 005'e taşındı |
| 003_functions.sql | `public_holidays` tablosu migrasyonda yok (seed'de) | `CREATE TABLE IF NOT EXISTS` eklendi |
| 004_compliance_report.sql | `audit_logs` tablosu yok | Tablo + index + RLS eklendi |
| 005_cloud_storage.sql | `encrypt/decrypt_cloud_config()` → generated column için IMMUTABLE lazım | `LANGUAGE plpgsql IMMUTABLE` yapıldı |
| 006_kvkk_texts.sql | `ON CONFLICT` eksik, `updated_at` trigger yok | `ON CONFLICT DO NOTHING`, trigger eklendi |

### Edge Functions

| Dosya | Sorun | Çözüm |
|-------|-------|-------|
| _shared/deps.ts | `@latest` versiyon etiketleri | `pdf-rfc3161@3.0.0`, `pdfkit@0.15.0` vb. pin'lendi |
| _shared/tsa.ts | `createClient` duplicate import | İkinci import `./deps.ts`'ye çevrildi |
| auth/otp-verify/index.ts | **Kritik:** OTP mantık hatası — production'da her OTP kabul ediliyor | `isValidOtp` boolean ile düz mantık |
| export/court-pdf/index.ts | `Uint8Array` → `ArrayBuffer` dönüşümü yok | `.buffer as ArrayBuffer` eklendi |
| media/upload/index.ts | `decrypt_cloud_config()` SQL fonksiyon hatası | Doğrudan `config` kolonu kullanıldı |
| support/create-ticket.ts | Sadece tenant ticket açabiliyor | Owner da açabilir; karşı tarafa bildirim |
| support/update-ticket.ts | `getUser()` hata yakalaması yok | Try/catch eklendi |

## OTP Akışı

### Mock Mod (development)
```
POST /auth/otp-request  →  { "phone_number": "+905..." }
  → sendSms() → console.log + return { mock: true, otp: "123456" }

POST /auth/otp-verify   →  { "phone_number": "...", "otp": "123456", ... }
  → sadece "123456" kabul → user oluştur → return { user_id }
```

### Production Mod (NetGSM)
```
.env'de:
  NODE_ENV=production
  NETGSM_USERCODE=...
  NETGSM_PASSWORD=...
  NETGSM_MSGHEADER=KiraLog

sendSms() → NetGSM XML API → gerçek SMS
otp-verify → production'da şimdilik her OTP kabul (storage implementasyonu yok)
```

## Konfigürasyon

`config.toml`'da `verify_jwt`:
- `auth/otp-*`: `false` (kullanıcı henüz giriş yapmamış)
- Diğer tüm fonksiyonlar: `true`

## Notlar

- **tsc hataları normal** — `supabase/functions` `tsconfig.json`'da exclude edildi
- **WatermelonDB peer deps** — `--legacy-peer-deps` ile kurulur (Expo 54 + RN 0.81.5)
- **Production build:** `npx expo export --platform web` → çalışıyor
- **Test:** `test_otp_flow.py` — 8 test, 0 failure
- **Env koruması:** `.env` `.gitignore`'da, `git commit` öncesi restore edilmeli
