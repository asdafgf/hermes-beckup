---
name: docker-kurulumu-windows-sessiz
description: >-
  Windows 11'de Docker Desktop'i sessiz kurulum ile yükler.
  Claude.ai'dan Python scripti alınır, Yönetici PowerShell'de çalıştırılır.
  Son çalışan script: docker_kurulum_final.py
---

# Docker Desktop Windows 11 Sessiz Kurulum

## Ne Zaman Kullanılır
- Docker CLI scoop'tan yüklü ama Engine çalışmıyor (`failed to connect to the docker API at npipe://...`)
- Docker Desktop kurulu değil
- İndirme + kurulum + WSL2 hazırlığını tek script'te yapmak istiyorsun

## Kullanım Akışı

### 1. Claude.ai'a Sorun Durumunu Anlat
Aşağıdaki şablonu Claude.ai sohbetine yapıştır:

```
Windows 11'de Docker Desktop sessiz kurulumu için Python scripti yaz.

Durum:
- Windows 11, Python 3.x
- Docker CLI scoop'tan yüklü (v29.4.3) ama Engine çalışmıyor
- Docker Desktop kurulu DEĞİL
- WSL2 Ubuntu yüklü ama "Stopped"
- Installer zaten indirilmiş olabilir: C:\Users\eymen\AppData\Local\Temp\DockerDesktopInstaller.exe

Script gereksinimleri:
1. Admin kontrolü (değilse hata verip çıksın, UAC yükseltme DENEMESİN)
2. WSL2 hazırlığı: wsl --update, wsl -d Ubuntu echo ok
3. Mevcut installer varsa kullansın, yoksa indirsin
4. Sessiz kurulum: installer.exe install --quiet (timeout 720s)
5. Docker Desktop'ı başlatsın
6. docker ps hazır olana kadar bekle (maks 180s, her 10s'de bir)
7. [1/5] formatında adım adım çıktı, ANSI renk yok, input() yok
8. Hata yakalama + özet + exit code
```

### 2. Script'i Kaydet
```bash
cd /c/Users/eymen/kiralog
# Claude.ai'dan gelen kodu docker_kurulum_final.py olarak kaydet
```

### 3. Çalıştır — ÖNCE OTOMATİK DENE, OLMazsa elle
Denenecek sıra:

```bash
# Seçenek A: run_admin.py (4 strateji dener, UAC penceresi açar)
cd /c/Users/eymen/kiralog
python run_admin.py

# Seçenek B: admin_powershell.py (3 strateji dener)
python admin_powershell.py "C:\Users\eymen\kiralog\docker_kurulum_final.py"
```

**Eğer hiçbiri çalışmazsa (beklenen durum):**
- Windows tuşu → "PowerShell" yaz → Sağ tık → "Yönetici olarak çalıştır"
- Açılan pencerede:
```powershell
cd C:\Users\eymen\kiralog
python docker_kurulum_final.py
```

## Script Yapısı (5 Adım)

1/5 → Admin kontrolü (yoksa hata + çıkış)
2/5 → WSL2 güncelle + Ubuntu başlat (~2 dk)
3/5 → Installer bul/indir + sessiz kurulum (~10-12 dk)
4/5 → Docker Desktop'ı başlat
5/5 → docker ps hazır olana kadar bekle (~1-3 dk)

## Bilinen Tuzaklar (Pitfalls)

### ❌ UAC Yükseltme Çalışmaz (KRİTİK)
- Hermes venv'i (`AppData\Local\hermes\hermes-agent\venv\`) içinden **tüm** UAC yükseltme yöntemleri başarısız olabilir:
  - `ShellExecuteW runas` → Access Denied (kod 5)
  - `Start-Process -Verb RunAs` → "Kullanıcı tarafından iptal edildi"
  - `schtasks /rl HIGHEST` → yetki yetersiz
  - VBScript ShellExecute → aynı kısıt
- **Çözüm:** Script kendini yükseltmeye çalışmasın, sadece admin kontrolü yapıp hata versin
- **Son çare her zaman:** Kullanıcıya elle Yönetici PowerShell'de çalıştırmasını söyle

### ❌ İndirme Zaman Aşımı
- Installer ~617 MB, foreground timeout'u aşabilir
- **Çözüm:** Background mode + notify_on_complete kullan

### ❌ WSL2 "Stopped" Durumda
- Docker Engine WSL2 gerektirir
- **Çözüm:** Script `wsl --update` + `wsl -d Ubuntu echo ok` ile distro'yu tetiklesin

### ✅ Kabul Edilebilir Exit Code'lar
- 0 → Başarılı
- 1638 → Zaten kurulu (güncel)
- 3010 → Kurulum tamam, yeniden başlat gerekebilir

## Alternatif: WSL içine Docker Kur (Admin Gerekmez)

Eğer Docker Desktop Windows kurulumu UAC nedeniyle başarısız olursa, Docker'ı doğrudan WSL Ubuntu içine kurabilirsin. **Bu yöntem admin yetkisi GEREKTİRMEZ.**

### Script: wsl_docker_kur.py

```bash
cd /c/Users/eymen/kiralog
python wsl_docker_kur.py
```

### Ne Yapar
1. WSL erişim kontrolü
2. Eski Docker artıklarını temizle
3. apt-get update
4. Bağımlılıklar (ca-certificates, curl, gnupg)
5. Docker GPG anahtarı ekle
6. Docker reposu ekle
7. apt-get update (repo ile)
8. Docker Engine + CLI + Compose kur
9. Docker servisini başlat
10. Kullanıcıyı docker grubuna ekle
11. hello-world testi

### Önemli Notlar
- Docker WSL içinde çalışır — `wsl -e bash -c "docker ..."` veya WSL terminal'inden erişilir
- Windows'tan `docker` komutuna doğrudan erişim olmaz (Docker Desktop gerekir)
- Docker Compose dahil kurulur
- İlk seferinde `sudo docker ...` kullanılır, yeniden başlatma sonrası sudo gerekmez

### WSL Docker Kullanımı
```bash
# WSL terminal
wsl
docker ps
docker compose up -d

# veya doğrudan git-bash'ten
wsl -e bash -c "docker ps"
wsl -e bash -c "docker compose -f /path/to/docker-compose.yml up -d"
```

## İlgili Skill'ler
- `python-admin-runner-windows` → admin elevation için otomatik/manuel yöntemler (4 strateji)
- `docker-kurulumu-windows-sessiz` (bu skill) → Docker kurulumu için ana skill
- Script `scripts/wsl_docker_kur.py` → WSL içine Docker kur (admin gerekmez, alternatif)
