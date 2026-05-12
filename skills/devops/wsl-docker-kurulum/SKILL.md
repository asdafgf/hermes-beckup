---
name: wsl-docker-kurulum
description: >-
  WSL Ubuntu içine Docker Engine + Compose kurar. Admin/root gerekmez,
  UAC sorunu yaşanmaz. 10 adımda otomatik kurulum.
---

# WSL Ubuntu Docker Kurulum

## Ne Zaman Kullanılır
- Docker Desktop kurulamıyor (UAC hatası, Access Denied kod 5)
- Windows'ta Docker Engine çalışmıyor
- Admin yetkisi olmadan Docker lazım
- WSL2 Ubuntu yüklü ama "Stopped" durumda

## Nasıl Çalışır
WSL Ubuntu içine Docker Engine kurar. Windows ile tam uyumlu çalışır:
`docker ps` komutları WSL içinden çalışır, container'lar Windows ile paylaşılır.

## Kullanım

```bash
cd /c/Users/eymen/kiralog
python wsl_docker_kur.py
```

Admin gerekmez, UAC istemez. Direkt çalışır.

## 10 Adım Akışı

| Adım | İşlem | Süre |
|------|-------|------|
| 1 | WSL erişim kontrolü | Anlık |
| 2 | Eski Docker artıkları temizleme | ~5sn |
| 3 | apt-get update | ~30sn |
| 4 | Bağımlılıklar (curl, gnupg, ca-certificates) | ~30sn |
| 5 | Docker GPG anahtarı ekleme | ~5sn |
| 6 | Docker APT reposu ekleme | ~5sn |
| 7 | apt-get update (Docker reposuyla) | ~30sn |
| 8 | Docker Engine + CLI + Compose + Buildx kurulumu | ~90sn |
| 9 | Docker servisi başlatma | ~5sn |
| 10 | hello-world test container'ı çalıştırma | ~30sn |

**Toplam: ~5-10 dakika**

## Sonuç
✅ Docker Engine (v29.4.3)
✅ Docker CLI
✅ Docker Compose Plugin (v5.1.3)
✅ Docker Buildx Plugin
✅ hello-world testi başarılı

## Önemli Uyarılar

### MSYS2 Path Dönüşümü (Windows Git Bash)
Bu skill'in tüm WSL komutları `MSYS_NO_PATHCONV=1` ön ekiyle çağrılmalıdır.
Aksi halde `/root/...` gibi Linux path'leri Windows Git Bash tarafından `C:/root/...`'ye dönüştürülür.
```bash
# Doğru:
MSYS_NO_PATHCONV=1 wsl -d Ubuntu -u root -- bash -c "docker ps"

# Yanlış (path kırılır):
wsl -d Ubuntu -u root -- docker ps
```

`$MSYSTEM` değeri `MINGW64` ise bu sorun kesin vardır.

## Kullanım (Kurulum Sonrası)

WSL içinde Docker kullanmak için:
```bash
wsl -d Ubuntu -e bash -c "docker ps"
```

Veya WSL terminaline gir:
```bash
wsl
docker ps
```

İlk seferde `sudo docker ...` gerekebilir. Gruba ekleme için:
```bash
wsl --shutdown
# WSL'yi tekrar açınca docker grubu aktif olur
```

## Önceki Denemeler (Bilinen Sorunlar)
Bu yönteme geçilmeden önce denenip başarısız olan yöntemler:
- ❌ ShellExecuteW runas (venv) → Access Denied kod 5
- ❌ Start-Process -Verb RunAs → Kullanıcı iptal
- ❌ Scheduled Task → Erişim engellendi
- ❌ VBScript köprüsü → Timeout
- ❌ PowerShell Doğrudan → UAC onayı alınamadı

**Çözüm:** WSL içine kurulum — admin/UAC gerektirmez, direkt çalışır.

## Script Konumu
`C:\Users\eymen\kiralog\wsl_docker_kur.py`

Script içeriği için skill'in `assets/wsl_docker_kur.py` dosyasına bak.
