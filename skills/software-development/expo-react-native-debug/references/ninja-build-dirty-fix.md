# Ninja "build.ninja still dirty after 100 tries" — Windows Fix Recipe

## Tanı

CMake/Ninja C++ derlemesi sırasında:
```
ninja: error: manifest 'build.ninja' still dirty after 100 tries
```
veya:
```
ninja: error: mkdir(src/...): No such file or directory
ninja: error: Stat(...): Filename longer than 260 characters
```

## Sebep

Windows'ta CMake object file path'i 250 karakter sınırını aşıyor.
pnpm'nin `.pnpm/@package@version/node_modules/...` iç içe yapısı + proje yolu toplamda limiti aşar.
Özellikle: `react-native-screens`, `react-native-worklets`, `expo-modules-core` gibi C++ native modüller bu sınıra takılır.

## Çözüm Hiyerarşisi (en etkiliden en zayıfa)

### Seviye 1: LongPathsEnabled + Git longpaths + Reboot ✅ KALICI

```cmd
reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f
git config --system core.longpaths true
```
→ Bilgisayarı yeniden başlat
→ `gradlew clean && npx expo run:android`

### Seviye 2: Projeyi kısa yola taşı (C:\Users\... vb uzunsa)

```cmd
# Örn: C:\Users\eymen\runners-journey → C:\rj
cmd /c rename "C:\Users\eymen\runners-journey" rj
```
Eğer Permission denied alınırsa:
1. Tüm node process'lerini öldür: `powershell "Get-Process node | Stop-Process -Force"`
2. .cxx, .gradle cache'lerini temizle
3. Tekrar dene
4. Son çare: `write_file` ile yeni dizine dosyaları teker kopyala

### Seviye 3: pnpm node_modules'u düzleştir

```bash
echo "node-linker=hoisted" > .npmrc
echo "shamefully-hoist=true" >> .npmrc
rm -rf node_modules .pnpm-store
pnpm install
npx expo prebuild --clean
```

### Seviye 4: npm'e geç (pnpm'den tamamen kurtul)

pnpm workspace'in `.pnpm` iç içe yapısı sorun çıkarıyorsa:

```python
# package.json'daki catalog: referanslarını gerçek versiyonlarla değiştir
# pnpm-workspace.yaml'daki catalog bölümünden oku:
catalog = {
    "@tanstack/react-query": "^5.90.21",
    "react": "19.1.0",
    "react-dom": "19.1.0",
    "zod": "^3.25.76"
}
# workspace:* referanslarını kaldır
# pnpm-workspace.yaml + pnpm-lock.yaml sil
# npm install --legacy-peer-deps
# npx expo prebuild --clean
```

### Seviye 5: .cxx klasörünü junction yap

```cmd
rmdir /s artifacts/mobile/android/.cxx
mklink /J artifacts/mobile/android/.cxx C:\rj\.cxx_short
```

Not: Junction tek başına yeterli olmayabilir çünkü CMake yine .pnpm içindeki kaynak dosya yolunu kullanır.

## Doğrulama

Build başarılı olduğunda APK şurada oluşur:
```
artifacts/mobile/android/app/build/outputs/apk/debug/app-debug.apk
```

## Uyarılar

- `--rerun-tasks` Gradle cache'ini bypass eder ama CMake build.ninja script'leri önbellekte kalabilir
- .pnpm klasörünü silmek react-native/expo gibi önemli paketlerin symlink'lerini de kaldırır — settings.gradle'daki require.resolve başarısız olur
- npm'e geçişte `workspace:*` referansları kırılır — elle kaldırılmalı
