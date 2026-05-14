# Windows Dosya Konumları Rehberi

## OneDrive Desktop vs Normal Desktop

OneDrive kullanan Windows kullanıcılarında masaüstü konumu farklı olabilir:

| Sembolik yol | Gerçek yol |
|---|---|
| `C:\Users\eymen\Desktop` | Genelde boş veya OneDrive redirect |
| `C:\Users\eymen\OneDrive\Masaüstü` | OneDrive senkronize masaüstü (Türkçe Windows) |
| `C:\Users\eymen\OneDrive\Desktop` | İngilizce Windows |

**Arama stratejisi:** `search_files(path="C:\Users\eymen", pattern="*DosyaAdi*")` tüm alt dizinleri tarar
ve hem Desktop hem OneDrive paths'lerini bulur.

## ZIP İçerik İnceleme

Replit'ten gelen ZIP'ler genelde:
- Büyük: ~200-600 MB (çoğu pnpm cache / node_modules)
- Gerçek proje dosyaları: ~15-50 MB
- ZIP içinde kök klasör var (örn. `Runners-Journey/`)
- `|` karakteri içeren dosya adları olabilir (Windows'ta geçersiz)

### İnceleme komutu:
```python
import zipfile
path = r'C:\path\to\proje.zip'
with zipfile.ZipFile(path, 'r') as z:
    names = z.namelist()
    # Klasör yapısı
    dirs = set()
    for n in names:
        parts = n.split('/')
        dirs.add('/'.join(parts[:2]))
    for d in sorted(dirs):
        print(d)
    # Önemli dosyalar
    for n in names:
        if n.endswith(('.gradle', '.kt', '.kts', 'package.json', 'app.json')):
            print(n)
```

### Çıkarma (cache hariç):
```python
import zipfile, os
with zipfile.ZipFile(path, 'r') as z:
    for n in z.namelist():
        if '.local/share/pnpm' in n or 'node_modules' in n:
            continue
        # strip root dir
        parts = n.split('/', 1)
        rel = parts[1] if len(parts) > 1 else n
        if not rel: continue
        dest = os.path.join(target, rel)
        if n.endswith('/'):
            os.makedirs(dest, exist_ok=True)
        else:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            try:
                with z.open(n) as src, open(dest, 'wb') as dst:
                    dst.write(src.read())
            except OSError as e:
                # '|' karakteri Windows'ta geçersiz
                print(f'Skipping {rel}: {e}')
```
