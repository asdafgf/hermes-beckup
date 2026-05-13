# pnpm + Ninja Path Issue (Windows)

## Hata
```
ninja: error: manifest 'build.ninja' still dirty after 100 tries
```

Ayrıca şu hata da aynı kökenden gelir:
```
ninja: error: mkdir(src/fabric/CMakeFiles/.../C_/rj/node_modules/.pnpm/...): No such file or directory
```

## Nedeni
pnpm, `node_modules/.pnpm/<package>@<hash>/node_modules/<package>` şeklinde derin bir symlink/copy yapısı kullanır. Bu, Windows 260 karakter path sınırına yaklaşır. CMake/Ninja object file path'leri 250 karakteri aşınca `build.ninja` manifest'i güncelleyemez ve 100 denemeden sonra pes eder.

Ayrıca CMake, pnpm symlink'lerini çözümlerken Windows drive harfini (`C:\`) `C_/` formatına çevirir ve bu dizin var olmadığı için `mkdir` hatası alınır.

## Hangi modüller etkilenir

Birden fazla C++ native modül aynı anda build edilirken path çakışması yaşanır. En sık görülenler:
- `react-native-screens` — genelde ilk hatayı veren
- `expo-modules-core` — fabric CMakeFiles altında path hatası
- `react-native-reanimated` — CMAKE_OBJECT_PATH_MAX uyarısı + ninja hatası
- `react-native-worklets` — aynı pattern
- `.pnpm/<package>@<hash>` yapısındaki her C++ modül

**ÖNEMLİ:** İlk hatada react-native-screens görünse de, clean build'de farklı modül hatası çıkabilir (ör: react-native-worklets veya expo-modules-core). **Kök neden path uzunluğudur, hangi modülün hata verdiği tesadüfidir.**

## Etkilenen durumlar
- Expo New Architecture (Fabric) ile native C++ derlemesi
- `expo-modules-core` gibi CMake kullanan modüller
- pnpm v9+ (veya v11 gibi daha yeni sürümler)
- Windows + MSYS/git-bash ortamı
- `react-native-reanimated` ve `react-native-worklets` (New Architecture ZORUNLU)

## newArchEnabled kısıtlaması
Proje `react-native-reanimated` veya `react-native-worklets` kullanıyorsa:
```json
// app.json
"newArchEnabled": true  // ZORUNLU, false yapılamaz
```
Kapatılırsa şu hata alınır:
```
[Reanimated] Reanimated requires new architecture to be enabled.
[Worklets] Worklets require new architecture to be enabled.
```
Bu durumda C++ native build kaçınılmazdır — hoisted linker çözümü şarttır.

## Çözüm stratejileri

### 1. node-linker=hoisted (önerilen — tek seferlik)
```bash
# .npmrc'ye yazmadan hızlı deneme:
pnpm install --config.node-linker=hoisted

# Kalıcı yapmak için:
echo "node-linker=hoisted" >> .npmrc
rm -rf node_modules
pnpm install
```
Bu, pnpm'i flat `node_modules` yapısına zorlar (pnpm'nin disk tasarrufu kaybolur ama path sorunu çözülür).

### 1b. .npmrc'ye ek ayarlar (workspace'ler için)
```ini
node-linker=hoisted
shamefully-hoist=true
symlink=false
resolve-peers-from-workspace-root=true
dedupe-peer-dependents=true
```
Bu ayarlar bile bazen yetersiz kalır. O zaman...

### 1c. Son çare: npm install (pnpm'i bypass)
pnpm workspace yapısındaki `.pnpm` symlink'leri çözülmezse, npm ile flat install dene:
```bash
# pnpm-lock.yaml temizle
rm pnpm-lock.yaml
# preinstall script'i kaldır (npm ile çalışmaz)
npm install
```
**Uyarı:** npm ile workspace bağımlılıkları (expo gibi) doğru çözülmeyebilir. `artifacts/mobile` altında `npm install expo` ile manuel kurulum gerekebilir.

### 2. Projeyi C:\'e yakın taşı
`C:\Users\eymen\Runners-Journey` yerine `C:\rj` gibi daha kısa bir yol.

