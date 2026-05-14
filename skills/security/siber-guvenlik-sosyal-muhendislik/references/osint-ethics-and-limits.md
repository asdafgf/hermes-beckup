# OSINT Etik Sınırları ve Telefon Numarası Sorgulama

## Genel Kural

- **Kullanıcının kendi verisi** her zaman sorgulanabilir — suç değildir.
- **Başkasının verisi** izinsiz sorgulanamaz — KVKK/TCK suçu.
- **Herkese açık kaynaklar** (Google, sosyal medya, forumlar) her zaman taranabilir.

## Kendi Telefon Numaranı Sorgulama

Yasal yöntemler:
1. **Google araması** — `"0539XXXXXXX"` tırnak içinde arat
2. **Have I Been Pwned** — e-posta için çalışır, telefon için sınırlı
3. **Firefox Monitor** — ücretsiz sızıntı kontrolü
4. **Trend Micro ID Protection** — ücretsiz leak checker
5. **Telegram leak check botları** — gri alan ama kendi numaran için suç değil

## Sızıntı Veritabanları

- **IntelX** — yasal API, kendi verini sorgulayabilirsin
- **LeakCheck / Snusbase** — gri alan, kendi verin için kullanılabilir
- **HIBP API** — ücretsiz ama telefon için abonelik gerekir

## Truecaller ve Kapalı Veritabanları

Truecaller crowdsourced bir veritabanıdır. API'si yoktur. Truecaller'da kayıtlı olup olmadığını görmek için:
- Truecaller uygulamasını yükle (kendin bak)
- Web arayüzü sınırlı

## Önemli Uyarı

- Bir numaranın internette hiçbir yerde görünmemesi İYİDİR
- Sızıntı veritabanlarında bile çıkmaması en iyi senaryo
- WhatsApp/Telegram'da kayıtlı olmak, o platformların kullanıcılarının seni bulabileceği anlamına gelir (gizlilik ayarlarıyla kontrol edilebilir)
