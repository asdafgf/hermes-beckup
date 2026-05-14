---
name: ag-kamera-kesfi
description: Agdaki WiFi kameralari bul, RTSP yollarini kesfet, ONVIF sorgula, marka/model tespit et
---

# Ağ Kamera Keşfi

## Ne Zaman Kullanılır
Kullanıcı ev/ofis ağındaki IP kameraları bulmak, RTSP akış adresini öğrenmek, kamera markasını/modelini tespit etmek istediğinde.

## Adımlar

### 1. Ağı ve Kendi IP'ni Bul
```bash
ipconfig | grep "IPv4"
# Veya:
arp -a
```

Ana ağ genelde default gateway'in olduğu subnet'tir (örn. 192.168.0.0/24).

### 2. Ağdaki Tüm Cihazları Tara
```bash
nmap -sn 192.168.0.0/24 --exclude <kendi_ipn> -T5
```

### 3. Kamera Olabilecek Cihazlarda Port Tara
Kamera genelde şu portları açar:
- **80/tcp** — HTTP web arayüzü
- **554/tcp** — RTSP video akışı
- **443/tcp** — HTTPS
- **8080/tcp** — Alternatif HTTP
- **8554/tcp** — Alternatif RTSP
- **3702/tcp** — ONVIF discovery

```bash
nmap -p 80,554,443,8080,8554,3702 <ip> -T5
```

### 4. MAC Adresinden Marka/Model Tespit Et
nmap çıktısında MAC adresi satırı markayı gösterir:
```
MAC Address: E0:BA:AD:17:B1:84 (Hangzhou Hikvision Digital Technology)
```

Yaygın MAC önekleri:
- `E0:BA:AD` veya `00:01:8C` — **Hikvision**
- `78:2B:46` veya `AC:CC:8C` — **Dahua**
- `48:22:54` — **TP-Link Tapo**
- `F4:C7:AA` — **EZVIZ**
- `34:C0:59` — **Xiaomi**
- `00:12:47` — **Axis Communications**

### 5. RTSP Yollarını Dene

Markaya göre yaygın RTSP yolları:

**Hikvision:**
- `rtsp://IP:554/Streaming/Channels/101` (ana akış)
- `rtsp://IP:554/Streaming/Channels/102` (alt akış)
- `rtsp://IP:554/h264/ch1/main/av_stream`
- `rtsp://IP:554/live/ch00_0`

**Dahua:**
- `rtsp://IP:554/cam/realmonitor?channel=1&subtype=0`
- `rtsp://IP:554/live/ch00_0`
- `rtsp://IP:554/onvif1`

**TP-Link Tapo:**
- `rtsp://IP:554/stream1`
- `rtsp://IP:554/stream2`

**Xiaomi:**
- `rtsp://IP:554/live/ch00_0`
- `rtsp://IP:554/mjpg/1/video.mjpg`

**Generic/ONVIF:**
- `rtsp://IP:554/onvif/media`
- `rtsp://IP:554/video1`
- `rtsp://IP:554/cam1`
- `rtsp://IP:554/live`

### 6. RTSP Test (FFmpeg ile)
```bash
ffmpeg -rtsp_transport tcp -i "rtsp://IP:554/yol" -t 1 -f null - 2>&1 | grep "Duration\|Stream #0"
```

### 7. Kullanıcı Adı/Şifre Dene
Kamera varsayılan giriş bilgileri (markaya göre değişir):

| Marka | Kullanıcı | Şifre |
|-------|-----------|-------|
| Hikvision | admin | 12345 |
| Hikvision | admin | admin |
| Dahua | admin | admin |
| TP-Link | admin | admin |
| Xiaomi | admin | (boş) |
| EZVIZ | admin | 123456 |
| Generic | admin | 123456 / admin / password / 666666 / 888888 |

```bash
ffmpeg -rtsp_transport tcp -i "rtsp://kullanici:sifre@IP:554/path" -t 1 -f null - 2>&1
```

### 7b. Şifre Bulunamazsa — Kapsamlı Brute-Force
Seri numarası, MAC son 6 hane, marka adı gibi değerlerden türetilmiş şifreleri dene:
```bash
# Tum kombinasyonlar
for user in "admin" "Admin" "root" "administrator"; do
  for pass in "" "12345" "admin" "123456" "password" "pass" "111111" "000000" "888888" "666666" "1234" "4321" "EZVIZ" "ezviz" "$SERI_NO" "$MAC_SON6"; do
    code=$(curl -s -o /dev/null -w "%{http_code}" -u "$user:$pass" -m 2 "http://IP/onvif/device_service" 2>/dev/null)
    [ "$code" != "401" ] && [ "$code" != "000" ] && echo "✅ $user:$pass -> HTTP $code"
  done
done
```

