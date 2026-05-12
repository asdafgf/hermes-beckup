---
name: supabase-edge-functions-nested-dir-fix
description: "Supabase Edge Functions'ta nested dizin (auth/otp-request/) 404 hatası çözümü — fonksiyonları flat yapıya taşı, import path'lerini düzelt, _shared symlink ekle"
category: "devops"
---

# Supabase Edge Functions Nested Dizin Fix

## MSYS2 Path Dönüşümü Sorunu

Windows Git Bash'ten WSL çağrıları yaparken `MSYS_NO_PATHCONV=1` ön eki kullanılmazsa,
`/root/kiralog` gibi WSL yolları otomatik olarak `C:/root/kiralog`'a dönüşür.
Detaylar için `references/msys2-path-fix.md`'ye bak.

```
# Kullanımı çok kolay — adımları sıralıyorum ve senin için hazırlıyorum.

## Ne Zaman Kullanılır
- `npx supabase functions serve` çalışıyor ama tüm fonksiyonlar **HTTP 404 "Function not found"** dönüyor
- Supabase CLI v2.x'te nested dizin yapısı (`auth/otp-request/index.ts`) route kaydında sorun çıkarıyor
- Edge-runtime log'unda `<function-name>` placeholder'ı görünüyor (gerçek fonksiyon isimleri yok)

## Kök Neden
Supabase CLI v2.x Edge Runtime, nested dizin yapısını (`auth/otp-request/`) doğru kaydedemiyor.
İç router yalnızca ilk segmenti arar ve 404 döner. Flat yapı (`otp-request/`) çalışır.

## Çözüm Adımları

### 1. Flat Dizinler Oluştur ve Kopyala
```bash
# WSL içinde (MSYS2 path sorunu varsa MSYS_NO_PATHCONV=1 ile)
cd /root/kiralog/supabase/functions

# Her nested fonksiyon için flat dizin oluşturup index.ts kopyala
mkdir -p auth-kvkk-consent && cp auth/kvkk-consent/index.ts auth-kvkk-consent/
mkdir -p auth-otp-verify && cp auth/otp-verify/index.ts auth-otp-verify/
mkdir -p contracts-create && cp contracts/create/index.ts contracts-create/
mkdir -p contracts-sign && cp contracts/sign/index.ts contracts-sign/
mkdir -p dev-auto-approve && cp dev/auto-approve/index.ts dev-auto-approve/
mkdir -p export-court-pdf && cp export/court-pdf/index.ts export-court-pdf/
mkdir -p media-timestamp && cp media/timestamp/index.ts media-timestamp/
mkdir -p media-upload && cp media/upload/index.ts media-upload/
```

### 2. Import Path'lerini Düzelt
Flat dizinde `../_shared/` yerine `./_shared/` veya `../../_shared/` yerine `./_shared/` kullanılmalı:

```bash
# Python ile tüm flat fonksiyonlarda import path'lerini düzelt
python3 -c "
import os, glob
base = '/root/kiralog/supabase/functions'
fns = ['auth-kvkk-consent','auth-otp-verify','contracts-create','contracts-sign',
       'dev-auto-approve','export-court-pdf','media-timestamp','media-upload','otp-request']
for fn in fns:
    path = os.path.join(base, fn, 'index.ts')
    if not os.path.exists(path):
        print(f'MISS: {fn}')
        continue
    with open(path, 'r') as f:
        content = f.read()
    old = content
    content = content.replace('../../_shared/', './_shared/').replace('../_shared/', './_shared/')
    if content != old:
        with open(path, 'w') as f:
            f.write(content)
        print(f'FIXED: {fn}')
    else:
        print(f'OK: {fn}')
"
```

### 3. _shared Symlink Ekle
Edge Runtime, flat dizin içinde `_shared/` arar. Ana `_shared/`'e symlink ver:

```bash
python3 -c "
import os
base = '/root/kiralog/supabase/functions'
fns = ['auth-kvkk-consent','auth-otp-verify','contracts-create','contracts-sign',
       'dev-auto-approve','export-court-pdf','media-timestamp','media-upload','otp-request']
for fn in fns:
    target = os.path.join(base, fn, '_shared')
    if os.path.islink(target):
        os.unlink(target)
    os.symlink('../_shared', target)
    print(f'{fn}/_shared -> ../_shared')
"
```

### 4. Supabase Yeniden Başlat
```bash
cd /root/kiralog
npx supabase stop
npx supabase start
```

### 5. Doğrulama
```bash
# Tüm flat fonksiyonları test et (beklenen: 401 = auth gerekli, yani fonksiyon çalışıyor)
for fn in otp-request auth-otp-verify auth-kvkk-consent dev-auto-approve contracts-create contracts-sign export-court-pdf media-timestamp media-upload; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -X POST "http://127.0.0.1:54321/functions/v1/$fn" -H "Content-Type: application/json" -d "{}")
  echo "$fn -> $code"
done
```

**Beklenen çıktı:** Tümü HTTP 401 (fonksiyon çalışıyor, JWT auth bekliyor)
**Eğer HTTP 404 dönerse:** Çözüm başarısız — adımları tekrar kontrol et

## Önemli Uyarılar
- **MSYS2 path sorunu:** Windows'ta Git Bash'ten WSL çağrısı yaparken `MSYS_NO_PATHCONV=1` ön eki kullan. Aksi halde `/root/kiralog` → `C:/root/kiralog`'a dönüşür
- **Orijinal nested dizinleri silme:** Eski yapıyı koru (`auth/otp-request/`), sadece kopya oluştur
- **Symlink:** Edge Runtime container restart'ında symlink'ler korunur, ancak `npx supabase start`'in _shared/ hiyerarşisini tekrar kontrol ettiğinden emin ol
- **import_map.json:** Her fonksiyon ayrı import_map kullanabilir; fallback kullanımı WARN verir ama çalışmayı engellemez

## Alternatif Çözümler
1. **Supabase CLI güncelle:** `npm install -g supabase@latest` — 2.99+ sürümlerde nested fix gelmiş olabilir
2. **Kong Admin API route enjeksiyonu:** Kong port 8001'den route manuel ekle (production ortamında)
3. **Deno doğrudan çalıştırma:** `npx supabase functions serve` bypass edilip Deno ile direkt çalıştırılabilir
4. **FUNCTIONS_DIR override:** `SUPABASE_FUNCTIONS_DIR=./supabase/functions/auth npx supabase functions serve`

## Referanslar
- `references/reproduction-recipe.md` — tam teşhis + reproduction adımları (hata ayıklama sırasında bak)
