---
name: hermes-gemini-copilot
title: Hermes ↔ Gemini otonom hata çözüm döngüsü (3-2-1 kuralı)
description: Hermes sorunu kendi çözmeye çalışır (2 deneme), çözemezse Chrome'daki Gemini sohbetine hatayı gönderir, Gemini'nin kodunu alır, VS Code projesine yazar, çalıştırır, çıktıyı Gemini'ye verir. Çözüm bulunana kadar döngü. Otomatik, kullanıcıya sormaz.
category: software-development
---
# Hermes ↔ Gemini Otonom Hata Çözüm Döngüsü

## 3-2-1 Kuralı (Eymen tercihi)

| Aşama | Ne yapılır |
|---|---|
| **1. deneme** | Kendi çözümünü dene (terminal, web_search, bildiğin yöntem) |
| **2. deneme** | Farklı bir yaklaşım dene |
| **3. deneme** | 🚨 Gemini'ye bağlan, sorunu tam metin yaz |
| **Kod geldi** | VS Code yeni proje aç → kopyala → kaydet → kullanıcı terminalde görsün |
| **Çıktı** | Kullanıcı VS Code terminalinde görür + ben de okuyup Gemini'ye veririm |
| **Döngü** | Çözüm bulunana kadar devam |

**Kesin kural 1:** Kullanıcıya sorma. Otomatik yürüt.
**Kesin kural 2:** VS Code açık mı kontrol et (`ps aux | grep code`) — açıksa yenisini açma, mevcut terminali kullan.
**Kesin kural 3:** Kodu ben çalıştırıp çıktısını Gemini'ye vermek yerine, kullanıcının VS Code terminalinde görmesini sağla. Ben çıktıyı ayrıca alıp Gemini'ye veririm.
**Kesin kural 4:** Her seferinde **yeni bir VS Code projesi** aç. Kullanıcı "yeni proje" bekler. Klasör adı her seferinde farklı olsun (örn. `ag-tarama`, `network-scan-v2`).
**Kesin kural 5:** Kullanıcıya ▶ **Run butonunu** (yeşil oynatma) veya `Ctrl+F5` kullanmasını söyle. Terminal komutu yazdırma yerine VS Code'un kendi run mekanizmasını kullan.

## Ne Zaman Kullanılır

