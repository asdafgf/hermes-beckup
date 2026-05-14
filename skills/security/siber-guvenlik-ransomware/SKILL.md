---
name: siber-guvenlik-ransomware
description: Ransomware ve Fidye Yazılımları — 6 soru-cevap. Double extortion, 3-2-1 yedekleme, RaaS, sağlık sektörü.
version: 1.0
category: security
tags: [ransomware, backup, raas, double-extortion, healthcare-security]
---

# Ransomware ve Fidye Yazılımları

## S1: Ransomware 2026'da nasıl evrildi? Çifte ve üçlü şantaj yöntemleri neler?
**Cevap:** Ransomware 2026'da çok katmanlı gasp taktiklerine evrildi:
- **Çifte şantaj (Double Extortion):** 1) Verileri şifrele 2) Şifre çözme anahtarı için fidye iste 3) Ödenmezse verileri sızdır.
- **Üçlü şantaj (Triple Extortion):** 1+2+3) Müşterilere/hissedarlara verilerin sızdırılacağını bildirerek itibar baskısı yap.
- **Dörtlü şantaj:** Yukarıdakilere ek olarak, DDoS saldırısı ile şirketi çökertme tehdidi.
- **2026 trendi:** Saldırganlar fidye ödenmezse verileri doğrudan rakiplere satıyor.
- **Hedefler:** Sağlık, eğitim, kamu ve kritik altyapı en çok hedef alınanlar.

## S2: Ransomware saldırılarına karşı dayanıklılık stratejileri — 'Önlemeden kurtulmaya geçiş' ne anlama geliyor?
**Cevap:** 2026'da siber güvenlik stratejisi 'duvarları yükseltmek' yerine 'saldırıdan kurtulmak'a kayıyor.
- **Eski yaklaşım:** Güvenlik duvarı, antivirüs, IDS/IPS → saldırganı dışarıda tutmaya odaklı.
- **Yeni yaklaşım:** Saldırganın içeri gireceğini varsay → tespit hızı ve kurtarma kabiliyetine odaklan.
- **Önemli metrik:** 'Tespit süresi' değil, 'düzeltme süresi' (Time to Remediate).
- **Yatırım:** Yeni güvenlik duvarı yerine yedekleme altyapısı ve çevrimdışı kurtarma sistemlerine bütçe.
- **2026'da:** Kurullar güvenlik duvarı yükseltmesinden önce çevrimdışı yedekleme bütçesini onaylıyor.

## S3: 3-2-1 yedekleme kuralı ve ransomware'a karşı etkili yedekleme stratejileri neler?
**Cevap:** 3-2-1 yedekleme kuralı:
- **3:** Verinin 3 kopyası (1 ana + 2 yedek)
- **2:** 2 farklı medya türü (ör. SSD + harici disk)
- **1:** 1 kopya çevrimdışı / farklı fiziksel konumda
- **Ransomware için ek önlemler:**
  - **Immutable (değiştirilemez) yedekler:** Saldırgan yedekleri silemez
  - **Air-gapped (çevrimdışı) yedekler:** Ağa bağlı olmayan yedekler
  - **3-2-1-1-0 kuralı:** 1 immutable + 0 hata (doğrulama ile)
  - Düzenli kurtarma testi (en az ayda bir)
- **Bulut yedek:** Object lock özellikli bulut depolama (AWS S3 Object Lock, Azure Blob immutability).

## S4: Ransomware fidyesi ödenmeli mi? Hükümetlerin tutumu nedir?
**Cevap:** Hükümetlerin ve kolluk kuvvetlerinin resmi tutumu:
- **ABD:** CISA ve FBI resmi olarak 'fidye ödemeyin' diyor. Ödeme saldırganları cesaretlendirir.
- **AB:** Europol ve ENISA de ödemeyi önermiyor.
- **Türkiye:** Resmi bir politika yok ancak kamu kurumlarının ödeme yapması yasal olarak sorunlu.
- **Gerçek dünya:** Şirketlerin %60'ı hala ödeme yapıyor (2026 verisi).
- **Ödeme yapılırsa:**
  - Verilerin geri geldiğinin garantisi yok (ortalama %70-80 iade oranı)
  - Aynı saldırgan tekrar hedef alabilir
  - OFAC (ABD) yaptırım listesindeki gruplara ödeme yapmak yasa dışı olabilir
- **Öneri:** Ödeme yapma kararını hukuk + siber güvenlik + yönetim kurulu birlikte almalı.

## S5: Ransomware-as-a-Service (RaaS) nasıl işliyor?
**Cevap:** RaaS, karanlık ağda organize suç ekonomisinin bir parçası:
- **İş modeli:**
  - Geliştirici: Ransomware yazılımını yazar (ör. LockBit, BlackCat, REvil)
  - İştirakçı (affiliate): Saldırıyı gerçekleştirir
  - Kar paylaşımı: Geliştirici %20-30, iştirakçı %70-80
- **Hizmetler:**
  - Hazır kötü amaçlı yazılım (customize edilebilir)
  - Sızıntı siteleri (verileri yayınlamak için)
  - Müzakere hizmeti (fidye pazarlığını yönetir)
  - Kripto para aklama hizmeti
- **2026'da:** RaaS çeteleri profesyonel şirketler gibi yönetiliyor: çağrı merkezi, müşteri hizmetleri, güvenlik açığı raporlama programları.

## S6: Sağlık sektöründe ransomware — hastaneler neden en çok hedef?
**Cevap:** Sağlık sektörü ransomware için ideal hedef:
- **Neden:**
  - Kritik sistemler (hasta verileri, ameliyat planlaması) — duruş kabul edilemez
  - Eski sistemler (tıbbi cihazlar, Windows 7, yamalanmamış sunucular)
  - Yüksek veri değeri (sağlık kayıtları kara borsada en pahalı veri)
  - Düşük siber güvenlik bütçesi
- **Maliyet:** Sağlık sektöründe ortalama veri ihlali maliyeti 9,77 milyon dolar (IBM/Ponemon).
- **Örnek:** 2024'te Change Healthcare saldırısı — ABD sağlık sistemini haftalarca etkiledi.
- **Önlemler:** Tıbbi cihaz envanteri, ağ segmentasyonu (IT/OT ayrımı), düzenli yedekleme, HIPAA uyumu.
