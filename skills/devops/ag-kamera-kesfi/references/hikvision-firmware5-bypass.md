# Hikvision Firmware 5.x+ — Web Arayüzü 404 Çözüm Rehberi

## Belirti
- nmap'te port 80 (HTTP) ve 554 (RTSP) açık
- Tüm HTTP endpoint'leri **404 Not Found** döner
- Server header: `webserver` (Hikvision'a özel)
- HTTP banner'da güvenlik başlıkları: `X-Frame-Options: SAMEORIGIN`, `CSP: default-src 'self'`, `X-XSS-Protection`
- ONVIF SOAP sorguları **401 Unauthorized** döner
- Varsayılan şifrelerin hiçbiri çalışmaz

## Sebep
Hikvision firmware 5.x+ (güvenlik duvarı aktif, web arayüzü devre dışı). Kamera tamamen kilitli.

## Denenmiş ve Başarısız Yöntemler

| Yöntem | Sonuç |
|--------|-------|
| HTTP varsayılan şifreler (30+ komb.) | 401 |
| ONVIF SOAP (auth'suz) | 401 |
| CVE-2017-7921 (snapshot bypass) | 405 Method Not Allowed |
| CVE-2021-36260 (backdoor) | 405 |
| ISAPI/PSIA/SDK endpoint'leri | Hepsi 404 |
| RTSP auth'suz kanallar | Hepsi 401 |
| onvif-http/snapshot | 404 |
| Security/users.xml | 405 |
| System/configurationFile | 405 |
| PSIA/Streaming | 404 |
| Brute-force (1000+ deneme) | Hepsi 401 |

## Çalışan Tek Yöntem

### 1. Fiziksel Reset (En Garantili)
Kameranın üzerindeki **reset düğmesine** ataç/uçlu kalemle **10-15 saniye** basılı tut. Fabrika ayarlarına döner:
- Kullanıcı: `admin`
- Şifre: boş veya `12345`

### 2. SADP Tool (Hikvision Resmi Aracı)
SADP, aynı LAN'daki Hikvision cihazlarını bulur ve şifre sıfırlamaya izin verir.

**İndir:** https://sadptool.net/SADP.zip (68 MB)
**Kurulum:**
1. ZIP'i çıkar
2. `SADP.exe`'yi **Yönetici olarak çalıştır**
3. Npcap kurulumunu onayla (gerekiyorsa)
4. Cihaz listelenecek → seç → "Forgot Password"
5. XML dosyası export et → Hikvision support'a gönder (veya)
6. Cihaz modeline bağlı olarak güvenlik kodu ile sıfırlama

### 3. Hik-Connect / Hik-Partner Pro (Mobil Uygulama)
Kameranın bağlı olduğu Hik-Connect hesabı varsa:
- Uygulamada cihazı bul
- Ayarlar → Password Reset
- Yeni şifre belirle

### 4. ONVIF WS-Discovery (Sadece Tespit İçin)
Python ile multicast discovery:
```python
import socket
msg = '<?xml version="1.0"?>...<wsd:Probe>...'  # ONVIF probe mesajı
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.settimeout(5)
sock.sendto(msg.encode(), ('239.255.255.250', 3702))
sock.sendto(msg.encode(), ('192.168.0.255', 3702))
data, addr = sock.recvfrom(4096)  # Cihaz IP'si döner
```

## Önemli Uyarılar
- **Firmware 5.x+ olan Hikvision'da web arayüzü yoktur.** Çözüm: reset veya SADP.
- "CODE:" etiketi şifre DEĞİLDİR — seri no/aktivasyon kodudur.
- HTTP'de tüm istekler 404 dönüyorsa: güvenlik duvarı aktiftir, brute-force işe yaramaz.
- SADP kurulumunda Npcap gerekebilir (Windows için).
- SADP aynı broadcast domain'de olmalıdır (farklı subnet'te çalışmaz).
