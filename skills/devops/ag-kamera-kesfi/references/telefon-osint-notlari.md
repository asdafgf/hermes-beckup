# Telefon Numarasından OSINT — Ne Mümkün, Ne Değil

## Herkese Açık Kaynaklardan Ulaşılabilecekler
- **Google araması** — numara tırnak içinde aratılırsa, halka açık sitelerde paylaşılmışsa çıkar (ilan siteleri, forumlar, rehberler)
- **Operatör öneki** — 053x Turkcell, 054x Vodafone, 050x TT, 055x Turkcell (taşınabilirlik var, %100 güvenilir değil)

## Kapalı/Gri Kaynaklar
- **Truecaller API** — rehberi senkronize eden kullanıcıların verilerinden oluşur. API'si yok, mobil uygulama gerekir.
- **WhatsApp/Telegram** — rehberde kayıtlıysa profil ismi görünür. API'si yok.
- **Veri sızıntısı veritabanları** — HIBP, leakcheck, snusbase, intelx. Bazıları yasal API sunar, bazıları gri alan.
- **HVPH/HVI** — Türk hack forumları, çalıntı veritabanları.

## Telefon Numarasından Ulaşılamayanlar (Doğrudan)
- **TC Kimlik No** — telefon-TC eşleştirmesi resmi olarak yok
- **Ev adresi** — sadece e-ticaret/operatör veri sızıntılarında birlikte geçiyorsa
- **Ad-soyad** — Truecaller dışında doğrudan yöntem yok

## Yasal OSINT Araçları
- `haveibeenpwned.com` — e-posta sorgulama (telefon için abonelik gerekli)
- `intelx.io` — çok kaynaklı tarama (ücretsiz limitli)
- `leak-lookup.com` — veri sızıntısı arama motoru
- Trend Micro ID Protection (ücretsiz leak checker)
