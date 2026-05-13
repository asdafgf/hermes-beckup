---
name: gemini-chat-cdp-workflow
description: "Chrome CDP + Playwright ile Gemini'ye mesaj gönderme. Chrome'u --remote-debugging-port=9222 ile başlatır, Gemini'yi açar, mesaj yazar ve Enter'a basar."
---
# Gemini Chat — CDP Workflow

## Ne işe yarar
Chrome'u CDP modunda başlatıp Gemini sohbetine Playwright ile mesaj gönderme. Her seferinde temiz ve garantili çalışan adımlar.

## Ön koşullar
- Chrome Scoop ile kurulu: `/c/Users/eymen/scoop/apps/googlechrome/148.0.7778.97/chrome.exe`
- Playwright Anaconda Python'da kurulu: `python -c "import playwright"`
- CDP port 9222 boşta (değilse eski Chrome'ları öldür)

## Adımlar (sırayla uygula)

### 1. Mevcut Chrome process'lerini öldür
```bash
taskkill //F //IM chrome.exe 2>/dev/null; sleep 3
```

### 2. Chrome'u CDP modunda background'da başlat
```bash
# Background + yenı data dir ile (varsayılan profili bozmamak için)
"/c/Users/eymen/scoop/apps/googlechrome/148.0.7778.97/chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:/Users/eymen/AppData/Local/Google/Chrome/CDPProfile" "https://gemini.google.com/app"
```
**NOT:** `terminal(background=true)` ile çalıştır.

### 3. CDP portunun açılmasını bekle
```bash
for i in 1..10; do
  curl -s http://localhost:9222/json/version | python -c "import sys,json; print(json.load(sys.stdin).get('Browser',''))"
  if [ -n "$result" ]; then break; fi
  sleep 3
done
```

### 4. Chrome intro sayfasını Gemini'ye yönlendir (gerekirse)
Eğer `chrome://intro/` açıldıysa, CDP WebSocket ile `Page.navigate` yap:
```python
resp = requests.get("http://localhost:9222/json")
tabs = resp.json()
intro = [t for t in tabs if 'intro' in t["url"]][0]
# WebSocket üzerinden navigate
async with websockets.connect(intro["webSocketDebuggerUrl"]) as ws:
    cmd = json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": "https://gemini.google.com/app"}})
    await ws.send(cmd)
    await ws.recv()
```

### 5. Playwright ile mesaj gönder
```python
# Anaconda Python ile çalıştır (Hermes venv'inde playwright yok)
/c/Users/eymen/anaconda3/python.exe -c "
import asyncio
from playwright.async_api import async_playwright

async def send(msg):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        ctx = browser.contexts[0]
        page = next((p for p in ctx.pages if 'gemini' in p.url), None)
        if not page:
            print('❌ Gemini sekmesi yok')
            return
        await page.wait_for_timeout(3000)
        sel = 'div[contenteditable=\"true\"]'
        await page.wait_for_selector(sel, timeout=10000)
        await page.click(sel)
        await page.fill(sel, '')
        await page.type(sel, msg, delay=20)
        await page.keyboard.press('Enter')
        print(f'✅ Gönderildi: {msg}')

asyncio.run(send('MESAJ'))
"
```

## Bilinen tuzaklar
- **PATH karışıklığı:** Hermes venv'i (`source venv/Scripts/activate`) playwright'i görmez. Her zaman **Anaconda Python** (`/c/Users/eymen/anaconda3/python.exe`) kullan. `which python` Hermes venv'ini gösterir, onu ASLA kullanma.
- **Chrome --remote-debugging-port almıyorsa:** yeni bir `--user-data-dir` ile dene, varsayılan profili bozmamak için iyi de olur.
- **CDP açılmıyor:** `ps aux | grep chrome` ile process var mı kontrol et, `taskkill //F //IM chrome.exe` ile tamamen öldürüp yeniden başlat. Başlatırken `--user-data-dir` vermek CDP'nin daha güvenilir açılmasını sağlar.
- **Gemini sekmesi intro'da kalıyorsa:** `Page.navigate` CDP komutu ile elle yönlendir (bkz. Adım 4).
- **type() timeout:** delay=15-20 kullan, 50 çok yavaş kalıyor. Gemini'nin React input'u sadece Playwright `fill()` + `type()` ile çalışır (textContent + InputEvent işe yaramaz).
- **Birden çok kod bloğu:** Gemini aynı kodu 3 kere yazabilir. Son bloğu al, diğerleriyle aynıysa sorun yok.
