# Chrome CDP Profil & Oturum Yönetimi

## Sorun
CDP ile Chrome başlatırken `--user-data-dir` parametresi ZORUNLU. Farklı profiller kullanmak oturum bilgilerini kaybettirir (Gemini'ye tekrar giriş gerekir).

## Profil seçenekleri

### 1. Yeni profil (CDPProfile) — Gemini oturumu yok
```bash
--user-data-dir="C:/Users/eymen/AppData/Local/Google/Chrome/CDPProfile"
```
- Artı: Varsayılan profili bozmaz
- Eksi: Gemini'ye giriş yapılmamış, "Oturum açın" ekranı gelir

### 2. Varsayılan profil (Default) — Gemini oturumu olabilir
```bash
--user-data-dir="C:/Users/eymen/AppData/Local/Google/Chrome/User Data/Default"
```
- Artı: Mevcut oturumlar korunur
- Eksi: Bazen hata alınır ("DevTools ... requires non-default"), Default kabul edilmez

### 3. User Data ana dizini (Tüm profiller)
```bash
--user-data-dir="C:/Users/eymen/AppData/Local/Google/Chrome/User Data"
```
- Artı: Tüm profilleri yükler, kullanıcının seçtiği profil açılır
- Eksi: Çoklu profil varsa hangisinin açılacağı belirsiz

## Çözüm

Normal kullanımda **CDPProfile** kullan, Gemini'ye giriş yapılmamışsa:
1. CDP'ye bağlan
2. `Page.navigate` ile gemini.google.com'a git
3. "Oturum açın" yazısını tespit et (DOM'da `link "Oturum açın"`)
4. Varsa → kullanıcıdan elle giriş yapmasını iste

Alternatif: `--user-data-dir="C:/Users/eymen/AppData/Local/Google/Chrome/User Data"` kullan.

## Chrome intro sayfası tuzağı
Chrome CDP modunda bazen `chrome://intro/` sayfasında kalır. CDP WebSocket ile yönlendir:
```python
import json, requests, asyncio, websockets
r = requests.get("http://localhost:9222/json")
tabs = r.json()
intro = [t for t in tabs if 'intro' in t['url'] or (t['url'].startswith('chrome') and not 'extension' in t['url'])][0]
ws_url = intro["webSocketDebuggerUrl"]
async with websockets.connect(ws_url) as ws:
    await ws.send(json.dumps({"id":1,"method":"Page.navigate","params":{"url":"https://gemini.google.com/app"}}))
    await ws.recv()
```

## Test edilen Chrome sürümü
Chrome/148.0.7778.97 (Scoop ile kurulu)
Yol: `/c/Users/eymen/scoop/apps/googlechrome/148.0.7778.97/chrome.exe`
