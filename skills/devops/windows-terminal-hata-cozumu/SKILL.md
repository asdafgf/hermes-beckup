---
name: windows-terminal-hata-cozumu
description: >-
  Windows'ta Hermes terminal tool'unun (git-bash) karşılaştığı süreç yönetimi sorunları:
  zombi süreçler, pipe sızıntıları, Chrome/Edge çakışmaları, timeout sonrası süreç temizliği.
  Aynı zamanda local.py'deki _kill_process iyileştirmesini içerir.
category: devops
---

# Windows Terminal Hata Çözümü

## Ne Zaman Kullanılır
- `subprocess.Popen` ile başlatılan işlemler (Chrome, Edge, Firefox) zaman aşımına uğrayıp asılı kalıyorsa
- "SessionNotCreated", "exitCode=21", "port already in use" gibi hatalar alınıyorsa
- Terminal tool'u yanıt vermiyor veya "Command interrupted" dönüyorsa
- Pipe/stream sızıntısı şüphesi varsa

## Windows'ta Process Group Yönetimi

Hermes'in terminal tool'u (`tools/environments/local.py`) aşağıdaki iyileştirmeleri içerir:

### `_run_bash` — `creationflags` eklendi
```python
creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if _IS_WINDOWS else 0,
```
Böylece `CTRL_BREAK_EVENT` tüm alt süreçlere ulaşır.

### `_close_pipes` — yeni metod
```python
def _close_pipes(self, proc) -> None:
    if proc is None:
        return
    try:
        if proc.stdout: proc.stdout.close()
    except Exception: pass
    try:
        if proc.stderr: proc.stderr.close()
    except Exception: pass
```
Her `_kill_process` çağrısında hem başta hem finalde çalıştırılır.

### `_kill_process` — kademeli sonlandırma (Windows)
1. **Pipe'ları kapat** — bloke okuyucu thread'ler çözülsün
2. **`CTRL_BREAK_EVENT`** gönder (nazik)
3. **1.5 sn bekle** — `proc.wait(timeout=1.5)`
4. **`proc.kill()`** — yanıt yoksa zorla öldür
5. **2 sn daha bekle** — zombi kalmasın
6. **Pipe'ları tekrar kapat** — kesin temizlik

## Sık Karşılaşılan Sorunlar

### Chrome "SessionNotCreatedException"
**Sebep:** Chrome zaten çalışıyor (arka planda 20+ process) VEYA önceki kapatılan ChromeDriver bağlantıları port'u `FIN_WAIT_2`/`CLOSE_WAIT` durumunda bıraktı.

**Önce port durumunu kontrol et:**
```bash
netstat -ano | grep -E "9222|32368|57008|57757"
# FIN_WAIT_2 / CLOSE_WAIT durumunda portlar varsa → yeni driver bağlanamaz
```

**Çözüm:**
```bash
# 1. Tüm chrome/chromedriver süreçlerini öldür
taskkill /F /IM chrome.exe
taskkill /F /IM chromedriver.exe

# 2. Lock dosyalarını temizle
rm -f "$HOME/../Local/Google/Chrome/User Data/SingletonLock"
rm -f "$HOME/../Local/Google/Chrome/User Data/SingletonSocket"

# 3. Port'u hâlâ tutan process varsa (PID'yi bul)
netstat -ano | grep 9222
# listen port PID'ini taskkill /F /PID <pid> ile öldür

# 4. FIN_WAIT portları 2-4 dk içinde otomatik temizlenir
# Beklemek istemiyorsan farklı port dene: --remote-debugging-port=9333
```

**Pitfall — `FIN_WAIT_2` ve `CLOSE_WAIT`:**  
Windows'ta kapatılan TCP bağlantıları hemen serbest kalmaz. `FIN_WAIT_2` durumu 2-4 dakika sürebilir. Bu sürede yeni ChromeDriver/undetected-chromedriver `cannot connect to chrome at 127.0.0.1:XXXXX` hatası verir. Çözüm: farklı port kullan veya bekle.

**Pitfall — `undetected-chromedriver` da aynı sorunu yaşar:**  
Undetected-ChromeDriver da `uc.Chrome()` içinde aynı `subprocess.Popen` mekanizmasını kullanır. Windows port kilitliyse o da başlamaz. Bu bir bot-koruması sorunu değil, port/process yönetimi sorunudur.

### Port 9222 "already in use"
**Sebep:** Önceki Chrome instance'ı portu bırakmadı.
**Çözüm:** Farklı port dene (`--remote-debugging-port=9333`), veya `netstat -ano | grep 9222` ile PID'i bulup taskkill yap.

### Firefox "exitCode=0" (hemen kapanıyor)
**Sebep:** Playwright'ın `-juggler-pipe` modu uyumsuz.
**Çözüm:** Firefox'u `subprocess.Popen` ile doğrudan başlat, Playwright kullanma.

### "Command timed out" sonrası zombi süreç
**Sebep:** Hermes timeout'ta süreci öldürmüyor, sadece beklemeyi bırakıyor.
**Çözüm:** 
```bash
ps aux | grep -iE "chrome|firefox|msedge" | grep -v grep
# Asılı kalanları elle öldür
taskkill /F /IM chrome.exe
taskkill /F /IM firefox.exe
```

## Otomatik Süreç Temizleme Scripti

```bash
# Tüm asılı tarayıcı süreçlerini öldür
for proc in chrome.exe chromedriver.exe firefox.exe msedge.exe; do
  taskkill /F /IM "$proc" 2>/dev/null
done
# Chrome lock dosyalarını temizle
rm -f "$HOME/../Local/Google/Chrome/User Data/SingletonLock" 2>/dev/null
rm -f "$HOME/../Local/Google/Chrome/User Data/SingletonSocket" 2>/dev/null
echo "Temizlik tamam"
```

## Patch Uygulama (local.py değişikliği)

Eğer `tools/environments/local.py` güncellenirse (Hermes upgrade sonrası sıfırlanabilir), değişiklikler:
1. `_run_bash` içinde `creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if _IS_WINDOWS else 0` satırını ekle
2. `_close_pipes(self, proc)` metodunu ekle
3. `_kill_process(self, proc)` metodunu pipe kapatma + kademeli sonlandırma ile değiştir
