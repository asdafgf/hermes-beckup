# Chrome CDP ile Claude.ai Web Erişimi

## Ne Zaman Kullanılır
Gemini API görsel analizde tutarsız sonuç verdiğinde, Claude.ai web'de manuel analiz yapmak için Chrome CDP üzerinden giriş yapılır.

## Chrome Yolu (Bu Makinede)
```
C:\Users\eymen\scoop\apps\googlechrome\148.0.7778.97\chrome.exe
```

## Chrome'u CDP Modunda Başlatma

```bash
# Arka planda başlat
"/c/Users/eymen/scoop/apps/googlechrome/148.0.7778.97/chrome.exe" \
  --remote-debugging-port=9222 \
  --user-data-dir="C:\Users\eymen\.chrome-claude" \
  "https://claude.ai"
```

## CDP Kontrolü (Python + websockets)

Chrome `localhost:9222`'de dinlerken:

### 1. Mevcut sekmeleri listele
```python
import requests, json
tabs = requests.get("http://localhost:9222/json").json()
for t in tabs:
    print(t['title'], t['url'], t['id'])
```

### 2. Yeni sekme aç
```python
# GET /json/new?url=<URL> ile yeni sekme
tab = requests.get("http://localhost:9222/json/new?url=https://claude.ai").json()
ws_url = tab['webSocketDebuggerUrl']
```

### 3. JavaScript çalıştır (WebSocket üzerinden)
```python
import asyncio, websockets, json

async def eval_js(ws_url, js_code):
    async with websockets.connect(ws_url, max_size=10*1024*1024) as ws:
        await ws.send(json.dumps({
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": js_code}
        }))
        await asyncio.sleep(2)
        resp = await ws.recv()
        return json.loads(resp)

# Sayfa içeriğini al
result = asyncio.run(eval_js(ws_url, "document.body.innerText.substring(0,3000)"))
```

## Sınırlamalar

1. **Claude.ai giriş sayfası JavaScript ile render ediliyor.** Basit DOM sorguları sonuç vermeyebilir.
2. **"Continue with email" butonu** — CDP ile `.click()` yapılsa bile sayfa state'i değişmeyebilir (React render cycle).
3. **Şifre girişi** — kullanıcının manuel müdahalesi gerekir.
4. **Chrome'da oturum açma ekranı** — `--user-data-dir` yeni profil oluşturduğu için ilk açılışta Chrome girişi isteyebilir.

## Çözüm Önerisi

CDP otomasyonu sınırlı olduğu için:
1. Chrome'u arka planda başlat
2. Kullanıcıya "Chrome açıldı, Claude.ai'ye giriş yap" diye bildir
3. Kullanıcı giriş yapınca CDP ile sayfayı kontrol etmeye devam et

## Alternatif: Agent Browser Kurulumu

```bash
# Playwright ile chromium yüklemeyi dene
pip install playwright
playwright install chromium

# Sonra Hermes browser tool'unu chromium path ile yapılandır
# config.yaml: browser.executable_path: /path/to/chromium
```
