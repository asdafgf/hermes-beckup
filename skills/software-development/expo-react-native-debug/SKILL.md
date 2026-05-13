---
name: expo-react-native-debug
description: Fix TypeScript/React Native/Expo project build errors — Metro bundler, import path issues, decorator config, style dupes, merge conflicts
---

# Expo/React Native Proje Hata Ayıklama

## Ne Zaman Kullanılır
Kullanıcı bir Expo/React Native projesinde (örn. KiraLog gibi) derleme hatası, TypeScript hatası, Metro bundler hatası, import path sorunu, veya çalışma zamanı hatası aldığında.

## Adımlar

### 0. Projeyi Tanı — Todo ile Planla
Önce projenin ne olduğunu anla (Expo? CLI? Hangi kütüphaneler?) ve bir todo listesi oluştur:

1. `package.json`, `tsconfig.json`, `app.json` — proje yapısı
2. `npx tsc --noEmit` — TypeScript hatalarını tara
3. `npx expo export --platform web` — Metro bundler ile gerçek derleme
4. Mevcut test varsa çalıştır
5. Hataları kategorize et ve sırayla düzelt
6. Build'i tekrar dene (doğrulama)

Todo tool ile ilerlemeyi takip et (`completed` → `in_progress` → `pending`) — bu, çok sayıda dosyada işlem yaparken nerede kaldığını gösterir.

### 1. Önce package.json'u Oku
Proje yapısını ve bağımlılıkları anla:
```bash
cat package.json | head -50
```
Hangi Expo sürümü, hangi kütüphaneler kullanılıyor gör.

### 2. TypeScript Derlemesini Kontrol Et
```bash
npx tsc --noEmit 2>&1 | head -30
```
Hataları tek tek ele al.

### 3. Yaygın Hata Tipleri ve Çözümleri

#### a. Import Path Hatası (Module not found)
Genelde dosya taşıma/yeniden adlandırma sonrası olur:
```
Unable to resolve module ../../../utils/supabase from ...
```
**Çözüm:** Dosyanın bulunduğu dizine göre doğru göreceli yolu hesapla.
Örn: `app/(auth)/cloud-accounts.tsx` içinde `../../utils/supabase` doğruyken `../../../utils/supabase` yanlıştır.
Klasör derinliğine bak: count `../` from file location to project root.

#### b. Yanlış Kütüphane Adı (react-query vs @tanstack/react-query)
`react-query` artık `@tanstack/react-query` olarak güncellendi:
```typescript
// YANLIŞ:
import { useQuery } from 'react-query';
// DOĞRU:
import { useQuery } from '@tanstack/react-query';
```

#### c. Merge Çakışması (Duplicate Variable/Property)
Aynı satırların iki kopyası varsa — merge hatası:
```typescript
const { phone_number, otp } = await req.json();
const { phone_number, otp, full_name } = await req.json(); // DUPLICATE
```
**Çözüm:** Daha yeni/kapsamlı olan versiyonu tut, eskisini sil.

#### d. Duplicate Style Property
`StyleSheet.create` içinde aynı stil adı iki kere tanımlanmış:
```typescript
header: { marginBottom: 30, ... },
// ...
header: { flexDirection: 'row', ... }, // ERROR: duplicate
```
**Çözüm:** Hangisi doğru/eksiksizse onu tut, diğerini sil.

#### e. Null/Undefined Kontrolü
```typescript
// HATA: new Date(this.startDate) — startDate undefined olabilir
// ÇÖZÜM:
const start = new Date(this.startDate!);
```

#### f. React Query v5 API Değişikliği

