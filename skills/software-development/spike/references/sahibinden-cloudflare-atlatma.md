# Sahibinden.com Cloudflare Atlatma Denemesi (Comparison Spike)

## Problem

Sahibinden.com güçlü Cloudflare koruması kullanır. Normal `requests.get()` 403 Forbidden döner. Playwright ile dahi "Olağandışı bir durum tespit ettik" hatası alınır.

## Denenen Yöntemler (Başarısızlık Sırasına Göre)

| # | Yöntem | Sonuç | Süre |
|---|--------|-------|------|
| 1 | `requests.get()` + User-Agent header | ❌ 403 Forbidden | 0.2s |
| 2 | Playwright headless=True | ❌ Boş sayfa (body: 292 karakter) | 36s |
| 3 | Playwright + playwright-stealth `apply_stealth_sync()` | ❌ "Olağandışı durum tespit ettik" | 35s |
| 4 | Playwright headless=True + gerçek Chrome profili (`launch_persistent_context`) | ❌ Timeout (kullanıcı bilgisayarda değil) | 60s+ |
| 5 | Playwright headless=False + gerçek Chrome profili | ❌ Kullanıcı bilgisayarda değilken çalışmaz | — |

## Çıkarımlar

1. **Sahibiden dosyalarının sert bot koruması var** — Cloudflare + kendi JS challenge sistemi
2. **Playwright + stealth bile atlatamıyor** — sahibinden özellikle headless browser'ları tespit ediyor
3. **Gerçek Chrome profili** (kullanıcı oturum açıkken) en umut verici yöntem ama kullanıcı bilgisayarda değilken çalışmaz
4. **Alternatif yollar** denenmeli:
   - n8n ile HTTP Request + HTML Extract (n8n'in kendi HTTP client'i farklı fingerprint kullanabilir)
   - Google Cache / archive.org üzerinden sayfa çekmek
   - RSS feed (varsa)
   - E-posta bildirimi (sahibinden'in arama kaydetme özelliği var)
   - Farklı bir emlak sitesi (emlakjet, hepsiemlak, zingat — daha az korumalı olabilir)

## Öneri: n8n Workflow

n8n (localhost:5678'de çalışıyor) şu node'larla denenebilir:

```
Schedule (cron: 0 * * * *) 
  → HTTP Request (GET, sahibinden URL, headers ile)
  → HTML Extract (CSS selector: .searchResultsItem)
  → Function (ilan_id çıkar, JSON belleğe kaydet/yükle)
  → Telegram (yeni ilan varsa bildirim)
```

n8n'in HTTP Request node'u, sahibinden'in bot korumasını playwright'den farklı bir fingerprint ile karşılayabilir. Ancak kullanıcı bilgisayarda değilken n8n UI'a erişilemez.

## Verdict

**INVALIDATED** — Sahibinden scraping, bilgisayar başında olmayan bir kullanıcı için mevcut araç setiyle mümkün değil. Kullanıcı bilgisayara geçince n8n workflow veya gerçek Chrome profili ile tekrar denenmeli.
