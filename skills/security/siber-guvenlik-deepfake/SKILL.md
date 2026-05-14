---
name: siber-guvenlik-deepfake
description: Deepfake ve Kimlik Aldatmacası — 5 soru-cevap. Gerçek zamanlı deepfake, CP2A standardı, biyometrik doğrulama, güven kodu.
version: 1.0
category: security
tags: [deepfake, identity, biometrics, cp2a, social-engineering]
---

# Deepfake ve Kimlik Aldatmacası

## S1: Gerçek zamanlı deepfake nedir ve 2026'da hangi seviyeye ulaştı?
**Cevap:** Gerçek zamanlı deepfake, bir kişinin yüzünü ve sesini canlı video görüşmesinde anında taklit edebilen AI teknolojisidir.
- **2026 seviyesi:** Artık önceden kaydedilmiş video gerektirmez. Tek bir fotoğraf ve 3 saniyelik ses kaydı yeterli.
- **Kullanım:** Zoom toplantılarında CFO'yu taklit ederek para transferi talep etme, uzaktan işe alımda kimlik doğrulamayı atlatma.
- **Tespit zorluğu:** Çıplak gözle ayırt etmek neredeyse imkansız. SentinelOne'a göre video ve ses artık güvenilir doğrulama yöntemi değil.
- **İstatistik:** 2026'da deepfake kaynaklı dolandırıcılık vakaları bir önceki yıla göre %300 arttı.

## S2: Deepfake ile işe alım dolandırıcılığı nasıl yapılıyor?
**Cevap:** Uzaktan çalışma modelinin yaygınlaşmasıyla deepfake işe alım dolandırıcılığı 2026'da büyük bir tehdit haline geldi:
- **Yöntem:** Saldırgan, gerçek bir kişinin kimliğini kullanarak (çalınan kimlik + deepfake video) işe başvurur.
- **Mülakat:** Canlı video görüşmede deepfake ile kimliğe bürünür.
- **Sızma:** İşe girince şirket iç ağına, müşteri verilerine, finansal sistemlere erişir.
- **Sonuç:** Veri sızıntısı, dolandırıcılık, endüstriyel casusluk.
- **Çözüm:** Çok kanallı doğrulama (video + ayrı telefon onayı), fiziksel kimlik doğrulama, liveness detection.

## S3: Deepfake tespit yöntemleri ve CP2A standardı nedir?
**Cevap:** Deepfake tespit yöntemleri:
- **AI tabanlı analiz:** Video/seste AI ile üretilmiş eserleri tespit eden modeller.
- **Çoklu kanal analizi:** Ses, video ve davranışsal ipuçlarını aynı anda çapraz analiz eder.
- **CP2A Standardı (Content Provenance and Authenticity):** Resmi medyaya kurcalamaya dayanıklı dijital imzalar ekler. Bir görüntü/videonun nerede, ne zaman, hangi cihazla çekildiğini doğrular.
- **2026'da:** CP2A, finans ve sağlık sektöründe zorunlu hale geliyor.
- **Sınırlama:** Tek kanal tespit sistemleri (sadece ses veya sadece video) yetersiz kalıyor. Çapraz doğrulama şart.

## S4: Biyometrik doğrulama ve liveness detection deepfake'i yenebilir mi?
**Cevap:** Liveness detection, canlı bir insanla karşı karşıya olunduğunu doğrulayan biyometrik sistemdir.
- **Gelişmiş yöntemler:**
  - Yüzdeki kan akışı ve nabız desenlerini analiz etme
  - Derinlik algılama (3D kameralar)
  - Rastgele talimatlara tepki (başını çevir, gülümse)
  - Termal görüntüleme
- **Başarı durumu:** 2026'da en gelişmiş liveness sistemleri deepfake'in çoğu formunu tespit edebiliyor.
- **Zayıf nokta:** Önceden kaydedilmiş yanıt videoları ve yüksek kaliteli 3D maskeler bazı sistemleri hala atlatabiliyor.
- **Öneri:** Çok faktörlü biyometri + insan denetçi + güven kodu kombinasyonu.

## S5: Güven kodu ve günlük gizli ifadelerle yönetici kimliğine bürünme nasıl önlenir?
**Cevap:** 'Güven kodu' sistemi, yönetici kimliğine bürünmeye karşı 2026'da standart hale geliyor:
- **Çalışma şekli:** Her gün değişen gizli bir ifade veya sayı kodu. Yönetici ile çalışan arasında önceden belirlenir.
- **Kullanım:** Yüksek riskli işlemlerde (para transferi, veri erişimi, şifre sıfırlama) güven kodu sorulur.
- **Çok kanallı doğrulama:** Video görüşmede kod sorulur, ardından farklı bir kanaldan (SMS, ayrı telefon hattı) doğrulama yapılır.
- **2026 trendi:** Şirketler finansal işlemlerde ek kanal doğrulamasını (video + telefon geri arama) prosedür haline getiriyor.
- **Kural:** Acil para transferi taleplerinde daima ayrı bir doğrulanmış numaradan geri ara.
