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

### Pitfall'lar
- **WatermelonDB decorator hataları** (`@field`, `@relation` → TS1240) — tsc standalone hata verir ama Metro bundler ile sorunsuz çalışır. Bunları tsc hatası sanıp düzeltmeye çalışma. Metro her zaman gerçek kaynağı söyler.
- **Edge Function import'ları** (`https://deno.land/...`, `https://esm.sh/...`) vs `Deno.env` — bunlar normal TypeScript'e yabancıdır. Sadece Supabase Edge Function ortamında çalışır. tsc kontrolünde hata vermesi normaldir. Yoksay.
- **npx expo export** hata verdiğinde, ilk hataya odaklan — sonraki hatalar genelde onun zincirleme etkisidir.
- **Yanlış .env değişkenleri** proje çalışmaz — `EXPO_PUBLIC_` öneki zorunludur (Expo'nun client-side env kuralı).

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
