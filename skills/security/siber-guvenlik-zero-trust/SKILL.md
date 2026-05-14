---
name: siber-guvenlik-zero-trust
description: Sıfır Güven (Zero Trust) Mimarisi — 6 soru-cevap. Identity-first, mikro segmentasyon, ZTNA, sürekli doğrulama.
version: 1.0
category: security
tags: [zero-trust, identity, microsegmentation, ztna, vpn]
---

# Sıfır Güven (Zero Trust) Mimarisi

## S1: Zero Trust'ın temel prensipleri neler? 'Asla güvenme, her zaman doğrula' gerçekte nasıl uygulanır?
**Cevap:** Zero Trust'ın 3 temel prensibi:
1. **Açık doğrulama:** Her erişim talebi, kaynağı ne olursa olsun (iç ağ, VPN, uzak ofis) doğrulanır.
2. **En az ayrıcalık erişimi:** Kullanıcı/sistem sadece ihtiyacı olan kaynaklara erişir.
3. **İhlal varsayımı:** Ağın zaten sızdırılmış olduğu varsayılır.
- **Uygulama:** Kullanıcı ofis içinde bile olsa, her dosya/uygulama/sunucu erişimi ayrı ayrı doğrulanır. Statik güvenlik duvarı kuralları yerine dinamik, risk bazlı politikalar kullanılır.
- **2026'da:** SentinelOne'a göre ağ çevresi öldü, kimlik yeni güvenlik duvarı.

## S2: Identity-first security nedir? Neden kimlik yeni güvenlik duvarıdır?
**Cevap:** Identity-first security, güvenlik politikalarının IP adresi veya ağ segmenti yerine kullanıcı kimliğine dayandırılmasıdır.
- **Neden:** Bulut, uzaktan çalışma ve hibrit ağlarda fiziksel ağ sınırları kayboldu. Kullanıcının nereden bağlandığı değil, kim olduğu önemli.
- **Nasıl çalışır:**
  - Her oturumda: kullanıcı kimliği + cihaz sağlığı + konum + davranış kalıbı doğrulanır
  - Risk puanı düşükse yetkilendirme otomatik, yüksekse ek doğrulama
- **2026 trendi:** Splunk, biyometrik + risk bazlı kimlik doğrulamanın standart haline geldiğini belirtiyor. Parolaların yerini passkeys ve biyometri alıyor.

## S3: Mikro segmentasyon: Ağ içinde yanal hareket nasıl engellenir?
**Cevap:** Mikro segmentasyon, ağı çok küçük mantıksal bölümlere ayırarak bir saldırganın sızdıktan sonra yanal hareketini kısıtlar.
- **Nasıl çalışır:**
  - Her uygulama/sunucu grubu kendi segmentinde
  - Segmentler arası geçiş için ayrı yetkilendirme
  - Bir segment ihlal edilirse diğerlerine geçilemez
- **Gerçek dünya örneği:** Bir finans kuruluşunda, müşteri veritabanı ile ödeme sistemi aynı ağda değil. Saldırgan müşteri verilerine sızsa bile ödeme sistemine erişemez.
- **Araçlar:** VMware NSX, Cisco ACI, Illumio.
- **Zorluk:** Eski uygulamalar segmentasyon için yeniden mimari gerektirebilir.

## S4: Zero Trust'da sürekli doğrulama nasıl çalışır?
**Cevap:** Sürekli doğrulama, sadece login'de değil, tüm oturum boyunca güveni kontrol eder.
- **Kontrol edilen sinyaller:**
  - Cihaz sağlığı: Antivirüs güncel mi? Disk şifreleme aktif mi? İşletim sistemi güncel mi?
  - Konum: Kullanıcı normalde İstanbul'dan bağlanırken birden Rusya'dan mı bağlandı?
  - Davranış kalıbı: Normalde saat 9-18 arası çalışan kullanıcı gece 3'te mi veritabanına erişiyor?
- **Sonuç:** Risk puanı eşiği aşılırsa oturum otomatik sonlandırılır, MFA istenir veya erişim engellenir.
- **2026 trendi:** Artık statik politika yerine gerçek zamanlı risk sinyalleri (cihaz, konum, davranış) kullanılıyor.

## S5: Zero Trust adaptasyonundaki en büyük engeller nelerdir?
**Cevap:**
1. **Eski sistemler:** 10+ yıllık uygulamalar Zero Trust ile uyumlu değil. Modernizasyon maliyetli ve riskli.
2. **Karmaşıklık:** Her erişim talebi için ayrı politika tanımlamak büyük ölçekte zor.
3. **Kullanıcı deneyimi:** Sürekli doğrulama kullanıcılar tarafından 'angarya' olarak görülebilir.
4. **Maliyet:** Zero Trust altyapısı (kimlik sağlayıcı, mikro segmentasyon, sürekli izleme) pahalı.
5. **Beceri eksikliği:** Zero Trust mimarisi kurabilecek uzman sayısı sınırlı.
6. **Kültürel direnç:** 'İç ağ güvenlidir' zihniyetini değiştirmek zaman alır.

## S6: ZTNA ile geleneksel VPN arasındaki farklar neler?
**Cevap:**
| Özellik | VPN | ZTNA |
|---------|-----|------|
| Erişim modeli | Ağa tam erişim | Sadece belirli uygulamaya |
| Doğrulama | Login'de bir kere | Sürekli (oturum boyunca) |
| Risk | Sızan kullanıcı tüm ağa erişir | Sızan kullanıcı tek uygulamaya takılır |
| Kurulum | Donanım/yazılım gerektirir | Bulut tabanlı, hızlı kurulum |
| Performans | Tüm trafik merkezden geçer | Edge'de sonlandırma, düşük gecikme |
| 2026 trendi | ZTNA, VPN'in yerini hızla alıyor | |
