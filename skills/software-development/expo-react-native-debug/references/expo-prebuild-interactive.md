# Expo Prebuild İnteraktif Mod Sorunları

## Sorun: "Input is required, but 'npx expo' is in non-interactive mode"

Expo CLI (SDK 52+) non-interactive ortamlarda `Install the updated dependencies?` sorusunda takılır.

### Çözüm: stdin pipe

```bash
echo "y" | npx expo prebuild
```

### Ön Koşul

```bash
pnpm install   # veya npm install
```

Eğer pnpm kullanılıyorsa ve `preinstall` scripti user-agent kontrolü yapıyorsa:

```bash
pnpm install --ignore-scripts   # preinstall script'ini bypass
echo "y" | npx expo prebuild
```

### Alternatif: --yes flag (çalışmıyor)

`npx expo prebuild --yes` Expo CLI tarafından tanınmaz. Geçerli flag'ler için `npx expo prebuild --help`.

### Neden Olur

- CI/CD ortamları (GitHub Actions, vs.)
- Agent/headless terminal (Hermes gibi)
- `echo "y" |` pipe edilmeyen her terminal oturumu

### Doğrulama

```bash
ls android/   # app/, build.gradle, settings.gradle vs.
```
