---
name: n8n-lancio
description: n8n kontrol et, baslat, sifre sifirla, Chrome'da ac ve workflow yardimi
---

# n8n Açma ve Yönetme

## Ne Zaman Kullanılır
Kullanıcı "n8n aç", "n8n çalıştır", "n8n başlat" veya benzeri bir komut verdiğinde.
Ayrıca n8n login sorunu, workflow oluşturma yardımı, loop/döngü kurulumu için de kullanılır.

## Adımlar

### 1. n8n çalışıyor mu kontrol et
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:5678/
```
- HTTP 200 dönerse → çalışıyor, atla
- Hata alırsan → çalışmıyor, başlat

### 2. n8n başlat (çalışmıyorsa)
```bash
n8n start &
```
Başarılı olup olmadığını curl ile doğrula (birkaç saniye bekle).

### 3. Chrome'da aç (güvenlik uyarısız)
Chrome'u `--unsafely-treat-insecure-origin-as-secure` flag'i ile başlat:
```powershell
Start-Process 'C:\Users\eymen\scoop\apps\googlechrome\current\chrome.exe' -ArgumentList '--unsafely-treat-insecure-origin-as-secure=http://localhost:5678', 'http://localhost:5678'
```
Alternatif: `C:\Users\eymen\n8n-ac.bat` scriptini çalıştır.
Alternatif (workflow ID varsa):
```
http://localhost:5678/workflow/<WORKFLOW_ID>?new=true
```

### 4. Şifre sıfırlama (login sorunu)
n8n login sayfası "Wrong username or password" hatası veriyorsa:
- n8n'i durdur → kullanıcıyı bul → hash oluştur → yaz → başlat
- **Detaylı komutlar için:** `references/n8n-sifre-sifirlama.md`

### 5. Workflow yardımı / döngü oluşturma
Kullanıcı n8n'de döngü kurmak istediğinde:
- Schedule Trigger (her 5 saniye/periyodik)
- Loop Over Items (liste üzerinde döngü)
- Set node (değişken ekleme)
- NoOp (placeholder)

GUI açık değilse Chrome'u aç, kullanıcıya adım adım söyle (terminal değil, ekran).

### 6. n8n API ile workflow oluşturma (detaylı)
API üzerinden workflow oluşturma, aktifleştirme ve execution izleme için:
- **Detaylı komutlar:** `references/n8n-api-workflow.md`

Python ile Chrome kontrolü isterse:
Kullanıcı Python'dan Chrome kontrolü isterse:
- Chrome binary: `C:\\Users\\eymen\\scoop\\apps\\googlechrome\\current\\chrome.exe`
- `C:\\Users\\eymen\\n8n-gui.py` hazır script (n8n çalışıyor mu kontrol et + Chrome'da aç)
- **NOT:** Selenium/Playwright ile Python Chrome kontrolü Hermes venv'inde değil, Anaconda Python'unda
  (`/c/Users/eymen/anaconda3/python.exe` ile `pip install selenium`)
- **Tercih edilen yöntem:** `powershell.exe -Command "Start-Process ..."` — daha hızlı ve hatasız

## KULLANICI PREFERANSLARI (KAZANIMLAR)

### 1. Otomatik Durum Tespiti (SORMA, YAP)
Kullanıcı "kontrol et", "durumu öğren", "ne durumda" dediğinde:
- Otomatik kontrol yap, kullanıcıya sorma
- n8n: `curl -s -o /dev/null -w "%{http_code}" http://localhost:5678/`
- Chrome: `ps | grep chrome | grep -v grep`
- Sonucu kısa raporla: `n8n: ✅/❌, Chrome: ✅/❌`
- "bana sorma bu bir kazanım sana" kuralı gereği tüm rutin kontroller otomatik

### 2. Terminal vs GUI Bilinci
- Workflow oluşturma, düzenleme, canlı izleme → Chrome'da aç
- Servis kontrolü, API çağrıları, dosya işlemleri → terminal
- "ekranda oluşumunu görmek istiyorum" dediğinde Chrome'da aç, terminalde anlatma

### 3. Kullanıcıya Sormama Kuralı
- Temel işlemlerde (servis kontrol, hata ayıklama, dosya tarama) kullanıcıya sorma
- Sadece geri dönüşü olmayan kararlarda sor (silme, reset, büyük değişiklik)
- Kullanıcı "sen bilirsin", "bana sorma", "bu bir kazanım" dediğinde hemen belleğe kaydet

### Notlar
- Chrome scoop üzerinden kurulu (googlechrome)
- n8n npm global v2.19.5 (node ile direkt çalışır, Docker gerekmez)
- Port: 5678 (n8n), 5679 (Task Broker)
- Kullanıcı: markopasa_@hotmail.com
- Şifre varsayılan: 123456 (sıfırlandıysa)