- Bir Python script'i veya terminal komutu hata verdiğinde ve çözüm bulunamadığında
- Kullanıcı "şu işi yapan bir Python kodu yaz" dediğinde (ilk kodu Hermes yazar, hata alırsa Gemini'ye geçer)
- Herhangi bir sistem/ağ/Python sorunu çözülmesi gerektiğinde

## Mimari

```
Hermes (ana)
  ├── 1. deneme → kendi çöz
  ├── 2. deneme → farklı çözüm dene
  ├── 3. deneme →
  │     Chrome/Gemini sohbetine sorunu yaz (CDP + Playwright)
  │     Gemini'nin kod cevabını oku (CDP)
  │     Kodu VS Code projesine yaz (write_file)
  │     Kullanıcıya VS Code'da ▶ Run yapmasını söyle
  │     Kullanıcı çıktıyı görsün
  │     Ben çıktıyı okuyup Gemini'ye geribildirim yap
  └── Çözüm → bildir
```

## Ön koşullar

- **Chrome** Scoop ile kurulu: `/c/Users/eymen/scoop/apps/googlechrome/148.0.7778.97/chrome.exe`
- **Playwright** Anaconda Python'da: `/c/Users/eymen/anaconda3/python.exe` ile `import playwright` çalışıyor
- **CDP port 9222** — açık değilse Chrome'u öldürüp yeniden başlat
- **VS Code** PATH'te: `code` komutu çalışıyor

### VS Code açık mı kontrol et (Kesin Kural 2'nin uygulanışı)

```bash
# VS Code process var mı?
ps aux | grep -i code | grep -v grep | wc -l
# 0 ise → yenisini aç
# 1+ ise → mevcut olanı kullan, yenisini açma
```

## Adımlar (detaylı)

### A. Gemini'ye sorunu yaz

Gemini chat'ine şu formatta yaz:
```
[SORUN]
Hedef: <ne yapılmak isteniyor>
Ortam: Windows 11, Python
Hata: <hata mesajı - tam metin>
Denenen: <1. denemede ne oldu>, <2. denemede ne oldu>
Bana Python kodu ver, açıklama ekleme.
```

Gönderme kodu (Playwright CDP):
```python
/c/Users/eymen/anaconda3/python.exe -c "
import asyncio
from playwright.async_api import async_playwright

async def send(msg):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        ctx = browser.contexts[0]
        page = next((p for p in ctx.pages if 'gemini' in p.url), None)
        if not page: return
        await page.wait_for_timeout(2000)
        sel = 'div[contenteditable=\"true\"]'
        await page.wait_for_selector(sel, timeout=10000)
        await page.click(sel)
        await page.fill(sel, '')
        await page.type(sel, msg, delay=15)
        await page.keyboard.press('Enter')
        print('✅ Gönderildi')

asyncio.run(send('MESAJ'))
"
```

### B. Gemini'nin cevabını oku (10-12sn bekle)

```python
/c/Users/eymen/anaconda3/python.exe -c "
import asyncio
from playwright.async_api import async_playwright

async def read():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        ctx = browser.contexts[0]
        page = next((p for p in ctx.pages if 'gemini' in p.url), None)
        if not page: return
        await page.wait_for_timeout(12000)
        blocks = await page.evaluate('''
            () => {
                const b = document.querySelectorAll('pre code, div.code-block, pre');
                return Array.from(b).map(x => x.textContent.trim()).filter(t => t.length > 50);
            }
        ''')
        if blocks:
            print(f'{len(blocks)} kod blogu')
            for i, code in enumerate(blocks[-3:]):
                print(f'--- KOD {i+1} ---')
                print(code[:4000])
        else:
            txt = await page.evaluate('() => document.body.innerText')
            print(txt[:2000])

asyncio.run(read())
"
```

**NOT:** Bu script zaten `scripts/read_gemini_code.py` olarak kayıtlı:
```bash
/c/Users/eymen/anaconda3/python.exe /c/Users/eymen/AppData/Local/hermes/skills/software-development/hermes-gemini-copilot/scripts/read_gemini_code.py 12
```

### C. Kodu VS Code'da yeni proje olarak hazırla (KRİTİK)

> **Bu adım atlanamaz.** Kullanıcı kodun çalıştığını **kendi VS Code'unda** görmek ister.

1. **VS Code process kontrolü:**
   ```bash
   ps aux | grep -i code | grep -v grep | wc -l
   ```
   - 0 ise → `code C:\Users\eymen\Desktop\<yeni-proje-adi>` ile yeni aç
   - 1+ ise → mevcut VS Code'u kullan, **yeniden açma**

2. **Yeni proje klasörü oluştur:**
   ```bash
   mkdir -p /c/Users/eymen/Desktop/<yeni-proje-adi>
   ```
   Her seferinde farklı isim (örn. `ag-tarama`, `network-scan-v2`)

3. **Kodu write_file ile yaz:**

4. **Kullanıcıya adım adım talimat ver:**
   - ▶ **Run butonu** (sağ üst, yeşil oynatma) veya `Ctrl+F5`
   - Alternatif: sağ tık → **Run Python File in Terminal**
   - Alternatif: sol tıkla dosyayı seç, üst menüden Run → Run Without Debugging

5. **Çıktıyı VS Code terminalinde görmesini bekle**

6. **Çıktıyı oku** (ben terminal command ile çalıştırırım) → Gemini'ye geribildirim

**YANLIŞ (bu oturumda yapılan hata):**
- Kodu yazıp ben terminalde çalıştırdım, çıktıyı kullanıcı görmedi
- VS Code'u her adımda kapatıp açtım
- Terminal komutu yazdırdım, ▶ Run kullanmadım

**DOĞRU:**
- Kodu VS Code projesine yaz
- Kullanıcıya ▶ Run yapmasını söyle
- Bekle, çıktıyı VS Code terminalinde görsün
- Sonra ben çıktıyı alıp Gemini'ye gönder

### D. Çıktıyı oku + Gemini'ye geribildirim

Kullanıcı çıktıyı gördükten sonra, ben de terminal'den çalıştırıp çıktıyı alırım:
```bash
cd /c/Users/eymen/Desktop/<proje-adi>
/c/Users/eymen/anaconda3/python.exe main.py 2>&1
```

Bu çıktıyı Gemini'ye gönder:
```
VERDİĞİN KOD ŞU ÇIKTIYI VERDİ:
<çıktının tamamı>

Düzeltilmiş kodu ver, sadece kod.
```

Sonra B'ye dön, yeni kodu oku.

## Chrome'u CDP modunda başlatma (kapalıysa)

```bash
# 1. Öldür
taskkill //F //IM chrome.exe 2>/dev/null; sleep 3

# 2. Background'da başlat (yeni profil, varsayılanı bozmaz)
terminal(background=true) komutuyla:
"/c/Users/eymen/scoop/apps/googlechrome/148.0.7778.97/chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:/Users/eymen/AppData/Local/Google/Chrome/CDPProfile" "https://gemini.google.com/app"

# 3. CDP'nin açılmasını bekle
for i in 1..10; do
  curl -s http://localhost:9222/json/version | python -c "import sys,json; print(json.load(sys.stdin).get('Browser',''))"
  if [ -n "$result" ]; then break; fi
  sleep 3
done
```

## Bilinen tuzaklar

1. **PATH karışıklığı:** `python` komutu Hermes venv'ini gösterir, orada playwright YOK. Her zaman **tam yol** kullan: `/c/Users/eymen/anaconda3/python.exe`

2. **type() timeout:** Gemini'nin React input'u sadece Playwright `fill()` + `type()` ile çalışır. `delay=15-20` kullan, daha yüksek yavaş kalır.

3. **Chrome intro sayfası:** Chrome `--remote-debugging-port` ile açılınca bazen `chrome://intro/` sayfasında kalır. Gemini açılmazsa CDP WebSocket ile `Page.navigate` yap:
   ```python
   import asyncio, json, websockets, requests
   tabs = requests.get("http://localhost:9222/json").json()
   intro = [t for t in tabs if 'intro' in t["url"]][0]
   ws_url = intro["webSocketDebuggerUrl"]
   async with websockets.connect(ws_url) as ws:
       cmd = json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://gemini.google.com/app"}})
       await ws.send(cmd)
       await ws.recv()
   ```

4. **Timeout:** Tarama gibi uzun işlemlerde timeout değerini 120sn yap. Yetmezse background'da çalıştır.

5. **Birden çok kod bloğu:** Gemini bazen aynı kodu 3 kere yazar. Son bloğu al, birinciyle aynıysa fark etmez.

6. **VS Code'u tekrar tekrar açma:** Her adımda `code .` ile yeni pencere açma. Önce process var mı kontrol et (`ps aux | grep code`).

## Başarıyla test edilen senaryolar

Ayrıntılar: `skill_view('hermes-gemini-copilot', 'references/chrome-cdp-profile.md')` — Chrome CDP profil yönetimi ve intro sayfası navigasyonu.

### 13 May 2026 — WiFi ağ taraması (full loop testi ✅)
- **Hedef:** WiFi'daki cihazların IP + MAC adreslerini bul
- **1. deneme:** SendARP ile tarama → sadece 1 cihaz buldu (192.168.37.x subnet'teydi)
- **2. deneme:** Aynı kod geliştirilmiş hali → GERÇEK ağ (192.168.0.x) bulundu, 6 cihaz ✅
- **Sonuç:** Modem, bilgisayar, Hikvision kamera, 3 bilinmeyen cihaz
- **Kod:** `/c/Users/eymen/Desktop/network-scan/scanner2.py`

### Önceki test — WiFi tarama (5 cihaz)
- Gemini'den ping+ARP+threading kodu, 5 cihaz tespit edildi
- GitHub repo: https://github.com/asdafgf/hermes-gemini-copilot
