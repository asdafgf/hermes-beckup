---
name: cloudflare-browser-bypass
description: >-
  Cloudflare / Google bot korumasını, kullanıcının mevcut tarayıcı profiliyle (Chrome/Edge/Firefox)
  atlatma yöntemleri. Selenium, Playwright, undetected-chromedriver ile yaklaşımlar.
category: devops
---

# Cloudflare / Google Bot Koruması Atlatma

## Ne Zaman Kullanılır
- Replit, Google Drive, GitHub vb. siteler Cloudflare 403 veya Google bot tespiti döndürüyorsa
- `curl`, `requests`, `httpx` gibi HTTP kütüphaneleri bot korumasına takılıyorsa
- "Automated browser detected" hatası alınıyorsa

## Temel Strateji

**En önemli kural:** Mevcut tarayıcı profilini kullan (kullanıcının hesabı kayıtlı, çerezler duruyor). Yeni bir profil açmak bot tespitini tetikler.

## Yaklaşımlar (Sıralı)

### 1. Chrome Profili + Selenium / webdriver-manager
```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

CHROME_USER_DATA = r"C:\Users\eymen\AppData\Local\Google\Chrome\User Data"
CHROME_BINARY = r"C:\Users\eymen\scoop\apps\googlechrome\current\chrome.exe"

options = Options()
options.binary_location = CHROME_BINARY
options.add_argument(f"--user-data-dir={CHROME_USER_DATA}")
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
prefs = {
    "download.default_directory": r"C:\Users\eymen\runners-journey\downloads",
    "download.prompt_for_download": False,
    "safebrowsing.enabled": True,
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
```

**Pitfall — Chrome çakışması (SessionNotCreated):**
- Eğer Chrome zaten açıksa (`SessionNotCreatedException: session not created`), **tüm Chrome süreçlerini öldür** (`taskkill /F /IM chrome.exe`), `SingletonLock`/`SingletonSocket` dosyalarını temizle, yeniden dene
- Alternatif: Chrome'u `--remote-debugging-port=9333` ile background'da başlat, sonra `debugger_address` ile bağlan (ama bu GUI açmaz)
- exitCode=21 hatası: profil kilitli demektir
- **Windows tipi:** `FIN_WAIT_2`/`CLOSE_WAIT` portları 2-4 dk boyunca kullanımda kalır. `taskkill` sonrası bile yeni ChromeDriver bağlanamaz (`cannot connect to chrome at 127.0.0.1:XXXXX`). Çözüm: **farklı port kullan** (`--remote-debugging-port=9333`), veya `netstat` ile port kullanımını kontrol et

### 2. Firefox + Playwright (Yeni profil)
```python
import asyncio
from playwright.async_api import async_playwright

FIREFOX_PATH = r"C:\Users\eymen\scoop\apps\firefox\current\firefox.exe"
USER_DATA_DIR = r"C:\Users\eymen\AppData\Roaming\Mozilla\Firefox\Profiles\playwright"

async def main():
    async with async_playwright() as p:
        context = await p.firefox.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            executable_path=FIREFOX_PATH,
        )
        page = context.pages[0]
        await page.goto("https://drive.google.com")
        input("ENTER'a bas...")
        await context.close()

asyncio.run(main())
```

**Pitfall — Firefox exitCode=0 hemen kapanıyor / Playwright başlatamıyor:**
- Playwright'ın `-juggler-pipe` modu bazı Firefox sürümlerinde (v150+) çalışmaz — Firefox hemen `exitCode=0` ile kapanır
- `launch_persistent_context` hatası: `Failed to launch the browser process` + `<process did exit: exitCode=0>`
- **Çözüm:** Firefox'u doğrudan `subprocess.Popen` ile başlat, Playwright kullanma
- Firefox'un yeni profili (`Profiles/hermes_drive` gibi) ilk açılışta otomatik oluşur, önceden var olması gerekmez
- İlk açılışta Google hesabı yoktur — kullanıcının elle giriş yapması gerekir

**Pitfall — Telefondan elle indirme en hızlı çözüm:**  
Eğer bilgisayarda tüm otomasyon yöntemleri bot korumasına takılıyorsa (Chrome port kilitli, EdgeDriver DNS çözülmüyor, Firefox profili yok), en hızlı çözüm:
1. Kullanıcıya Drive linkini ver
2. Telefonunda Drive'ı açıp hesabına girsin
3. Dosyaya tıkla → İndir
4. Telegram/WhatsApp üzerinden dosyayı sana göndersin
5. Bilgisayarda alıp işleme devam et

### 3. Firefox Doğrudan (En basit)
```python
import subprocess

FIREFOX = r"C:\Users\eymen\scoop\apps\firefox\current\firefox.exe"
subprocess.Popen([
    FIREFOX, "-new-instance",
    "-profile", r"C:\Users\eymen\AppData\Roaming\Mozilla\Firefox\Profiles\hermes_drive",
    "https://drive.google.com"
], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
```

### 4. Edge Profili (Chrome altyapısı)
```python
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager

EDGE_USER_DATA = r"C:\Users\eymen\AppData\Local\Microsoft\Edge\User Data"
EDGE_BINARY = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

options = EdgeOptions()
options.binary_location = EDGE_BINARY
options.use_chromium = True
options.add_argument(f"--user-data-dir={EDGE_USER_DATA}")
options.add_argument("--profile-directory=Profile 6")
# ... aynı Chrome argümanları

driver = webdriver.Edge(
    service=EdgeService(EdgeChromiumDriverManager().install()),
    options=options
)
```

**Pitfall — EdgeDriver DNS hatası:**
- `msedgedriver.azureedge.net` çözülemezse → DNS sorunu
- Çözüm: ChromeDriver ile Chrome'u dene (Edge yerine), veya elle `edgedriver_win64.zip` indir
- Edge profilleri: `Default`, `Profile 2`, `Profile 4`, `Profile 5`, `Profile 6`

## Kurulum Ön Koşulları

```bash
# webdriver-manager (otomatik chromedriver yönetimi)
pip install webdriver-manager

# Playwright (tüm tarayıcılar için)
pip install playwright
playwright install chromium firefox

# undetected-chromedriver (Cloudflare spesifik)
pip install undetected-chromedriver
```

## Hata Kodları ve Çözümleri

| Hata | Sebep | Çözüm |
|------|-------|-------|
| `SessionNotCreatedException` | Chrome zaten açık | `taskkill /F /IM chrome.exe` + lock dosyalarını sil |
| `exitCode=21` | Profil kilitli | `SingletonLock`/`SingletonSocket` temizle |
| `exitCode=0` (hemen çıkış) | Firefox juggler-pipe sorunu | `subprocess.Popen` ile doğrudan başlat |
| DNS çözümleme hatası | `azureedge.net` çözülemiyor | ChromeDriver kullan (Edge yerine) |
| `ERR_CONNECTION_CLOSED` | Tarayıcı zaten çalışıyor | Tüm instance'ları öldür |

## Cloudflare 403 Spesifik

Eğer Cloudflare hala blokluyorsa (undetected-chromedriver bile yetmezse):
```python
import undetected_chromedriver as uc
driver = uc.Chrome(
    user_data_dir=r"C:\Users\eymen\AppData\Local\Google\Chrome\User Data",
    profile_directory="Default"
)
```
