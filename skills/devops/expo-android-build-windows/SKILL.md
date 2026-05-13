---
name: expo-android-build-windows
title: Expo Android Build on Windows
description: Run expo run:android on Windows — JDK setup, NDK, Gradle, pnpm monorepo workarounds, path length issues.
---

# Expo Android Build — Windows

## Ne zaman kullanılır

- Windows'ta `expo run:android` çalıştırılacaksa
- Gradle build hatası, NDK eksik, JDK uyumsuzluğu, pnpm path sorunu yaşanıyorsa

## Adımlar

### 1. Ortam Kontrolü

```bash
# JDK (21+)
java -version

# Android SDK yolu
echo $ANDROID_HOME
ls "$ANDROID_HOME/platforms/" 2>/dev/null
ls "$ANDROID_HOME/build-tools/" 2>/dev/null
```

### 2. NDK Kurulumu (Android Studio ile)

NDK eksikse ninja build hatası alırsın:

1. Android Studio aç → File → Settings → Appearance & Behavior → System Settings → Android SDK
2. **SDK Tools** sekmesi
3. **"NDK (Side by side)"** işaretle
4. **"Show Package Details"** tıkla
5. Projenin beklediği NDK sürümünü seç
6. **Apply → OK**

Alternatif: commandline tools ile:
```bash
sdkmanager.bat "ndk;27.1.12297006"
```

### 3. local.properties

Projede yoksa oluştur (`artifacts/mobile/android/local.properties`):

```properties
sdk.dir=C:\\<kullanici>\\AppData\\Local\\Android\\Sdk
```

### 4. JAVA_HOME

Android Studio JBR'si bozuk olabilir. Mevcut JDK'yı kullan:

```bash
# Mevcut JDK'yı bul
ls -d /c/Program\\ Files/*/jdk* /c/Program\\ Files/*/java* /c/Program\\ Files/*/zulu* /c/Program\\ Files/*/corretto*

# Kullan
JAVA_HOME="/c/Program Files/Microsoft/jdk-21.x.x.x-hotspot" pnpm expo run:android
```

**JDK-Gradle uyumu:**
- Gradle 8.x → JDK 21 veya 22 (max 23)
- `Unsupported class file major version XX` hatası → JDK çok yeni, Gradle'ı yükselt veya JDK düşür

### 5. pnpm Monorepo (Replit projeleri)

Replit'ten gelen Expo projelerinde workspace yapısı vardır:

```bash
# Ana dizinde preinstall script'i user_agent kontrolü yapar
# pnpm ile bypass:
pnpm install --ignore-scripts

# Workspace paketine gir
cd artifacts/mobile
pnpm android   # "android": "expo run:android" script'ini kullanır
```

**pnpm preinstall script'i Windows'ta kırılıyor:**
Replit projelerinin kök `package.json`'unda şu script bulunur:
```json
"preinstall": "sh -c 'rm -f package-lock.json yarn.lock; case \"$npm_config_user_agent\" in pnpm/*) ;; *) echo \"Use pnpm instead\"; exit 1 ;; esac'"
```
Bu script Windows'ta çalışmaz çünkü:
- `sh` MSYS'den gelir ve `$npm_config_user_agent` ortam değişkenini okuyamaz
- `case` ifadesi her zaman hata verir
- **Çözüm:** script'i kaldır veya `node` versiyonuyla değiştir:
```json
"preinstall": "node -e \"require('fs').unlinkSync('package-lock.json');require('fs').unlinkSync('yarn.lock')\" 2>nul || echo skipping"
```

### 6. Emülatör Başlatma (Android Studio olmadan)

```bash
# AVD'leri listele
export PATH=$PATH:"/c/Users/<user>/AppData/Local/Android/Sdk/emulator"
emulator -list-avds

# Emülatör başlat (arka plan)
emulator -avd <AVD_NAME> -no-snapshot &

# Hazır olana kadar bekle
export PATH=$PATH:"/c/Users/<user>/AppData/Local/Android/Sdk/platform-tools"
for i in $(seq 1 30); do
  sleep 2
  state=$(adb get-state 2>/dev/null)
  if [ "$state" = "device" ]; then echo "HAZIR"; break; fi
  echo -n "."
done
```

### 7. Expo run:android akışı

```bash
# Adım adım ilerle
export ANDROID_HOME="/c/Users/<user>/AppData/Local/Android/Sdk"
export PATH=$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator

# Prebuild (android/ klasörünü oluştur)
cd artifacts/mobile
echo "y" | npx expo prebuild

# Build + deploy
npx expo run:android
```

**ÖNEMLİ: Git dirty state prebuild'i bloklar.**
Expo prebuild, git working tree dirty ise uyarı verir ve bazı durumlarda işlemi durdurur (örn. android klasörünü temizler ama yeniden oluşturmaz). **Her zaman önce commit veya stash yap:**
```bash
git add -A && git stash
# veya
git commit -am "prebuild checkpoint"
```

### 8. newArchEnabled Kısıtlaması

Proje `react-native-reanimated` veya `react-native-worklets` kullanıyorsa:

```json
// app.json
"newArchEnabled": true   // ZORUNLU, false yapılamaz!
```

