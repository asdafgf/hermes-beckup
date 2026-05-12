---
name: wsl-edge-functions-fix
description: >-
  WSL Ubuntu içinde Supabase Edge Functions serve'i tanılar ve onarır.
  .env kopyalama, Docker kontrolü, container durumu, functions dizin yapısı,
  serve başlatma ve curl test adımlarını otomatik yapar.
---

# WSL Edge Functions Fix

## Ne Zaman Kullanılır
- WSL'de `npx supabase functions serve` çalışmıyor
- "Function not found" (404) hatası alınıyor
- .env dosyası WSL'de bulunamıyor
- Supabase container'ları çalışıyor ama Edge Functions serve etmiyor

## Kullanım

```bash
cd /c/Users/eymen/kiralog
python wsl_edge_fix.py --function auth/otp-request --test-payload '{"phone":"+905555555555"}'
```

## 7 Adım

1. **Ön Kontrol** — WSL bağlantısı + .env varlık kontrolü
2. **.env Kopyalama** — Windows'tan WSL'e .env kopyala
3. **Docker Engine** — Çalışıyor mu? Gerekirse başlat
4. **Supabase Container** — Container'lar aktif mi? Gerekirse npx supabase start
5. **Functions Dizin** — index.ts mevcut mu? Gerekirse kopyala
6. **Functions Serve** — npx supabase functions serve başlat
7. **Curl Test** — Fonksiyonu çağır, HTTP kodu kontrol et

## Bilinen Sorunlar

### "Function not found" (404) — En Sık Sebep: Nested Dizin
Supabase CLI v2.x, nested dizin yapısını (`auth/otp-request/`) doğru kaydedemez. **Çözüm:** `supabase-edge-functions-nested-dir-fix` skill'ini uygula (flat dizine taşı + import path düzelt + symlink).

Olası diğer sebepler:
- `config.toml` eksik → `supabase/config.toml` oluştur
- `import_map.json` eksik → `supabase/functions/import_map.json` oluştur
- supabase/functions dizini WSL'e kopyalanmamış → elle kopyala

### MSYS2 Path Dönüşümü (Windows Git Bash)
WSL komutları `MSYS_NO_PATHCONV=1` ile çağrılmalı. Aksi halde `/root/kiralog` → `C:/root/kiralog`'a dönüşür:
```bash
MSYS_NO_PATHCONV=1 wsl -d Ubuntu -u root -- bash -c "docker ps"
```

### .env WSL'de yok
Script adım 2'de otomatik kopyalar. Ama `SUPABASE_SERVICE_ROLE_KEY` prefix'i Supabase CLI tarafından engellenebilir.

## Script Konumu
`C:\Users\eymen\kiralog\wsl_edge_fix.py`

## İlgili Skill'ler
- `wsl-docker-kurulum` — WSL'de Docker kurulumu
- `wsl-allow-once-cozumu` — WSL Allow Once sorunu
- `wsl-supabase-start-cozumu` — WSL'de Supabase start sorunu
