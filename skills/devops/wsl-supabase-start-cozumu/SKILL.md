---
name: wsl-supabase-start-cozumu
description: >-
  WSL içinde npx supabase start çalışırken Docker imaj indirme, 
  network, timeout veya bağlantı hatası alındığında Claude.ai'a
  anlatılacak sorun tanımı ve Python script şablonu.
---

# WSL Supabase Start Hata Çözümü

## Ne Zaman Kullanılır
- WSL içinde `npx supabase start` çalışırken Docker imajları inemiyor
- Network timeout, connection refused, image not found hataları
- Docker pull başarısız oluyor

## Sorunu Claude.ai'a Anlatma Şablonu

Aşağıdaki metni Claude.ai sohbetine yapıştır:

```
WSL Ubuntu 26.04 içinde npx supabase start çalıştırıyorum ama Docker imajları inerken hata alıyorum.

Ortam:
- Windows 11 + WSL2 Ubuntu
- WSL içinde Docker Engine kurulu (v29.4.3, docker compose plugin v5.1.3)
- Docker servisi aktif
- Node.js + npm WSL içine kurulu
- Supabase CLI: npx supabase start (WSL Node.js ile)

Hata:
[hatayı buraya yapıştır]

Bana bir Python scripti yaz (wsl_supabase_fix.py) şunları yapsın:

1. WSL içinde Docker çalışıyor mu kontrol et (docker ps)
2. Gerekli Supabase imajlarını elle docker pull ile çek
3. Eksik imajları tespit et
4. Hata varsa hangi imajda olduğunu göster
5. Alternatif: Docker DNS ayarlarını düzelt (8.8.8.8)
6. Alternatif: Docker proxy ayarlarını kontrol et
7. Her adımda renkli çıktı ver
8. SONRA yeniden npx supabase start dene
9. Hata çözülmezse log al ve özet çıkar

Script admin gerekmeden WSL içinde çalışsın. subprocess.run ile WSL komutları çalıştırsın. 
wsl -d Ubuntu -u root -- bash -c "..." formatını kullansın (Allow Once'i atlar).
```

## Bilinen Hatalar ve Çözümleri

### 1. Docker DNS Hatası
```
Error response from daemon: Get "https://registry-1.docker.io/v2/": dial tcp: lookup registry-1.docker.io on 127.0.0.53:53: read udp 127.0.0.1...: i/o timeout
```
**Çözüm:** WSL içinde `/etc/docker/daemon.json` dosyasına DNS ekle:
```json
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}
```
Sonra `sudo service docker restart`

### 2. Disk Alanı Yetersiz
```
no space left on device
```
**Çözüm:** `docker system prune -a` ile temizlik

### 3. Network Timeout
```
net/http: TLS handshake timeout
```
**Çözüm:** Imajları tek tek elle çek: `docker pull supabase/postgres:latest`

### 4. Proxy Hatası (Kurumsal)
```
proxyconnect tcp: dial tcp proxy...: connect: connection refused
```
**Çözüm:** Docker proxy ayarlarını kontrol et veya temizle

## Skill Kullanımı
1. Bu skill'i yükle
2. Claude.ai'a sorunu anlat (yukarıdaki şablonla)
3. Python script'i al
4. `python wsl_supabase_fix.py` ile çalıştır
5. Hata çözülmezse çıktıyı Claude'a geri ver
