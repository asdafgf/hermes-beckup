# WiFi Ağı Taraması — Referans

Windows 11'de WiFi ağındaki cihazları (IP + MAC) bulmak için çalışan desen.

## Çalışan Yaklaşım

### WiFi IP'yi Bulma (En Güvenilir Yöntem)

PowerShell üzerinden doğrudan WiFi arayüzünü sorgula:

```python
import subprocess, re

def get_wifi_ip():
    ps_cmd = [
        "powershell.exe", "-Command",
        'Get-CimInstance Win32_NetworkAdapter -Filter \'NetEnabled=True AND Name LIKE "%%Wi-Fi%%"\' | '
        'Get-CimAssociatedInstance -ResultClassName Win32_NetworkAdapterConfiguration | '
        'Select-Object IPAddress, IPSubnet | Format-List'
    ]
    r = subprocess.run(ps_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=10)
    ip = re.search(r'IPAddress\s*:\s*\{([0-9.]+)', r.stdout)
    subnet = re.search(r'IPSubnet\s*:\s*\{([0.9]+)', r.stdout)
    return ip.group(1) if ip else None
```

**Fallback:** `ipconfig` çıktısında `192.168.x.x` olan IPv4 adresini bul.

### ARP Tablosundan Cihaz Listeleme

```python
def get_arp_devices():
    r = subprocess.run(["arp", "-a"], capture_output=True, text=True, encoding="utf-8", errors="ignore")
    devices = {}
    for line in r.stdout.splitlines():
        m = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F]{2}[-:][0-9a-fA-F]{2}[-:][0-9a-fA-F]{2}[-:][0-9a-fA-F]{2}[-:][0-9a-fA-F]{2}[-:][0-9a-fA-F]{2})", line)
        if m:
            ip, mac = m.group(1), m.group(2).replace('-', ':')
            if ip.startswith("192.") or ip.startswith("10."):
                devices[ip] = mac
    return devices
```

**Önemli:** Multicast (224.x.x.x, 239.x.x.x) ve broadcast (ff-ff-ff-ff-ff-ff) adreslerini filtrele.

### Aktif Tarama (Ping + ARP)

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping_host(ip):
    try:
        r = subprocess.run(["ping", "-n", "1", "-w", "300", ip], capture_output=True, timeout=2)
        return r.returncode == 0
    except:
        return False

def scan(base_ip, my_ip):
    hosts = [f"{base_ip}.{i}" for i in range(1, 255)]
    active = set()
    with ThreadPoolExecutor(max_workers=50) as ex:
        fut = {ex.submit(ping_host, ip): ip for ip in hosts}
        for f in as_completed(fut):
            if f.result():
                active.add(fut[f])
    return active
```

## Zorluklar ve Çözümleri

| Sorun | Çözüm |
|---|---|
| ipconfig'de yanlış arayüz (VirtualBox) | PowerShell WMI sorgusu ile sadece Wi-Fi arayüzünü hedefle |
| ARP tablosu boş | `arp -d *` ile önbelleği temizle, sonra ping ata (ARP kaydı oluşur) |
| Ping'e yanıt yok (güvenlik duvarı) | Sadece ARP tablosuna güven, multicast/broadcast'leri filtrele |
| MAC formatı tireli | `.replace('-', ':')` ile normalleştir |
| Türkçe Windows | `encoding="utf-8", errors="ignore"` ile hem Türkçe hem İngilizce çalışır |

## Örnek Çıktı (Temiz)

```
IP: 192.168.0.1    MAC: 98:f2:17:02:03:4f    🌐 MODEM
IP: 192.168.0.17   MAC: e0:ba:ad:17:b1:84    📱 CİHAZ
IP: 192.168.0.18   MAC: 56:52:a4:bd:51:54    📱 CİHAZ
```

## Önemli Uyarı

- `ThreadPoolProcessor` diye bir sınıf yok — doğrusu `ThreadPoolExecutor` (`concurrent.futures`).
- Ping timeout 100ms çok kısa, 300ms kullan.
- `encoding="cp857"` yanlış — `utf-8` kullan, hata alırsan `cp857` dene.
- ARP regex'inde `dinamik/statik` kontrolü yapma — tüm satırı yakala, sonra filtrele.
