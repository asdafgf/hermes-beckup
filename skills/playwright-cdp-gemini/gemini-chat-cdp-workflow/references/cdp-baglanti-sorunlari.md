# CDP Bağlantı Sorunları ve Çözümleri

Bu referans dosyası, Gemini Chat CDP workflow sırasında karşılaşılan bağlantı sorunlarını ve çözümlerini içerir.

## Chrome CDP portu açılmıyor

### Belirti
- `curl -s http://localhost:9222/json/version` boş döner
- `for` döngüsü 10 denemede port açılmaz

### Çözümler (sırayla dene)

1. **Chrome process'lerini tamamen öldür:**
   ```bash
   taskkill //F //IM chrome.exe 2>/dev/null
   sleep 3
   ```
   Chrome'un birden çok process'i olabilir (12+ tane). hepsini öldürmek için `//F` zorunlu.

2. **Yeni user-data-dir ile başlat:**
   ```bash
   "/c/Users/eymen/scoop/apps/googlechrome/148.0.7778.97/chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:/Users/eymen/AppData/Local/Google/Chrome/CDPProfile" "https://gemini.google.com/app"
   ```
   Varsayılan profil bozulmuş olabilir. Yeni profil ile dene.

3. **Scoop shim yerine direkt exe kullan:**
   `chrome` (scoop shim) yerine direkt tam yol:
   `/c/Users/eymen/scoop/apps/googlechrome/148.0.7778.97/chrome.exe`

4. **Chrome başlatıldı mı kontrol et:**
   ```bash
   ps aux | grep -i chrome | grep -v grep
   ```
   Process var ama port yoksa → flag'ler iletilmemiştir. Kapat, yeniden dene.

## Gemini sayfası chrome://intro/ açılıyor

### Belirti
- Chrome açılır ama `chrome://intro/` sayfasında kalır
- Gemini URL'i yüklenmez

### Çözüm
CDP WebSocket ile manuel yönlendir:
```python
import requests, json, asyncio, websockets

tabs = requests.get("http://localhost:9222/json").json()
intro = [t for t in tabs if 'intro' in t["url"]][0]
ws_url = intro["webSocketDebuggerUrl"]

async def navigate():
    async with websockets.connect(ws_url) as ws:
        cmd = json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": "https://gemini.google.com/app"}})
        await ws.send(cmd)
        await ws.recv()
        print("✅ Yönlendirildi")

asyncio.run(navigate())
```

## Playwright bağlanamıyor

### Belirti
- `connect_over_cdp('http://localhost:9222')` hata verir

### Çözüm
- CDP portunun açık olduğundan emin ol (`curl http://localhost:9222/json/version`)
- Anaconda Python kullan (`/c/Users/eymen/anaconda3/python.exe`), Hermes venv'inde playwright yok
- CDP versiyonunu kontrol et (`/json/version` dönen Browser sürümü)

## Gemini input kutusu bulunamıyor

### Belirti
- `wait_for_selector('div[contenteditable="true"]')` timeout

### Çözüm
- Sayfanın tamamen yüklendiğinden emin ol (`wait_for_timeout(5000)`)
- Gemini UI güncellenmiş olabilir, selector'ı güncelle
- Alternatif selector dene: `textarea`, `[contenteditable]`, `.input-area`
