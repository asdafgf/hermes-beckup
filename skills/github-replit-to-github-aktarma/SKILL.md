---
name: github-replit-to-github-aktarma
description: "Replit'ten GitHub'a proje aktarma otomasyonu — güvenlik izolasyonlu, adım adım raporlu Python scripti ile. Repo oluştur, git init, commit, push."
category: "github"
---

# Replit → GitHub Proje Aktarma

## Ne Zaman Kullanılır
- Replit'teki bir projeyi GitHub'a taşımak istediğinde
- Yeni bir Python projesini güvenlik kontrollü GitHub'a yüklemek istediğinde
- Replit Cloudflare korumasını undetected-chromedriver ile aşıp projeyi ZIP olarak indirmek istediğinde

## Ön Koşullar
- `gh` CLI kurulu ve GitHub'a authenticate edilmiş (`gh auth status`)
- Git kurulu
- Python paketleri: `pip install undetected-chromedriver selenium colorama python-dotenv`

## Android Studio / Expo Proje Kurulumu

ZIP'ten çıkarılan proje bir **Expo/React Native monorepo** ise (pnpm workspace + `artifacts/mobile/` klasörü):

### 1. Bağımlılıkları Yükle
```bash
cd /c/Users/eymen/proje_adi
pnpm install --no-frozen-lockfile
```
Not: Replit projelerinde `preinstall` script'i hata verebilir ("Use pnpm instead") — bu güvenlik kontrolüdür, bağımlılıklar yine de yüklenir.

### 2. Android Native Klasörünü Oluştur
```bash
cd /c/Users/eymen/proje_adi/artifacts/mobile
npx expo prebuild --platform android
```
Bu komut `android/` klasörünü oluşturur (Gradle + Android manifest). Etkileşimli modda "Install the updated dependencies?" sorusuna `y` ver.

### 3. Android Studio ile Aç
```bash
"/c/Program Files/Android/Android Studio/bin/studio64.exe" "C:\Users\eymen\proje_adi\artifacts\mobile\android"
```
Alternatif: Android Studio'yu manuel aç → **File → Open** → `C:\Users\eymen\proje_adi\artifacts\mobile\android` seç.

### 4. Gradle Sync
- Sağ alt panelde "Gradle sync finished" yazısını bekle
- Üst menüde Run (▶️) butonu aktifleşince derlemeye hazır

### 5. Expo Dev Server (isteğe bağlı)
```bash
cd /c/Users/eymen/proje_adi/artifacts/mobile
npx expo start
```

### Windows Dosya Yolu İpuçları
- **OneDrive Desktop:** Kullanıcının Desktop'ı `C:\Users\eymen\OneDrive\Masaüstü\` altında olabilir. `search_files(path="C:\Users\eymen", ...)` ile tüm alt dizinleri tara.
- **ZIP'te `|` karakteri:** Replit ZIP'leri pipe karakteri içeren dosyalar barındırabilir (örn. `artifacts|mobile.metadata.toml`). Windows'ta `|` geçersizdir — bu dosyaları atla.
- **Zip çıkarma (cache hariç):** `.local/share/pnpm` ve `node_modules` içeren dosyaları atla (550+ MB cache). Sadece gerçek proje dosyalarını çıkar (~15 MB).

## Kullanım — Seneryo A: Replit'ten Export

### 1. .env Dosyasını Hazırla
Proje klasörüne `.env` oluştur (şablon için skill'deki `templates/env_replit.txt`'i kullan):
```
REPLIT_EMAIL=ornek@mail.com
REPLIT_PASSWORD=sifren
REPLIT_USER=kullanici_adi
REPLIT_PROJECT=ProjeAdi
DOWNLOAD_DIR=C:\\Users\\eymen\\proje_adi
```

### 2. Replit Export Script'ini Çalıştır
```bash
cd /c/Users/eymen/proje_adi
python replit_export.py
```
Script: Chrome açar → Replit'e giriş yapar → ZIP indirir.

