# Reproduction Recipe: Nested Dir 404

## Ortam
- Windows 11 + WSL2 Ubuntu
- Docker Engine WSL içinde (no Desktop)
- Supabase CLI v2.98.2
- Supabase local v2.x
- Edge Runtime v1.73.13 (Deno v2.1.4)

## Belirtiler
- `npx supabase functions serve` yanıt veriyor: `Serving functions on http://.../functions/v1/<function-name>`
- Edge-runtime container log'unda yalnızca `<function-name>` placeholder'ı, gerçek isim yok
- `curl -X POST http://127.0.0.1:54321/functions/v1/auth/otp-request` → HTTP 404
- Kong gateway route'ları fonksiyonları görmüyor

## Teşhis Adımları
1. Edge-runtime container log'unda route listesini kontrol et:
   ```bash
   docker logs supabase_edge_runtime_kiralog --tail 50
   ```
2. Beklenen fonksiyonları bul:
   ```bash
   find /root/kiralog/supabase/functions -name 'index.ts' ! -path '*/_shared/*'
   ```
3. HTTP test:
   ```bash
   curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:54321/functions/v1/auth/otp-request
   ```
4. Edge-runtime iç kodu (Deno) route mantığı:
   ```typescript
   // functionName = pathParts[1] — yalnızca ilk segment alınır
   // `auth/otp-request` → functionName = "auth", "otp-request" kaybolur
   const functionName = pathParts[1];
   if (!functionName || !(functionName in functionsConfig)) {
     return getResponse("Function not found", STATUS_CODE.NotFound);
   }
   ```

## Çözüm
Flat dizin yapısı. Bu skill'deki adımları uygula.

## Doğrulama
```
otp-request       → 401 ✓ (auth gerekli — fonksiyon çalışıyor)
auth-otp-verify   → 401 ✓
...
```

Not: 401 = başarı (JWT auth bekliyor). 404 = hata (route yok).
