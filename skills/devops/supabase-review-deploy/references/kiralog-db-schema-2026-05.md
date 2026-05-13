# KiraLog DB Schema Durumu (May 2026)

## Servisler (11 container)
- Studio: `localhost:54323`
- REST API: `localhost:54321/rest/v1/`
- Edge Functions: `localhost:54321/functions/v1/`
- DB (Postgres): `localhost:54322`
- Auth (GoTrue): built-in
- Storage (S3-compatible): `localhost:54321/storage/v1/s3`

## Tablolar (public schema)
| Tablo | Primary Key | Foreign Keys |
|-------|-------------|--------------|
| users | id (uuid, gen_random_uuid()) | — |
| contracts | id (uuid) | owner_id→users.id, tenant_id→users.id |
| payments | id (uuid) | contract_id→contracts.id, payer_id→users.id |
| media | id (uuid) | contract_id→contracts.id, uploader_id→users.id |
| support_tickets | id (uuid) | contract_id→contracts.id, reporter_id→users.id |
| notifications | id (uuid) | user_id→users.id |
| audit_logs | id (uuid) | user_id→users.id |
| sla_tracking | id (uuid) | ticket_id→support_tickets.id |
| kvkk_texts | id (uuid) | — |
| invitations | id (uuid) | inviter_id→users.id, accepted_user_id→users.id |
| user_cloud_accounts | id (uuid) | user_id→users.id |
| tsa_errors | id (uuid) | — |
| public_holidays | id (int32) | — |

## RLS Durumu
- **Aktif:** Tüm kullanıcı tablolarında RLS aktif
- Anonim `INSERT` reddedilir (`42501` — row-level security violation)

## Edge Functions (9 adet)
| Fonksiyon | Yol | Açıklama |
|-----------|-----|----------|
| OTP Request | `auth/otp-request` | SMS/email ile OTP gönderimi |
| OTP Verify | `auth/otp-verify` | OTP doğrulama + kullanıcı oluşturma |
| KVKK Consent | `auth/kvkk-consent` | KVKK onay kaydı |
| Contract Create | `contracts/create` | Sözleşme oluşturma |
| Contract Sign | `contracts/sign` | Sözleşme imzalama |
| Auto Approve | `dev/auto-approve` | Geliştirme: otomatik onay |
| Court PDF Export | `export/court-pdf` | Mahkeme PDF çıktısı |
| Media Timestamp | `media/timestamp` | Medya zaman damgası |
| Media Upload | `media/upload` | Medya yükleme |

## Test Durumu
- ✅ OTP Flow mock test: 8/8 PASS
- ✅ sequential_pipeline: 3 adım çalışıyor
- ✅ REST API sorgusu: users tablosu boş
- ❌ OTP real Edge Function: compile edilmedi (modüller bekleniyor)