### 7c. Son Çare — Fabrika Reset
Kameranın üzerindeki reset düğmesine (ataç/uçlu kalemle) 10-15 saniye basılır. Fabrika ayarlarına döner. Genelde kullanıcı `admin`, şifre boş veya `12345` olur.

### 8. Web Arayüzünü ve ONVIF'i Sorgula
Kamera web arayüzü varsa marka-specific API dene:
```bash
# Hikvision ISAPI
curl -s http://admin:sifre@IP/ISAPI/System/deviceInfo

# Dahua CGI
curl -s http://admin:sifre@IP/cgi-bin/magicBox.cgi?action=getSystemInfo

# ONVIF (auth gerektirir)
curl -s http://IP/onvif/device_service -X POST \
  -H "Content-Type: application/soap+xml" \
  -d '<?xml version="1.0"?>
   <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope">
    <s:Body>
     <GetDeviceInformation xmlns="http://www.onvif.org/ver10/device/wsdl"/>
    </s:Body>
   </s:Envelope>'
```

## Pitfall'lar
- Bazı kameralar RTSP'yi default devre dışı bırakır, web arayüzünden aktifleştirmek gerekir
- Hikvision kameralarda ONVIF auth zorunludur
- Varsayılan şifre değiştirilmişse sıfırlamak için kamera üzerindeki reset düğmesine 10sn basılır (fabrika ayarları)
- RTSP auth digest veya basic olabilir; FFmpeg ikisini de dener
- Windows'ta ping sweep çok yavaştır, nmap tercih edilir
- Kamera üzerinde "CODE:" etiketi varsa, yanındaki kod ŞİFRE değildir — genelde seri no/aktivasyon kodudur. Şifre ayrı bir ayardır.
- Kullanıcının masaüstünde Python projeleri varsa, içlerinde rtsp:// veya camera password bilgisi olabilir — tara: `grep -ril "rtsp://\\|kamera.*sifre\\|camera.*password" *.py`
- Generic/XCLYCM tipi kameralarda HTTP web arayüzü 404 dönebilir, bu normaldir — ONVIF ve RTSP portlarına odaklan
- Boş şifre (`admin:@`) genelde çalışmaz çünkü kullanıcı kurulumda şifre belirlemiştir, reset gerekebilir
- HTTP snapshot endpoint'leri 401 döndüyse auth gerektiriyordur — RTSP de auth gerektirecek demektir, doğrudan reset düşün
- **Hikvision Firmware 5.x+ kritik tuzak:** Tüm HTTP endpoint'leri 404 döner, varsayılan şifrelerin hiçbiri çalışmaz, ONVIF auth zorunludur, CVE'ler (2017-7921, 2021-36260) 405 Method Not Allowed döner. Bu bir güvenlik özelliğidir — kamera kilitlidir. Brute-force zaman kaybıdır. Çözüm: fiziksel reset, SADP tool veya Hik-Connect uygulaması. Detaylı rehber: `references/hikvision-firmware5-bypass.md`
- SADP tool kurulumu: ZIP indir → çıkar → Sağ tık Yönetici olarak çalıştır → Npcap kurulumunu onayla. Doğrudan terminal'den `.exe` çalıştırmak sessiz kurulum gerektirir (`/VERYSILENT`) ve genelde başarısız olur — elle kurmak daha güvenilir.

### Web Arayüzü 404 Dönen Kameralar İçin HTTP Endpoint Tarama
Kamera web arayüzü 404 dönüyorsa şu endpoint'leri dene:
```bash
endpoints=("/" "/index.html" "/login.html" "/en/index.asp" "/doc/page/login.asp" "/web/"
           "/snapshot" "/image" "/img/snapshot" "/capture" "/cgi-bin/snapshot.cgi"
           "/cgi-bin/image.cgi" "/tmpfs/snap.jpg" "/onvif/snapshot"
           "/Streaming/channels/1/preview")
for ep in "${endpoints[@]}"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -m 3 "http://IP$ep" 2>/dev/null)
  echo "$ep -> $code"
done
```

Ayrıca HTTP header ile banner grab yap (Server alanı markayı gösterebilir):
```bash
curl -s -I -m 3 "http://IP/" 2>/dev/null | head -15
```

