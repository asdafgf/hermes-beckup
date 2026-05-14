---
name: siber-guvenlik-agentic-ai
description: Agentic AI ve Otonom Siber Saldırılar — 6 soru-cevap. AI destekli saldırılar, SOC otomasyonu, prompt injection, Shadow AI.
version: 1.0
category: security
tags: [ai, agentic-ai, prompt-injection, shadow-ai, soc-automation]
---

# Agentic AI ve Otonom Siber Saldırılar

## S1: Agentic AI nedir ve siber güvenlikte nasıl kullanılır?
**Cevap:** Agentic AI, insan müdahalesi olmadan otonom kararlar alıp eylem gerçekleştirebilen yapay zeka sistemleridir. Siber güvenlikte iki ucu keskin bir bıçaktır:
- **Saldırı:** AI ajanları otonom keşif yapabilir, zafiyet taraması gerçekleştirebilir, kimlik avı e-postaları yazabilir ve ağda yanal hareket edebilir.
- **Savunma:** SOC'lerde 7/24 izleme, triyaj ve otomatik müdahale için kullanılır. SentinelOne gibi platformlar AI ajanlarıyla tehditleri insan hızından çok daha hızlı tespit eder.
- **2026 trendi:** Gartner'a göre, AI ajanları 2026'da SOC'lerin standart bir parçası haline geldi.

## S2: AI destekli saldırılar geleneksel savunmaları nasıl aşıyor?
**Cevap:** AI saldırıları şu yöntemlerle klasik savunmaları aşar:
1. **Polimorfik kötü amaçlı yazılım:** Her çalıştırmada imzasını değiştirir, imza tabanlı antivirüsler tespit edemez.
2. **Hiper-kişiselleştirilmiş phishing:** AI, hedefin sosyal medyasını tarar, dilini taklit eder, güvenilir kişileri taklit eden mesajlar üretir.
3. **Makine hızında tarama:** AI ajanları binlerce API'yi saniyeler içinde tarayarak zafiyet bulur.
4. **Davranış taklidi:** AI, normal kullanıcı davranışını öğrenip taklit ederek UEBA (Kullanıcı ve Varlık Davranış Analizi) sistemlerini atlatır.
**Çözüm:** AI destekli savunma (AI vs AI). Davranışsal analitik, anomali tespiti ve sıfır güven mimarisi.

## S3: SOC otomasyonu ve AI'ın tehdit avcılığında rolü nedir?
**Cevap:** Security Operations Center (SOC) 2026'da:
- **Triyaj otomasyonu:** AI, gelen uyarıları önceliklendirir, yanlış pozitifleri eler, sadece gerçek tehditleri insana yükseltir.
- **24/7 izleme:** AI ajanları kesintisiz çalışır, gece vardiyası ihtiyacını azaltır.
- **Adli analiz:** AI, saldırı zincirini otomatik olarak yeniden yapılandırır.
- **Otomatik müdahale:** Şüpheli IP'yi karalisteye ekleme, host izolasyonu, tehdit besleme güncellemesi gibi görevleri insansız yapar.
- **Sınır:** Karmaşık çok katmanlı saldırılar ve stratejik kararlar için insan analisti hala gereklidir.

## S4: Prompt injection saldırıları nedir? LLM'leri hedef alan bu saldırılara karşı hangi savunmalar geliştirildi?
**Cevap:** Prompt injection, bir kullanıcının LLM'in sistem talimatlarını atlatan girdiler göndererek modeli istenmeyen davranışa zorlamasıdır.
- **Türleri:** Doğrudan (sistem talimatını geçersiz kılma), dolaylı (üçüncü taraf içeriğine gömülü talimat)
- **Risk:** Finansal sistemlerde AI kullanılıyorsa, injection yetkisiz işlem yapılmasına yol açabilir.
- **2026 trendi:** ECCU'ya göre, prompt injection 2026'nın en önde gelen AI siber güvenlik tehdidi.
- **Savunmalar:** Input sanitization, rol tabanlı çıktı kısıtlama, ayrıştırılmış talimat katmanları, Prompt Security gibi araçlar.

## S5: Otonom AI ajanları keşif yapıp sızabilir mi? Örneklerle açıkla.
**Cevap:** Evet, 2026'da otonom AI ajanları tam saldırı döngüsünü gerçekleştirebiliyor:
- **Keşif:** Hedefin alt alan adlarını, API'lerini, açık portlarını otomatik tarar.
- **Zafiyet analizi:** Bilinen CVE'leri eşleştirir, hangi saldırı vektörünün işe yarayacağını belirler.
- **Sömürü:** Seçilen zafiyeti otomatik olarak sömürür.
- **Yanal hareket:** Sızdıktan sonra ağı keşfeder, diğer sistemlere geçer.
- **Örnek:** ServiceNow BodySnatcher zafiyeti — bir AI ajanı API tanımlama zafiyetini kullanarak tam sistem işgaline yol açabilir.
**Savunma:** Runtime davranışsal izleme ve işlemsel yetkilendirme.

## S6: Shadow AI nedir? Hangi veri sızıntılarına yol açar?
**Cevap:** Shadow AI, çalışanların IT departmanının bilgisi veya izni olmadan kullandığı yapay zeka araçlarıdır.
- **Riskler:**
  - Çalışanlar hassas şirket verilerini halka açık AI araçlarına yükler
  - Müşteri verileri, kaynak kodu, finansal bilgiler sızdırılabilir
  - AI modeli bu verileri eğitim setinde kullanabilir
- **2026'da:** IT departmanları AI kullanımını haritalamak için ağ düzeyinde engelleme + onaylı sandbox versiyonlar sunuyor.
- **Önlem:** AI keşif ajanları, veri sınırı zorlama, Prompt Security gibi araçlar.
