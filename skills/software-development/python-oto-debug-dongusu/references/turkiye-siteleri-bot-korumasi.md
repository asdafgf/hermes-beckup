# Türkiye Sitelerinde Bot Koruması Atlatma Referansı

Bu referans, Türkiye'deki büyük sitelerin (sahibinden.com, hepsiburada, trendyol vb.) bot korumaları karşısında alınan dersleri içerir.

## Durum: sahibinden.com (Mayıs 2026)

### Koruma Seviyesi
- **En ağır:** Cloudflare + özel bot tespiti
- **requests + User-Agent:** 403 Forbidden
- **requests + tüm header'lar:** 403 Forbidden
- **Playwright headless:** "Olağandışı bir durum tespit ettik" sayfası
- **Playwright + playwright-stealth.Stealth().apply_stealth_sync():** Yine engellendi
- **Playwright + gerçek Chrome profili (launch_persistent_context):** Çalışabilir ama kullanıcı bilgisayarda değilken headless=False timeout yiyor

### Çalışan Yaklaşımlar (sıralı tercih)

| Yaklaşım | Açıklama | Durum |
|---|---|---|
| **n8n workflow** | n8n 2.19.5 bilgisayarda çalışıyor (localhost:5678). HTTP Request + HTML Extract + Telegram node'ları ile scraping yapılabilir | ✅ **En pratik** — ama kullanıcı bilgisayarda değilken yapılandırılamaz |
| **Gerçek Chrome profili** | `playwright.chromium.launch_persistent_context(user_data_dir=..., headless=False)` — kullanıcının oturum açık Chrome'unu kullanır | ⚠️ Bilgisayar açıkken çalışır, kullanıcı yokken headless=False timeout |
| **E-posta bildirimi** | Sahibinden'in "aramayı kaydet → e-posta bildirimi" özelliği var. E-postayı Himalaya CLI ile okumak | ✅ En stabil — scraping gerektirmez |
| **RSS/Atom** | Sahibinden'in resmi RSS beslemesi yok | ❌ |
| **Google Cache/Önbellek** | `webcache.googleusercontent.com` üzerinden sayfa önbelleğini çekmek | ⚠️ Nadiren güncel |

### Gelecek İçin Ders

Sahibinden gibi bot korumalı sitelerde:
1. Önce **site-specific API** veya **e-posta bildirimi** kontrol et
2. Yoksa **n8n** ile HTTP Request + HTML Extract dene (n8n kendi User-Agent'ını yönetir)
3. Olmazsa **gerçek Chrome profili** ile Playwright dene
4. En son çare: **başka bir site** (emlakjet, hepsiemlak, zingat) kullan — daha az korumalı olabilir

### Kullanıcı Durumu

Eymen bilgisayarda değil. Sahibinden izleyici için:
- `scripts/` ve `scraper.py` hazır
- `bellek.json` mekanizması (mükerrer ilan engelleme) çalışıyor
- Cronjob saatte bir çalışacak şekilde ayarlanabilir (`0 * * * *`)
- **Bilgisayara geçince n8n workflow'u kurulacak** — en pratik çözüm