### 3. .cxx cache temizleme (geçici düzeltme — genelde işe yaramaz)
```bash
find /c/rj/node_modules/.pnpm -path "*/android/.cxx" -exec rm -rf {} + 2>/dev/null
```
Not: Bu sadece clean build yapar, kök neden path uzunluğuysa yine aynı hata alınır.

### 4. Windows Long Path desteği
```powershell
# Registry'den etkinleştir (admin)
New-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```
Ancak bu her durumda işe yaramaz — Ninja/CMake kendi path buffer'larını da kontrol eder.

### 5. WSL'de build al (son çare)
```bash
wsl
cd /mnt/c/rj/artifacts/mobile
npx expo run:android
```
WSL'de path sorunu olmaz. Ön koşul: WSL'de Node.js ve pnpm kurulu olmalı.

### 6. .pnpm flatten + Gradle --rerun-tasks (kapsamlı çözüm denemesi)
pnpm symlink'leri kaldırılıp tüm paketler root node_modules'a kopyalanır, sonra Gradle cache bypass edilir:

```bash
# .pnpm'yi sil
rm -rf node_modules/.pnpm

# .cxx cache'ini temizle
rm -rf artifacts/mobile/android/.cxx
# Veya junction varsa: cmd /c rmdir artifacts/mobile/android/.cxx

# Gradle clean + --rerun-tasks ile tüm cache bypass
cd artifacts/mobile/android
./gradlew clean
./gradlew assembleDebug --rerun-tasks
```

`--rerun-tasks` olmazsa, Gradle önceden oluşturulmuş build.ninja script'lerini yeniden kullanır ve hâlâ `.pnpm` yollarını arar.

**ÖNEMLİ:** Bu çözüm bile bazen yetersiz kalır çünkü node_modules'ta pnpm workspace link'leri hâlâ `.pnpm`'e referans verebilir. Bu durumda `pnpm rebuild` veya `pnpm install --force` gerekebilir.

### 7. pnpm rebuild ile native modülleri yeniden derle
```bash
# Tüm native modülleri zorla yeniden derle
pnpm rebuild

# Spesifik modül
pnpm rebuild expo-modules-core react-native-screens react-native-reanimated
```

### 8. Kesin çözüm: Projeyi npm'e taşı (pnpm workspace'i bırak)
pnpm workspace yapısındaki `.pnpm` symlink'leri Windows CMake/Ninja ile uyumsuz. En kesin çözüm:
1. `pnpm-lock.yaml` sil
2. `package.json`'daki `preinstall` script'ini kaldır
3. `.npmrc` temizle
4. `npm install` yap
5. Expo prebuild --clean
6. Gradle build

**Risk:** npm workspace'ler arası bağımlılıkları doğru çözemeyebilir. `artifacts/mobile` altında `npm install expo` ile manuel kurulum gerekebilir.

### 9. Bir sonraki adım: APK çıktıysa emulator'e yükle
Build başarılı olursa APK şurada olur:
```
artifacts/mobile/android/app/build/outputs/apk/debug/app-debug.apk
```
Emulator'e yüklemek için:
```bash
adb install -r artifacts/mobile/android/app/build/outputs/apk/debug/app-debug.apk
```

## Çözülmemiş senaryo
Bu oturumda (2026-05-12) tüm yöntemler denenmesine rağmen `ninja: error: manifest 'build.ninja' still dirty after 100 tries` hatası çözülemedi. Sorunun kökü:
- pnpm workspace'ler arası link'ler (root node_modules <-> artifacts/mobile node_modules)
- CMake'in C_/ dönüşümü
- Gradle'in cached build script'leri yeniden kullanması

**Muhtemel çözüm:** Projeyi WSL'de build almak veya bir CI/CD pipeline'ında (GitHub Actions) build yapmak.

## Doğrulama
```bash
find /c/rj/node_modules/.pnpm -name "*.cpp.o" 2>/dev/null | head -5 | while read f; do echo "${#f} $f"; done
```

## Oturum referansı
İlk oluşturulma: 2026-05-12, Runners-Journey → rj projesi (Expo SDK 54, pnpm v11.1.1, JDK 21, Gradle 8.14.3)
Güncelleme: 2026-05-12, .pnpm symlink'lerinin workspace'lerde kalıcı olduğu, npm install fallback'i ve git stash gerekliliği eklendi.
