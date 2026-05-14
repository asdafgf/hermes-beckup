---
name: siber-guvenlik-tedarik-zinciri
description: Tedarik Zinciri ve Üçüncü Taraf Güvenliği — 6 soru-cevap. SBOM, Log4j, API saldırıları, tedarikçi denetimi.
version: 1.0
category: security
tags: [supply-chain, sbom, third-party, log4j, api-security, vendor-risk]
---

# Tedarik Zinciri ve Üçüncü Taraf Güvenliği

## S1: Tedarik zinciri saldırıları neden 2026'nın en büyük tehditlerinden biri?
**Cevap:** Tek bir küçük tedarikçinin zafiyeti, binlerce müşteriyi etkileyebilir. WEF Global Cybersecurity Outlook 2026'ya göre tedarik zinciri zafiyetleri en büyük endişe kaynağı (%78).
- **Neden büyük tehdit:**
  - Şirketler yüzlerce tedarikçi ile çalışır — hepsini denetlemek imkansıza yakın
  - Saldırganlar 'en zayıf halka' stratejisiyle büyük şirketlere tedarikçi üzerinden sızar
  - SolarWinds benzeri saldırılar: 18.000 müşteri etkilendi
- **2026'da:** Yeni düzenlemeler şirketlerin tüm tedarikçilerinin güvenlik süreçlerini denetlemesini zorunlu kılıyor.
- **Sözleşme maddeleri:** Tedarikçi saldırıya uğrarsa, müşteri şirket tedarikçinin sistemlerini anında denetleyebilir.

## S2: SBOM (Software Bill of Materials) nedir ve neden önemli?
**Cevap:** SBOM, bir yazılım ürününde kullanılan tüm bileşenlerin, kütüphanelerin ve bağımlılıkların listesidir.
- **Önemi:**
  - Log4j gibi bir zafiyet çıktığında, hangi ürünlerin etkilendiğini anında tespit edebilirsin
  - Tedarikçi değerlendirmesini hızlandırır
  - Yasal uyumluluk için gerekli (ABD 'Executive Order on Cybersecurity')
- **2026'da:** Dijital Malzeme Listesi (SBOM) birçok sektörde zorunlu hale geliyor.
- **Nasıl oluşturulur:** Her derleme (build) sırasında otomatik oluşturulur (SPDX veya CycloneDX formatında).
- **Saldırı durumunda:** SBOM sayesinde hangi ürünlerin güncellenmesi gerektiği dakikalar içinde belirlenir.

## S3: Açık kaynak kütüphane güvenliği — Log4j benzeri bir zafiyet tekrar ortaya çıkarsa ne yapmalı?
**Cevap:** Log4j (CVE-2021-44228) benzeri bir zafiyet durumunda:
- **Anlık (ilk 1 saat):**
  1. SBOM'u kontrol et — hangi ürünler etkileniyor?
  2. Saldırı yüzeyini değerlendir — etkilenen sistemler internete açık mı?
  3. Geçici önlem: WAF kuralları ekle, JNDI lookup'ı devre dışı bırak
- **Kısa vade (ilk 24 saat):**
  4. Tedarikçilerle iletişime geç — yama ne zaman geliyor?
  5. Etkilenen sistemleri segmentlere ayır
  6. Geçici yama uygula
- **Uzun vade:**
  7. Kalıcı yamayı test et ve dağıt
  8. Kütüphane kullanım politikasını gözden geçir
  9. SCA (Software Composition Analysis) aracını kur
- **Önleyici:** Düzenli SCA taraması, güncel kütüphane takibi, otomatik bağımlılık güncellemesi (Dependabot, Renovate).

## S4: Tedarikçi denetim sözleşmeleri 2026'da nasıl değişti?
**Cevap:** 2026'da tedarikçi sözleşmelerinde yeni güvenlik maddeleri standart hale geldi:
- **Anlık denetim yetkisi:** Müşteri, tedarikçinin sistemlerini haber vermeksizin denetleyebilir.
- **Bilgi paylaşımı zorunluluğu:** Tedarikçi saldırıya uğrarsa 24 saat içinde bildirmek zorunda.
- **Ceza maddeleri:** Bilgi paylaşımında gecikme veya yetersiz güvenlik için maddi yaptırımlar.
- **Sigorta şartı:** Tedarikçinin siber sigortası olmalı.
- **Liderlik beyanı:** Tedarikçinin CEO/CISO'su, güvenlik kontrollerinin varlığını yeminli olarak beyan eder.
- **Veri sorumluluğu:** Tedarikçideki veri ihlalinde, sözleşmede hangi tarafın sorumlu olduğu net olarak belirtilir.

## S5: API tedarik zinciri saldırıları — Wallarm'a göre %97 tek istekle gerçekleşiyor, neden?
**Cevap:** Wallarm araştırmasına göre API saldırılarının %97'si sadece bir API isteği ile gerçekleşiyor.
- **Nedenleri:**
  - **Broken Object Level Authorization (BOLA):** Kullanıcı kendi ID'sini değiştirip başkasının verisine erişir
  - **Kimlik doğrulama eksikliği:** Public API'lerde auth olmaması
  - **Rate limiting yok:** Saldırgan milyonlarca istekle sistemi çökertir
  - **API key sızıntısı:** GitHub'da açıkta kalan API anahtarları
- **2026 trendi:** AI ajanları API'leri makine hızında tarayarak insan gözünün bulamayacağı zafiyetleri keşfediyor.
- **Örnek:** ServiceNow BodySnatcher — bir API tanımlama zafiyeti üzerinden tam sistem işgali.
- **Çözüm:** API güvenlik taraması, runtime davranışsal izleme, işlemsel yetkilendirme.

## S6: Küçük bir tedarikçinin zafiyeti büyük bir şirketi nasıl çökertir?
**Cevap:** Gerçek senaryo:
1. Büyük şirket X, küçük bir SaaS sağlayıcısı Y'yi kullanıyor (ör. izin yönetimi)
2. Y şirketi temel güvenlik önlemlerini almamış (güncelleme yok, MFA yok, zayıf şifre)
3. Saldırgan Y'ye sızarak X'in sistemlerine geçiş anahtarı bulur
4. X'in tüm müşteri verilerini çalar
5. Sonuç: Milyonlarca dolar hasar, itibar kaybı, dava
- **2026'da:** Yeni regülasyonlar büyük şirketleri tüm tedarikçilerinin güvenlik seviyesinden sorumlu tutuyor.
- **Çözüm:** Tedarikçi risk puanlaması, sürekli izleme, SBOM zorunluluğu, sözleşmelerde denetim maddeleri.