`@tanstack/react-query` v5'te `useQuery` artık obje parametresi alır, eski `(key, fn, options)` imzası çalışmaz:
```typescript
// ESKİ (v4):
const { data } = useQuery('getContracts', fetchFn);

// YENİ (v5):
const { data } = useQuery({
  queryKey: ['getContracts'],
  queryFn: fetchFn,
});
```
Aynı şekilde `useMutation` da: `useMutation({ mutationFn, onSuccess })`.
`isLoading` artık `isPending` olarak da adlandırılabilir (v5'te her ikisi de var).

#### g. Supabase Client Protected Property'lere Erişim

`@supabase/supabase-js` v2'de `supabaseUrl`, `supabaseKey` gibi propertiler **protected** oldu:
```typescript
// HATA:
if (!supabase.supabaseUrl.includes("mock")) { ... }   // TS2445
fetch(url, { headers: { Authorization: `Bearer ${supabase.supabaseKey}` } })  // TS2445

// ÇÖZÜM: .env değişkenini doğrudan kullan:
if (!process.env.EXPO_PUBLIC_SUPABASE_URL?.includes("mock")) { ... }
fetch(url, { headers: { Authorization: `Bearer ${process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY}` } })
```

#### h. package.json main — Expo Router

Expo Router projelerinde `main` alanı `"expo-router/entry"` olmalı, `"index.ts"` değil:
```json
{
  "main": "expo-router/entry"
}
```
Bu olmazsa `expo export` "Cannot resolve entry file" hatası verir. Ayrıca kök `index.ts` dosyasına gerek yoktur — Expo Router kendi giriş noktasını yönetir.

#### i. Eksik Parantez/Kapatma
En sık rastlanan — fonksiyon sonunda `}` eksik:
```typescript
  await supabase.from('tsa_errors').insert({...});
}  // BURADA BİR } DAHA OLMALI - logCriticalError'i kapatmak için
```
**Tespit:** Derleyici `'}' expected` hatası verir. Dosyanın sonuna git, eksik parantezi ekle.

### 4. Metro Bundler ile Export Testi
```bash
npx expo export --platform web --output-dir /tmp/test-export 2>&1
```
Bu, tüm modülleri çözümler ve gerçek derleme hatalarını gösterir (tsc'nin gösterdiği dekoratör/lib hatalarını değil).

### 5. Expo Dev Server'ı Başlatma
```bash
cd /c/Users/eymen/kiralog
npx expo start --web
```
Sonra Chrome'da `http://localhost:8081` açılır.

### 6. Supabase Bağlantısı
`.env` dosyasındaki değişkenler:
```
EXPO_PUBLIC_SUPABASE_URL=
EXPO_PUBLIC_SUPABASE_ANON_KEY=
```

## Android Build (Gradle) — Windows Hata Çözümleri

### Hata 1: `ninja: error: manifest 'build.ninja' still dirty after 100 tries`

**Sebep:** CMake object file path'i Windows 250 karakter sınırını aşıyor. pnpm'nin `.pnpm/@package@version/node_modules/...` iç içe yapısı + proje yolu toplamda limiti aşar.

**Öncelikli çözüm (en etkili): Windows Long Path desteğini aç + Git longpaths + Bilgisayarı yeniden başlat**

Bu, kalıcı sistem seviyesinde çözümdür:

```cmd
# 1. Registry: LongPathsEnabled = 1
reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f

# 2. Git: longpaths true
git config --system core.longpaths true

# 3. Bilgisayarı yeniden başlat

# 4. Build doğrulama
cd /c/rj/artifacts/mobile/android
./gradlew clean
cd ..
npx expo run:android
```

**Alternatif (hızlı dene): Projeyi kısa bir yola taşı**
```bash
# C:\Users\eymen\proje-adi → C:\rj (20+ karakter kısalır)
mv /c/Users/eymen/runners-journey /c/rj
```
Windows taşıma sorunları için admin PowerShell:
```powershell
Rename-Item -Path "C:\Users\eymen\runners-journey" -NewName "rj" -Force
```
Git-bash'ten `mv` Permission denied verirse → `cmd /c rename "C:\Users\eymen\runners-journey" rj`

**İkincil çözüm: pnpm node_modules'u düzleştir (her zaman işe yaramaz)**
```bash
# .npmrc
echo "node-linker=hoisted" > .npmrc
echo "shamefully-hoist=true" >> .npmrc
# Temiz kurulum
rm -rf node_modules .pnpm-store
pnpm install
npx expo prebuild --clean
./gradlew assembleDebug
```

**Son çare: npm'e geç (pnpm workspace'ini kaldır)**
pnpm'nin `.pnpm` iç içe yapısı ve `catalog:` referansları Windows'ta sorun çıkarırsa:
1. `package.json`'daki `catalog:` referanslarını gerçek versiyonlarla değiştir (pnpm-workspace.yaml'daki catalog bölümünden oku)
2. `workspace:*` referanslarını kaldır
3. `pnpm-workspace.yaml` ve `pnpm-lock.yaml`'ı sil
4. `npm install --legacy-peer-deps` ile kurulum yap