### nmap Yoksa Powershell ile Hızlı ARP Taraması
```powershell
powershell.exe -Command '
$subnet = "192.168.0"
1..254 | ForEach-Object {
    $ip = "$subnet.$_"
    $ping = (New-Object System.Net.NetworkInformation.Ping).Send($ip, 100)
    if ($ping.Status -eq "Success") { Write-Output $ip }
}'
```

### Bilinen ONVIF SOAP Sorguları (Auth Gerektirir)
```bash
# Cihaz bilgisi
curl -s -u "admin:sifre" "http://IP/onvif/device_service" -X POST \
  -H "Content-Type: application/soap+xml" \
  -d '<?xml version="1.0"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope">
  <s:Body>
    <GetDeviceInformation xmlns="http://www.onvif.org/ver10/device/wsdl"/>
  </s:Body>
</s:Envelope>'

# Medya profilleri (RTSP URL'lerini verir)
curl -s -u "admin:sifre" "http://IP/onvif/media_service" -X POST \
  -H "Content-Type: application/soap+xml" \
  -d '<?xml version="1.0"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope">
  <s:Body>
## Kullanıcı Sorma Kuralı
- Servis durumu (çalışıyor mu, port açık mı, Chrome açık mı) gibi şeyleri sorma — direkt kontrol et
- Sadece karar gerektiren durumlarda sor (reset atalım mı, Chrome açalım mı)
- "Bana sorma bu bir kazanım" tarzı bir uyarı aldığında, hemen skill'e ekle ve bir daha aynı şeyi sorma

## Referans Dosyaları
- `references/telefon-osint-notlari.md` — Telefon numarasından OSINT, veri sızıntısı kontrolleri, yasal araçlar

## Google Arama ile Şifre Bulma Stratejisi
Kamera markası biliniyor ama şifre bulunamıyorsa:
1. Önce `"<marka_adı>" default password admin` ile ara
2. Bulunamazsa `"<marka_adı>" camera rtsp stream default password` dene
3. Hala yoksa `<marka_adı> camera wifi app download` ile uygulama adını bul
4. Uygulama adını bulunca `"<uygulama_adı>" rtsp password` veya `"<uygulama_adı>" local access password` ara
5. Kullanıcı telefonunda hangi uygulamayı kullandığını bilmiyorsa, uygulama adını sor

## Kullanıcının Python Projelerinde Şifre Arama
Kullanıcının bilgisayarındaki Python projelerinde camera password bilgisi olabilir:
```bash
# Desktop'taki .py dosyalarinda rtsp:// ara
grep -ril "rtsp://" /c/Users/eymen/Desktop/*.py 2>/dev/null

# 'kamera' veya 'camera' gecen dosyalari bul
grep -rilE "kamera|camera|rtsp" /c/Users/eymen/Desktop/*.py 2>/dev/null

# 'password' veya 'sifre' icerenleri tara
grep -rilE "password|sifre|şifre|passwd" /c/Users/eymen/Desktop/*.py 2>/dev/null
```

## Bilinen Markalar ve Default Şifreleri (Ek)
| Marka | Kullanıcı | Şifre | Not |
|-------|-----------|-------|-----|
| XCLYCM | admin | (kullanıcı tarafından belirlenir) | Generic Çin kamerası, reset gerekir |
| XCLYCM | admin | EZVİZ/EZVIZ/ezviz (dene) | Bazı modeller EZVIZ klonu olabilir |
| CloudEdge | admin | (uygulamada belirlenir) | Uygulama üzerinden RTSP ayarı |
| V380 | admin | (uygulamada belirlenir) | Uygulama içinde RTSP şifresi bölümü |

## Kullanıcının Kamera Uygulamasından Bilgi Alma
Kullanıcı kamera markasını söyler veya "CODE:" etiketindeki kodu verirse:
1. CODE etiketindeki kod genelde şifre DEĞİL, seri numarası veya aktivasyon kodudur
2. Kullanıcının telefonunda hangi uygulama olduğunu bul (CloudEdge, XCLYCM, V380, XMEye, EseeCloud)
3. Uygulama içinde "RTSP Ayarları", "Yerel Erişim", "Network Settings", "Stream URL" bölümlerine bakmasını söyle
4. Uygulama adı verilmezse web'den ara: `"<marka>" camera app android`

## Kullanıcı Sorma Kuralı
- Servis durumu (çalışıyor mu, port açık mı, Chrome açık mı) gibi şeyleri sorma — direkt kontrol et
- Sadece karar gerektiren durumlarda sor (reset atalım mı, Chrome açalım mı)
- "Bana sorma bu bir kazanım" tarzı bir uyarı aldığında, hemen skill'e ekle ve bir daha aynı şeyi sorma