Kapatılırsa:
```
[Reanimated] Reanimated requires new architecture to be enabled.
[Worklets] Worklets require new architecture to be enabled.
```

Detaylı path sorunu çözümü için `references/pnpm-ninja-path-issue.md`'ye bak.

### 9. Doğrudan gradlew ile build

Expo CLI üzerinden değil, doğrudan Gradle build test:
```bash
cd artifacts/mobile/android
JAVA_HOME="..." ./gradlew assembleDebug
```

### 10. Eksik expo modülü hatası

Prebuild sırasında "Cannot determine which native SDK version your project uses because the module `expo` is not installed" hatası alınırsa, expo workspace'de eksik kalmıştır. **npm install ile root yerine mobile alt projesine kur:**

```bash
cd artifacts/mobile
npm install expo
# Sonra tekrar
npx expo prebuild --clean
```

Bu genelde pnpm workspace yapısında, expo'nun workspace root'tan symlink'lenmesi beklenirken flat node_modules'a geçince kopmasından kaynaklanır. `pnpm install` ile yeniden kurmak da çözebilir.

### 11. Hızlı Ortam Envanteri

Build öncesi tüm araçları tek komutta kontrol et:

```bash
echo "=== PYTHON ===" && which python && python --version && \
echo "=== DOCKER ===" && docker --version 2>&1 && \
echo "=== NODE ===" && node --version && npm --version && \
echo "=== GIT ===" && git --version && \
echo "=== JDK ===" && java -version 2>&1 && \
echo "=== ANDROID SDK ===" && echo $ANDROID_HOME && ls "$ANDROID_HOME/platforms/" 2>/dev/null && \
ls "$ANDROID_HOME/build-tools/" 2>/dev/null && \
echo "=== EXPO ===" && npx expo --version 2>/dev/null && \
echo "=== SCOOP ===" && scoop list 2>/dev/null | head -10 && \
echo "=== WSL ===" && wsl --version 2>/dev/null | head -3
```

**MSYS path notu:** Git Bash'te `echo $ANDROID_HOME` boş dönebilir ama Windows env değişkeni olarak çalışır — Gradle ve Expo kendisi bulur. `find` gibi Unix araçlarıyla SDK'yı tararken `MSYS_NO_PATHCONV=1` gerekebilir.

### 12. Android Studio ile Proje Açma

```bash
# Projeyi argüman olarak vererek aç
powershell.exe -Command "Start-Process -FilePath 'C:\Program Files\Android\Android Studio\bin\studio64.exe' -ArgumentList 'C:\rj\artifacts\mobile' -Verb RunAs"
```

**UAC notu:** `-Verb RunAs` UAC onayı ister. Onay verilmezse işlem sessizce başarısız olur. Önce mevcut studio64 process'ini kapatmak gerekebilir:
```bash
powershell.exe -Command "Get-Process studio64 -ErrorAction SilentlyContinue | Stop-Process -Force"
```

## Pitfalls

- **pnpm preinstall script'i bypass** — Replit monorepo'ları `$npm_config_user_agent` kontrol eder, Windows'ta kırılır. Script'i düzelt veya kaldır.
- **Android Studio JBR** — `jvm.cfg` eksik olabilir, o durumda JBR kullanılamaz, sistem JDK'sını ayarla
- **CMake uyarıları** — `CMAKE_OBJECT_PATH_MAX` uyarıları genelde zararsız, asıl hata `ninja: error` değilse
- **Gradle daemon** — Farklı JDK'lar arasında geçiş yapınca "incompatible daemon" uyarısı normal
- **Expo SDK 54+** — Babel, Hermes, New Architecture ile gelir; Kotlin 2.1+, KSP gerekebilir
- **pnpm symlink + CMake hatası** — pnpm .pnpm store'u Windows'ta CMake/Ninja path sorunlarına yol açar; çözüm için references/pnpm-ninja-path-issue.md
- **Git dirty state** — prebuild öncesi git stash yapılmazsa android klasörü silinir ve yeniden oluşturulmayabilir
- **npm ile pnpm workspace kurulumu** — npm install workspace'e flat kurulum yapabilir ama workspace'ler arası bağımlılıkları (expo gibi) doğru çözemeyebilir. pnpm ile devam etmek daha güvenilir.
- **Elle flatten yetmez, Gradle cache'li build.ninja** — node_modules/.pnpm'deki tüm paketleri root node_modules'a kopyalasam bile, Gradle önceden oluşturulmuş build.ninja script'lerini cache'ler ve hâlâ .pnpm yollarını arar. `--rerun-tasks` veya `cleanBuildCache` gerekir.
- **Gradle --rerun-tasks zorunlu** — C++ ninja hatası çözülür gibi olup tekrarlıyorsa, Gradle cache build script'lerini yeniden kullanıyordur. `./gradlew assembleDebug --rerun-tasks` ile zorla yeniden derlet. `./gradlew clean` tek başına yetersiz kalabilir.
- **CMake drive harfi kodlaması** — CMake `C:\` yolunu `C_/` olarak kodlar ve `.ninja` manifest'inde bu şekilde saklar. .pnpm silinse bile cached build script bu yolu kullanmaya devam eder. Mutlaka `--rerun-tasks` veya `.cxx` + Gradle cache temizliği birlikte yapılmalı.
