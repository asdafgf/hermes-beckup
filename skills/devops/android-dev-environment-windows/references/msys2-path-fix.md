# MSYS2 Path Dönüşümü — Hızlı Başvuru

## Sorun
Git Bash (MSYS2/MINGW64) `/c/Users/..` gibi Unix-stili yolları
otomatik olarak `C:\Users\..` Windows yoluna çevirir.
Bu, `wsl` komutlarına `/root/...` gibi WSL yolları geçerken bozulmaya yol açar.

## Çözüm

### En Güvenilir — Ortam Değişkeni
Her `wsl` çağrısından önce:
```bash
MSYS_NO_PATHCONV=1 wsl -d Ubuntu -u root -- bash -c "komut"
```

### Alternatif — Çift Slash
```bash
wsl -d Ubuntu -u root -- ls //root/kiralog    # // MSYS dönüşümünü engeller
```

### Kalıcı Çözüm (isteğe bağlı)
```bash
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL="*"
```
Bunu `~/.bashrc` veya `~/.bash_profile`'a ekleyebilirsin.

## Neden Çalışır
- MSYS2, `/` ile başlayan argümanları Windows yolu olarak yorumlar
- `MSYS_NO_PATHCONV=1` bu dönüşümü **tamamen kapatır**
- `MSYS2_ARG_CONV_EXCL="*"` tüm argümanların dönüşümünü engeller
- Çift `//` ise MSYS2'ye "bu bir Windows yolu değil" der

## Hata Teşhisi
Eğer `wsl` çıktısında şu hataları görüyorsan:
```
ls: cannot access 'C:/Program Files/Git/root/...'
```
→ **MSYS2 PATH dönüşümü aktif** — `MSYS_NO_PATHCONV=1` kullan.