### 3. Alternatif: Google Drive'dan Manuel İndirme
Replit Cloudflare koruması aşılamazsa, kullanıcıdan telefonda Drive'ı açıp ZIP'i indirmesini iste.
Dosyayı OneDrive-senkronize masaüstüne kaydedebilir (`C:\Users\eymen\OneDrive\Masaüstü\`).
Agent bu dosyayı `search_files` ile bulur.

**OneDrive Desktop arama ipucu:** OneDrive kullanıcılarının Desktop'ı `C:\Users\eymen\Desktop\` değil,
`C:\Users\eymen\OneDrive\Masaüstü\` altında olabilir. `search_files(path="C:\Users\eymen", ...)` ile tüm alt dizinleri tara.

### 4. GitHub'a Push Et (ZIP indikten sonra)
```bash
# ZIP'ten projeyi çıkar (pnpm cache/node_modules hariç)
python -c "
import zipfile, os
path = r'C:\Users\eymen\...\proje.zip'
target = r'C:\Users\eymen\proje_adi'
with zipfile.ZipFile(path, 'r') as z:
    for n in z.namelist():
        if '.local/share/pnpm' in n or 'node_modules' in n:
            continue
        # ZIP içinde kök klasör varsa strip et
        parts = n.split('/', 1)
        rel = parts[1] if len(parts) > 1 and parts[0] == os.path.basename(n.split('/')[0]) else n
        if not rel: continue
        dest = os.path.join(target, rel)
        if n.endswith('/'):
            os.makedirs(dest, exist_ok=True)
        else:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with z.open(n) as src, open(dest, 'wb') as dst:
                dst.write(src.read())
"

PROJE_DIZIN=. GITHUB_REMOTE_URL=https://github.com/asdafgf/proje_adi.git python github_autosetup.py
```

**ZIP çıkarma uyarısı:** Replit ZIP'leri `|` (pipe) karakteri içeren dosya adları barındırabilir
(örn. `artifacts|mobile.metadata.toml`). Windows'ta `|` geçersiz karakterdir — bu dosyaları
atla veya `_` ile değiştir.

## Kullanım — Seneryo B: Mevcut Yerel Projeyi Push

### 1. GitHub'da Repo Oluştur
```bash
gh repo create asdafgf/proje-adi --public --description "Proje aciklamasi"
```

### 2. github_autosetup.py Çalıştır
```bash
cd /c/Users/eymen/proje-adi
PROJE_DIZIN=/c/Users/eymen/proje-adi \
GITHUB_REMOTE_URL=https://github.com/asdafgf/proje-adi.git \
GIT_BRANCH=main \
python github_autosetup.py
```

## Script: github_autosetup.py (10 Adım)
Script'in yaptıkları:
1. Git kurulum kontrolü
2. Proje dizini belirle (`PROJE_DIZIN` env)
3. `.gitignore` oluştur/güncelle (env, key, pem, pycache koruma)
4. `.env` güvenlik taraması
5. `git init`
6. Git kullanıcı config (global'dan okur)
7. `git add .`
8. `git commit`
9. `git remote add origin`
10. `git push -u origin main`

## Script: replit_export.py (Undetected ChromeDriver)
Replit Cloudflare bypass için:
- Chrome mevcut profili kullanır (varsa giriş yapmaz)
- `--disable-blink-features=AutomationControlled` ile bot tespitini engeller
- Önce doğrudan ZIP URL'ini dener, olmazsa menüden tıklar
- İndirme tamamlanana kadar bekler (.crdownload takibi)

## Önemli Uyarılar
- **Branch hatası (çözüldü):** `git init` sonrası default branch `master` olur; `git push -u origin main` `src refspec main does not match` hatası verir. Çözüm: `github_autosetup.py` Adım 5 içinde `git branch -m main` yaparak branch'i main'e çevirir. Branch anahtarı `GIT_BRANCH` env değişkeninden alınır (varsayılan: `main`).
- **Windows/MSYS2:** WSL komutlarında `MSYS_NO_PATHCONV=1` ön eki kullan. Aksi halde `/root/` → `C:/root/` dönüşür.
- **Replit Export:** Script etkileşimli olarak da çalışır (env'de bilgi yoksa input sorar); non-interactive ortamda tüm env değişkenlerini ayarla
- **Chrome profili:** `CHROME_PROFILE` yolunda Replit oturumu varsa login adımı atlanır — manuel giriş daha hızlı olabilir
- **Windows'ta undetected-chromedriver port çakışması:** Windows'ta art arda başarısız ChromeDriver oturumları `FIN_WAIT_2`/`CLOSE_WAIT` durumunda TCP portları bırakır. `SessionNotCreatedException: cannot connect to chrome at 127.0.0.1:XXXXX` hatası alınırsa:
  1. `taskkill /F /IM chrome.exe` ve `taskkill /F /IM chromedriver.exe` ile tüm süreçleri öldür
  2. `netstat -ano | grep <PORT>` ile takılı portları kontrol et (FIN_WAIT portları zamanla temizlenir)
  3. `version_main=<Chrome surumu>` parametresini ekle: `uc.Chrome(options=options, version_main=148)` 
  4. Alternatif: `use_subprocess=False` yerine `use_subprocess=True` dene (veya tersi)
  5. Son çare: Bilgisayarı yeniden başlat (FIN_WAIT portlarını temizler)
- **Google Drive bot koruması:** Undetected-chromedriver, Playwright, Firefox hepsi Google'ın "Bu tarayıcı veya uygulama güvenli olmayabilir" engeline takılır. Başarılı yöntem: kullanıcının telefonda Drive'dan manuel indirmesi → OneDrive Desktop'a kaydetmesi → agent'ın `search_files` ile bulması.

## İlgili Dosyalar
- `scripts/github_autosetup.py` — GitHub push otomasyonu
- `scripts/replit_export.py` — Replit'ten ZIP indirme (Cloudflare bypass)
- `templates/env_replit.txt` — .env şablonu
