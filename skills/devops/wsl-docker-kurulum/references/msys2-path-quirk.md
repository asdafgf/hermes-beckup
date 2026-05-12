# MSYS2 Path Dönüşümü: Windows Git Bash'te WSL Çağrısı

## Sorun
Git Bash (MINGW64), `/root/kiralog` gibi Unix yollarını otomatik olarak
`C:\root\kiralog`'a çevirir. Bu, `wsl -d Ubuntu -u root -- bash -c "cat /root/..."`
komutlarının çalışmasını engeller.

## Çözüm
Komutun önüne `MSYS_NO_PATHCONV=1` ekle:

```bash
MSYS_NO_PATHCONV=1 wsl -d Ubuntu -u root -- bash -c "cat /root/kiralog/..."
```

## Alternatif (export)
```bash
export MSYS_NO_PATHCONV=1
# Artık tüm wsl çağrıları düzgün çalışır
```

## İpuçları
- `git-bash` terminalinde `echo $MSYSTEM` → `MINGW64` çıkıyorsa bu sorun var demektir
- Aynı sorun `curl`'ün göreceli yollarında da görülür
- PowerShell'den çalıştırılan komutlarda bu sorun yok
- `wsl --` argümanı bile MSYS2 tarafından yutulabilir — her zaman `MSYS_NO_PATHCONV=1` ön eki kullan