**Alternatif: pnpm store'u kısa yola taşı**
```bash
pnpm config set store-dir C:\pnpm-store
pnpm install
```

**Alternatif: .cxx klasörünü junction yap**
```bash
# Android .cxx'yi C:\rj\.cxx_short'a junctionla
rmdir artifacts/mobile/android/.cxx
cmd /c mklink /J "artifacts/mobile/android/.cxx" "C:\rj\.cxx_short"
```

**Not:** `--rerun-tasks` flag'i Gradle cache'ini bypass eder ama CMake build script'leri (build.ninja) önbellekte kaldığı için yol sorunu devam edebilir. En güveniliri projeyi kısa yola taşımak.

### Hata 2: `[ERR_PNPM_IGNORED_BUILDS] Ignored build scripts: esbuild@0.27.3`

pnpm'in yeni güvenlik özelliği — build script'lerini manuel onay gerektirir:
```bash
pnpm approve-builds esbuild
```
Veya `pnpm-workspace.yaml`'da:
```yaml
allowBuilds:
  esbuild: true
```

### Hata 3: `[EPERM] operation not permitted, rename '...react-native' -> '...ignored_react-native'`

Bir process (node, Android Studio, Gradle) dosyayı kilitliyor. Önce tüm node process'lerini öldür:
```bash
powershell.exe -Command "Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force"
# Sonra tekrar dene
pnpm install
```

### Hata 4: `preinstall$ sh -c '...' Failed` (pnpm Windows'ta)

Root `package.json`'daki preinstall script sh ile user-agent kontrolü yapar ama Windows'ta env değişkeni gelmez. Fix:
```json
"preinstall": "node -e \"require('fs').unlinkSync('package-lock.json');require('fs').unlinkSync('yarn.lock')\" 2>nul || echo skipping"
```

### Hata 5: `Cannot determine which native SDK version your project uses because the module 'expo' is not installed`

npm ile kurulum yapıldıysa workspace yapısı bozulmuş olabilir. Expo'yu mobile projesine kur:
```bash
cd artifacts/mobile
npx expo install expo
```
Eğer `catalog:` hatası alınırsa (npm catalog protokolünü desteklemez) → yukarıdaki "npm'e geç" çözümünü uygula.

### Hata 6: Gradle `Process 'command 'node'' finished with non-zero exit value 1`

Gradle settings.gradle'daki `require.resolve` çağrıları node_modules'de paketi bulamaz. Genelde `.pnpm` klasörü silindiğinde symlink'ler gittiği için olur. Çözüm: `pnpm install` ile node_modules'u yeniden oluştur.

### Hata 7: `catalog:` Referansları (npm'e geçerken)

pnpm workspace kullanan projelerde `package.json`'da `"@tanstack/react-query": "catalog:"` gibi referanslar olabilir. Bunlar pnpm-workspace.yaml'deki catalog bölümünden versiyon alır. npm bu formatı anlamaz:
```
npm error code EUNSUPPORTEDPROTOCOL
npm error Unsupported URL Type "catalog:": catalog:
```
**Çözüm:** `pnpm-workspace.yaml`'daki catalog bölümünden versiyonları oku ve `catalog:` referanslarını gerçek versiyonlarla değiştir. Ayrıca `workspace:*` referanslarını da kaldır (npm'de workspace kavramı yok).

