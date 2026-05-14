---
name: siber-guvenlik-api
description: API Güvenliği ve Modern Web Tehditleri — 5 soru-cevap. BOLA, runtime monitoring, WAF, GraphQL.
version: 1.0
category: security
tags: [api-security, bola, waf, graphql, runtime-monitoring]
---

# API Güvenliği ve Modern Web Tehditleri

## S1: API güvenliği neden 2026'da en kritik konulardan biri? BOLA nedir?
**Cevap:** API'ler modern uygulamaların omurgası — her mobil uygulama, web sitesi ve mikroservis API'lerle çalışır.
- **Neden kritik:** API'ler en çok sömürülen saldırı yüzeyi. 97%'si tek istekle gerçekleşiyor (Wallarm).
- **BOLA (Broken Object Level Authorization):** En yaygın API zafiyeti. Kullanıcı /api/users/12345 çağırırken 12345'i 67890 yapıp başkasının verisine erişir.
- **2026 istatistiği:** API zafiyetleri raporlanan tüm ihlallerin %36'sını oluşturuyor.
- **Çözüm:** Her API isteğinde kullanıcı yetkilendirmesi, UUID kullanımı, rate limiting, şema doğrulama.

## S2: AI ajanları API'leri nasıl tarar ve sömürür?
**Cevap:** 2026'da AI ajanları API saldırılarını makine hızında gerçekleştiriyor:
- **Tarama:** AI ajanı API endpoint'lerini keşfeder (Swagger/OpenAPI, ortak desenler)
- **Test:** Her endpoint'te parametre manipülasyonu, auth bypass, injection dener
- **Sömürü:** ServiceNow BodySnatcher örneği — bir API tanımlama zafiyeti üzerinden ajan kendi kendine administrator yetkisi alır
- **Hız:** İnsanın saatler süren testini AI ajanı saniyelerde tamamlar
- **Savunma:** Runtime davranışsal izleme, anomali tespiti, işlemsel yetkilendirme (transactional authorization)

## S3: Runtime behavioral monitoring — statik güvenlik duvarları neden yetmez?
**Cevap:** Statik WAF kuralları (imza tabanlı) AI tarafından üretilen polimorfik saldırıları tespit edemez.
- **Runtime monitoring:** API isteklerinin sadece içeriğini değil, bağlamını ve davranışını da analiz eder.
  - Normalde 10 istek/dk yapan kullanıcı birden 1000 istek/dk mı yapıyor?
  - Aynı API'ye 3 farklı IP'den aynı anda mı erişiliyor?
  - Şifre sıfırlama API'sine 1 dakikada 500 istek mi geliyor?
- **Transaction authorization:** Her işlemin kullanıcı yetkisi + işlem bağlamı + risk puanına göre onaylanması.
- **2026 trendi:** Statik güvenlikten runtime izlemeye kayış.

## S4: WAF ile API Gateway güvenliği arasındaki farklar neler?
**Cevap:**
| Özellik | WAF | API Gateway |
|---------|-----|-------------|
| Katman | L7 (uygulama katmanı) | L7 + API yönetimi |
| Koruma | SQLi, XSS, OWASP Top 10 | Aynı + rate limiting, auth, şema validation |
| API bilgisi | Yok (genel HTTP kuralları) | Var (API şemasını bilir) |
| İşlev | Sadece güvenlik | Güvenlik + trafik yönetimi + dönüşüm |
| 2026'da | AI destekli WAF'lar çıkıyor | API Gateway + WAF entegrasyonu standart |
- **En iyi uygulama:** API Gateway + WAF birlikte kullanılır.

## S5: GraphQL API güvenliği — REST'ten farklı tehditler neler?
**Cevap:** GraphQL, REST'ten farklı tehditler getirir:
- **Sorgu derinliği saldırısı:** İç içe sorgularla sunucuyu çökertme (ör. friends → friends → friends ...)
- **Veri aşırı yükleme:** Tek sorguda tüm veritabanını çekme
- **Introspection disclosure:** API şemasını keşfetme
- **Batch sorgu:** Tek istekte milyonlarca sorgu
- **Korumalar:**
  - Sorgu derinliği limiti (max depth: 5-7)
  - Sorgu karmaşıklığı analizi (cost analysis)
  - Rate limiting (sorgu bazında)
  - Introspection'ı production'da kapatma
  - Persisted queries (izinli sorgu listesi)
