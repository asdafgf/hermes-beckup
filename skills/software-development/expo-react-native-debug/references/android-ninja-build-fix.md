# Android Ninja Build Fix — Debugging Log

## Problem

Gradle `assembleDebug` fails with:
```
ninja: error: manifest 'build.ninja' still dirty after 100 tries
ninja: error: mkdir(src/fabric/CMakeFiles/fabric.dir/C_/rj/node_modules/.pnpm/expo-modules-core@3.0.30_...): No such file or directory
```

## Root Cause

CMake object file paths exceed Windows 250-character limit. The chain:
- `C:\rj\` (short path, ~5 chars) ← good
- `node_modules\.pnpm\expo-modules-core@3.0.30_re_2f59f25f5fdf62302d93826c804e1e4e\node_modules\expo-modules-core\android\.cxx\Debug\4zw1u772\arm64-v8a\CMakeFiles\fabric.dir\C_\rj\...` ← ~235+ chars
- Plus object file names → exceeds 250 limit

## Solutions Attempted (in order)

| # | Solution | Result |
|---|----------|--------|
| 1 | Junction `.cxx` to short path | ❌ Ninja still sees `.pnpm` paths in build scripts |
| 2 | `pnpm config store-dir` to short path | ❌ Doesn't affect `.pnpm` in node_modules |
| 3 | `node-linker=hoisted` in `.npmrc` | ❌ pnpm workspace ignores hoisted mode |
| 4 | Flatten `.pnpm/*/node_modules/*` to root node_modules | ❌ build.ninja cached with old paths, --rerun-tasks didn't help |
| 5 | Delete `.pnpm` dir entirely | ❌ breaks `settings.gradle` require.resolve |
| 6 | Switch to npm (remove pnpm workspace) | ❌ `catalog:` protocol not supported by npm |
| 7 | Replace `catalog:` with real versions + npm install | ❌ workspace:* deps need manual removal |

## What Actually Works

### Çözüm A: Kısa yola taşı (tercih edilen)
**Moving project to a very short path** (e.g., `C:\\rj` instead of `C:\\Users\\eymen\\Runners-Journey`) reduces path length by ~20+ characters. Combined with one of the above flattening techniques, this is the reliable fix.

### Çözüm B: WSL'de build al (en garanti)
WSL'de CMake/ninja path sorunu yaşanmaz çünkü Linux dosya sistemi 250 karakter sınırı yoktur:
```bash
wsl

# WSL içinde:
cd /mnt/c/rj/artifacts/mobile

# ANDROID_HOME'u Windows SDK'sına yönlendir:
export ANDROID_HOME="/mnt/c/Users/eymen/AppData/Local/Android/Sdk"
export PATH=$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator

# Eksikse yükle:
sudo apt install -y openjdk-21-jdk nodejs npm
sudo npm install -g pnpm npx

pnpm install
npx expo prebuild --clean
npx expo run:android
```

**Not:** WSL içinde adb Windows'taki emülatörü görmez (ayrı kernel). Ya `adb connect` ile bağlan (emülatör `adb tcpip 5555` ile dinliyorsa) ya da emülatör yerine fiziksel cihazla USB üzerinden çalış. Alternatif: WSL2 Android Studio emülatör desteği için `netsh interface portproxy` kullanılabilir.

### Çözüm C: pnpm store path'ini kısalt
```bash
pnpm config set store-dir C:\pnpm-store --global
cd /c/rj
rm -rf node_modules
pnpm install
```

### Çözüm D: Tüm .cxx cache'lerini temizle + baştan dene
```bash
find /c/rj/node_modules/.pnpm -path "*.cxx" -type d -exec rm -rf {} + 2>/dev/null
cd /c/rj/artifacts/mobile
npx expo prebuild --clean
npx expo run:android
```

### ⚠️ Önemli Uyarılar
- **newArchEnabled = true** zorunlu — react-native-reanimated ve react-native-worklets New Architecture olmadan çalışmaz (assertNewArchitectureEnabledTask hatası).
- **CYGWIN/MSYS env varsayılanı path dönüştürme yapar** — `--cmake-path` ile CMake'i Windows native path'te çalıştırmayı dene.
- **pnpm hoisted mode bazen yeterli değildir** — çünkü CMakeLists.txt içindeki `file(GLOB ...)` relatif yolları pnpm symlink store'un içine çözer.
- **pnpm cache kullanma:** `--config.cache-dir=$(pwd)/.cache` store'u proje içine alarak path uzunluğunu kısaltabilir.

## Key Commands Used

```bash
# Move project (Windows)
cmd /c rename "C:\Users\eymen\runners-journey" rj

# Kill node processes (fix EPERM)
powershell.exe -Command "Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force"

# Fix preinstall script (Windows compat)
# Change in package.json:
# "preinstall": "sh -c '...'" → "preinstall": "node -e \"...\" 2>nul || echo skipping"

# Approve builds
pnpm approve-builds esbuild

# Clean .cxx
cmd /c rmdir artifacts/mobile/android/.cxx
rm -rf node_modules/.pnpm

# Quick check: path length
python -c "import os; print(len(os.path.abspath('node_modules/.pnpm/expo-modules-core@3.0.30_re_.../node_modules/expo-modules-core/android/.cxx/Debug/xxx/arm64-v8a/CMakeFiles/fabric.dir')))"
```
