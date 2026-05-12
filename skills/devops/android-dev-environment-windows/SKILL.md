---
name: android-dev-environment-windows
description: "Windows 11'de Android geliştirme ortamı kurulumu — JDK, Gradle, Android SDK (cmdline-tools ile), ADB, ANDROID_HOME yapılandırması. Hem React Native/Expo hem de native Kotlin/Java projeleri için."
category: "devops"
---

# Android Dev Environment — Windows 11 Kurulumu

## Ne Zaman Kullanılır
- Yeni bir Android projesi başlatılmadan önce ortam kontrolü gerektiğinde
- Bilgisayar değişikliği / sıfır kurulum yapıldığında
- Eksik araçlar tespit edildiğinde (JDK, Gradle, SDK, ADB)

## Ön Koşullar
- Windows 11 (64-bit)
- Scoop paket yöneticisi (`scoop --version` ile doğrula)
- PowerShell veya Git Bash terminali
- En az 10 GB boş disk, 16+ GB RAM önerilir

## Adım Adım Kurulum

### 1. Sistem Kontrolü
```bash
# CPU, RAM, disk
powershell -Command "Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores | Format-List"
powershell -Command "Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory | Format-List"
powershell -Command "Get-PSDrive C | Select-Object Used, Free | Format-List"
```

**Önerilen minimum:** i5/8 çekirdek, 16 GB RAM, 50 GB boş disk

### 2. JDK Kontrol / Kurulum
```bash
java -version
# Çıktı yoksa:
scoop install openjdk21
```

### 3. Gradle Kurulum
```bash
# Scoop ile (otomatik)
scoop install gradle
gradle --version

# Scoop yavaşsa manuel:
curl -L -o /tmp/gradle-bin.zip "https://services.gradle.org/distributions/gradle-8.13-bin.zip"
cd /tmp && unzip -q gradle-bin.zip
mkdir -p ~/scoop/apps/gradle/current
mv gradle-8.13/* ~/scoop/apps/gradle/current/
scoop reset gradle
```

### 4. Android SDK (cmdline-tools ile)
```bash
SDK_DIR="$HOME/AppData/Local/Android/Sdk"
mkdir -p "$SDK_DIR/cmdline-tools"
cd "$SDK_DIR"

# En son sürüm için developer.android.com/studio sayfasındaki linki kontrol et
# (commandlinetools-win-XXXXX_latest.zip)
curl -L -o cmdline-tools.zip "https://dl.google.com/android/repository/commandlinetools-win-14742923_latest.zip"
unzip -q cmdline-tools.zip
mkdir -p cmdline-tools && mv latest cmdline-tools/ 2>/dev/null
rm cmdline-tools.zip
```

### 5. SDK Platform + Build Tools + Platform Tools Yükle
```bash
export ANDROID_HOME="$HOME/AppData/Local/Android/Sdk"
yes | "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager.bat" \
  "platforms;android-35" \
  "build-tools;35.0.0" \
  "platform-tools"
```

**Alternatif API seviyeleri:** Projene bağlı — `android-34`, `android-36` de yüklenebilir.

### 6. ANDROID_HOME Ortam Değişkeni
```powershell
# PowerShell'de kalıcı ayar
[System.Environment]::SetEnvironmentVariable(
  'ANDROID_HOME',
  "$env:USERPROFILE\AppData\Local\Android\Sdk",
  'User'
)
```

**Not:** Git Bash'te `echo $ANDROID_HOME` boş gözükebilir — bu normaldir. Windows env değişkenleri Git Bash'te otomatik aktarılmaz. React Native / Expo projeleri SDK'yı `$LOCALAPPDATA\Android\Sdk` altında kendisi bulur.

### 7. ADB (Platform Tools)
Scoop'tan ayrıca adb kurma — SDK platform-tools içinde gelir. Yol:
```bash
ls "$HOME/AppData/Local/Android/Sdk/platform-tools/adb.exe"
```

Eski Scoop adb'sini kaldır:
```bash
scoop uninstall adb  # SDK platform-tools kullanılacak
```

### 8. Doğrulama
```bash
java --version          # OpenJDK 21+
node --version          # v18+ (Expo/RN için)
gradle --version        # 8.x+
ls $ANDROID_HOME/platforms/android-35   # SDK var mı?
ls $ANDROID_HOME/build-tools/35.0.0     # Build tools var mı?
ls $ANDROID_HOME/platform-tools/adb.exe # ADB var mı?
```

## Pitfalls / Tuzaklar

### MSVC Build Tools
- **React Native bare workflow** veya **native modüller** yazacaksan gerekli
- Expo managed workflow için gerekli DEĞİL
- Kurulum: `winget install Microsoft.VisualStudio.2022.BuildTools --override "--add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"` (5-10 dk sürer)

### MSYS2 Path Dönüşümü
Git Bash'ten SDK dizinine erişirken:
```bash
# Yanlış → MSYS2 /c/Users/eymen/... yerine C:\Users\eymen\... dener
ls /c/Users/eymen/AppData/Local/Android/Sdk/platforms/

# Doğru → MSYS_NO_PATHCONV=1 ile
MSYS_NO_PATHCONV=1 ls /c/Users/eymen/AppData/Local/Android/Sdk/platforms/

# Veya Windows stili çift ters slash
ls C:\\Users\\eymen\\AppData\\Local\\Android\\Sdk\\platforms\\
```

### Android Studio vs Cmdline-tools
- **Full Android Studio** Scoop'tan 1 GB+ olarak iner, uzun sürer
- Sadece SDK yönetimi için **cmdline-tools** yeterlidir (150 MB)
- Android Studio'yu sadece emülatör / layout editor / IDE özellikleri için gerek

### Expo CLI
- Node 24+ ile `expo-cli` legacy uyarısı normaldir
- Modern Expo projeleri `npx expo` ile çalışır, ayrıca global kurulum gerekmez