### Hata 8: `expo run:android` → `Process 'command 'node'' finished with non-zero exit value 1`

settings.gradle'da `require.resolve('react-native/package.json')` başarısız — node_modules'de react-native bulunamıyor. Genelde `.pnpm` klasörü silinip symlink'ler gittiğinde olur. Çözüm: `pnpm install` ile node_modules'u yeniden oluştur.

### Hata 9: Gradle `Could not resolve project :react-native-*` (Native modüller bulunamıyor)

Replit'ten gelen projelerde native modüller Windows için derlenmemiş olabilir. Çözüm:
1. `rm -rf node_modules`
2. `pnpm install` (veya `npm install --legacy-peer-deps`)
3. `npx expo prebuild --clean`
4. Tekrar build dene

## Expo Prebuild (Native Klasör Oluşturma)

Projeyi Android Studio'da açmak için önce native android/ios klasörleri gerekir:

```bash
cd artifacts/mobile
echo "y" | npx expo prebuild
```

```"


`echo "y" |` pipe'ı zorunludur — Expo CLI non-interactive ortamda `Install dependencies?` sorusunda takılır.
Çıktı: `android/` ve `ios/` klasörleri oluşur. Sonra Android Studio → Open → `artifacts/mobile/android`.

Detaylı referans: `references/expo-prebuild-interactive.md`
Ninja build fix: `references/android-ninja-build-fix.md`
Ninja build dirty fix (kapsamlı): `references/ninja-build-dirty-fix.md`
Gemini CLI process communication: `references/gemini-cli-process-communication.md`

### Pitfall'lar
- **WatermelonDB decorator hataları** (`@field`, `@relation` → TS1240) — tsc standalone hata verir ama Metro bundler ile sorunsuz çalışır. Bunları tsc hatası sanıp düzeltmeye çalışma. Metro her zaman gerçek kaynağı söyler.
- **Edge Function import'ları** (`https://deno.land/...`, `https://esm.sh/...`) vs `Deno.env` — bunlar normal TypeScript'e yabancıdır. Sadece Supabase Edge Function ortamında çalışır. tsc kontrolünde hata vermesi normaldir. Yoksay.
- **npx expo export** hata verdiğinde, ilk hataya odaklan — sonraki hatalar genelde onun zincirleme etkisidir.
- **Yanlış .env değişkenleri** proje çalışmaz — `EXPO_PUBLIC_` öneki zorunludur (Expo'nun client-side env kuralı).
- **Android build: `ninja: error: manifest 'build.ninja' still dirty after 100 tries`** — CMake object file path'i 250 karakteri aşıyor (Windows sınırı). pnpm'nin `.pnpm` iç içe klasör yapısı + uzun proje yolu (örn. `C:\\\\Users\\\\eymen\\\\Runners-Journey`) path'i limite yaklaştırır. **En etkili çözüm:** projeyi kısa bir yola taşı (örn. `C:\\\\rj`), path uzunluğunu ~20+ karakter kısalt. Alternatif: Windows Long Path desteğini aç (`reg add HKLM\\\\SYSTEM\\\\CurrentControlSet\\\\Control\\\\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f`) veya `node-linker=hoisted` ile pnpm node_modules'u düzleştir (her zaman işe yaramaz, çünkü CMake yine CMakeLists.txt içindeki relatif yolları değerlendirir). `.cxx` cache'ini temizle: `rm -rf android/app/.cxx`, ardından yeniden dene.
- **pnpm + Expo Android: preinstall script user-agent kontrolü** — root `package.json`'daki `preinstall` script'i `$npm_config_user_agent` kontrol eder ama pnpm child process'te env'i doğru aktarmaz. Çözüm: `pnpm install --ignore-scripts` ile bypass et. Sonra normal `pnpm android` çalışır.
- **pnpm workspace monorepo: doğru dizinden çalıştır** — monorepo'da Expo projesi bir workspace paketidir (örn. `artifacts/mobile`). `pnpm run:android` kök dizinde hata verir (`expo` modülü bulunamaz). Çözüm: workspace paketine gir (`cd artifacts/mobile`) ve oradan `pnpm android` veya `pnpm expo run:android` çalıştır. Veya kökten: `pnpm --filter @workspace/mobile expo run:android` — ama `expo` bir script değil direkt node_module bin olduğu için workspace root'tan çağırmak `[ERR_PNPM_RECURSIVE_RUN_NO_SCRIPT]` hatası verir. En güveniliri: direkt workspace dizinine gir.
- **expo run:android spawn'unda JAVA_HOME** — `expo run:android` gradlew'ı spawnlar ve JAVA_HOME env'ini child'a iletir. Git-bash/MSYS'de env'i inline set etmek çalışır: `JAVA_HOME="/c/Program Files/Microsoft/jdk-21.0.10.7-hotspot" pnpm android`
- **Android Studio JBR bozuk/kırık olabilir** — `jbr/lib/jvm.cfg` bulunamazsa Android Studio JBR kullanılamaz. Alternatif JDK (Microsoft JDK 21) ile devam et. `JAVA_HOME="/c/Program Files/Microsoft/jdk-21.0.10.7-hotspot"` ayarla.
- **Pre-requisite: NDK sürümü eşleşmeli** — proje belirli bir NDK sürümü ister (örn. 27.1.12297006). Android Studio → SDK Tools → "NDK (Side by side)" → Show Package Details → doğru sürümü seç → Apply. Eksik NDK ile build "Checking the license for package NDK" adımında takılır.
- **CMake path warning: 215/250 karakter sınırı** — pnpm'nin `.pnpm` iç içe yapısı uzun path'ler üretir. Uyarılar "The build may not work correctly" şeklindedir. Asıl kırıcı hata değildir ama ninja dirty error'una zemin hazırlar.
- **pnpm approve-builds hatası (`esbuild` vs.)** — ilk kurulumda `pnpm approve-builds esbuild` ile build script'ine izin ver. Yoksa `[ERR_PNPM_IGNORED_BUILDS]` hatası alınır.

## Proje Hazırlık (Eksiklik Giderme)

TS hatalarını temizledikten sonra projeyi "çalışır seviye"ye getirmek için şu adımları da uygula:

### 1. Boş test/placeholder dosyalarını temizle
```bash
rm -f test_*.py yeni_test.py
```
⚠️ .gitignore'da `test_*.py` ve `yeni_test.py` varsa silmeden önce git'ten untrack et — aksi halde git status'te görünmeye devam eder. Silinecek dosyalar `git check-ignore` ile test edilebilir.

### 2. package.json script'lerini zenginleştir
```json
"scripts": {
  "start": "expo start",
  "web": "expo start --web",
  "build:web": "expo export --platform web",
  "typecheck": "tsc --noEmit",
  "test": "echo 'No tests configured yet' && exit 1",
  "lint": "echo 'No linter configured yet' && exit 0",
  "clean": "rm -rf dist web-build .expo"
}
```

### 3. .env.example oluştur
Sensitiv olmayan referans template:
```
# .env.example
EXPO_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
```

### 4. .prettierrc ekle
```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "all",
  "printWidth": 100
}
```

### 5. README.md'yi güncelle
Mevcut durumu, nasıl başlatılacağını, proje yapısını ve komutları yansıt.

### 6. Build doğrulaması yap
```bash
npm run typecheck   # tsc --noEmit
npm run build:web   # expo export --platform web
```

## Kullanıcı'nın KiraLog Projesi Özel Notları
- Proje yolu: `/c/Users/eymen/kiralog`
- Node modules: `--legacy-peer-deps` ile kuruldu
- Expo 54, React Native 0.81, Supabase, WatermelonDB
- İki rol: owner (ev sahibi) / tenant (kiracı)
- HMK 193 uyumlu e-imza, TSA zaman damgası
- Edge functions: auth (OTP), contracts (create/sign), media (upload/timestamp), support, export
- TypeScript 0 hata, web export başarılı
