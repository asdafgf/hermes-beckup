# Altın Ons Sohbeti — 13 Mayıs 2026

## Kullanıcı Talebi
"hermes ollama içinde olan yapay zeka ile sohbet etsin, karşılıklı sorular sorsunlar, konu altın ons değeri. Altının dünyadaki atışı (artışı) konusu karşılıklı tartışılsın. Hermes internet verileri alarak altın konusunda sorular sorsun, ben cevapları izleyeceğim terminalden."

## Kullanılan Model
`gemma4:latest` (9.6 GB, 4B parametre) — Türkçe cevap veriyor.

## Toplanan Veriler

### Güncel Fiyatlar (13 Mayıs 2026)
- **Ons altın:** $4,699.22 (günlük -%0.34, aylık -%2.95, yıllık +%47.50)
- **Gram altın:** 6,851 - 6,881 TL
- **Çeyrek altın:** 11,114 - 11,248 TL
- **Tüm zamanlar rekoru:** $5,602 (Ocak 2026)
- **Gümüş ons:** $89.01 (günlük +%2.85, aylık +%12, yıllık +%176.31)

### Makro Faktörler
- ABD enflasyonu: %3.8 (Nisan 2026, Mayıs 2023'ten beri en yüksek)
- ABD faizi: %3.75 (Fed faiz indirimi beklentisi azaldı)
- İran savaşı devam ediyor — enerji maliyetleri yükseliyor
- Trump-Çin zirvesi bekleniyor (ticaret ateşkesi + İran)
- Hindistan altın vergisi: %6 → %15 (talebi baskılıyor)
- Üretici fiyatları (PPI) Nisan'da beklenenden fazla arttı

### Merkez Bankası Altın Rezervleri
- ABD: 8,133 ton
- Almanya: 3,350 ton
- İtalya: 2,452 ton
- Fransa: 2,437 ton
- Çin: 2,313 ton (Mart 2026)
- Rusya: 2,305 ton
- Hindistan: 881 ton

## Sohbet Akışı

### Tur 1: "Altın ons fiyatı nedir? Sence alınır mı?"
- **Script:** `/tmp/gold_chat.sh`
- **Metod:** PTY (terminal'de canlı izleme, pty=true, timeout=120s)
- **Sonuç:** Model 3 senaryolu detaylı analiz verdi (ayı/boğa/konsolidasyon). PTY'de yarıda kaldı → normal modda tekrar denendi, tam cevap alındı.

### Tur 2: "Düşüşün sebebi faiz mi jeopolitik mi? Gümüş neden %176 yükseldi?"
- **Script:** `/tmp/gold_q2.sh` (başarısız — timeout/boş çıktı)
- **Script v2:** `/tmp/gold_q2_v2.sh` (kısa cevap isteği eklendi, normal mod, timeout=180s)
- **Sonuç:** Başarılı. Model faiz beklentilerini ana sebep olarak verdi, gümüşün endüstriyel taleple yükseldiğini açıkladı.

## Kritik Gözlemler

1. **PTY vs Normal Mod:** PTY canlı izleme için idealdir ama uzun cevapları keser. Normal mod tam cevap verir.
2. **Model Hafızası Yok:** Her `ollama run` yeni bir oturumdur. Önceki cevaba atıf yapmak için prompt'a özet eklenmeli.
3. **Kısa Cevap Zorlaması:** Model uzun yazmaya meyilli. "Kisa cevap ver lutfen" eklemek timeout sorununu çözer.
4. **Script Dosyası Şart:** Doğrudan terminal komutuyla Türkçe metin göndermek bash tırnak sorunlarına yol açar. Her tur için ayrı .sh dosyası şart.

## Kullanılan Modeller

- **Tur 1:** `gemma4:latest` (9.6 GB, 4B) — başarılı
- **Tur 2:** `gemma4:latest` — PTY'de kesildi, normal modda tamamlandı
- **Qwen yükleme:** `qwen2.5-coder:7b-instruct-q4_K_M` (4.7 GB) çekildi, sohbet için hazır

## Script Şablonları

### PTY Modu (canlı izleme)
```bash
#!/bin/bash
MESSAGE="<soru metni>"
echo "$MESSAGE" | ollama run gemma4:latest 2>/dev/null
```
Çalıştır: terminal(komut, pty=true, timeout=180)

**PTY Uyarısı:** PTY uzun cevapları kesebilir. Eğer kullanıcı "canlı izledim" derse bile, cevabın tam gelip gelmediğini doğrula. Yarıda kaldıysa normal modda tekrar dene.

### Normal Mod (tam cevap)
```bash
#!/bin/bash
echo "<kısa soru>" | ollama run gemma4:latest 2>/dev/null
```
Çalıştır: terminal(komut, timeout=180)

### Normal Mod + Kısa Cevap Zoru (timeout riski varsa)
```bash
#!/bin/bash
echo "Kisa ve ozlu cevap ver lutfen. <soru>" | ollama run gemma4:latest 2>/dev/null
```
Çalıştır: terminal(komut, timeout=120)

## Altın Konuşması — Tam Metin

### Tur 1 Sorusu
Model'e gönderilen prompt (13 Mayıs 2026 verileriyle):
- Ons altın: ~$4,699 (günlük -%0.34, aylık -%3.02, yıllık +%47.39)
- Rekor: $5,602 (Ocak 2026)
- Gram altın: 6,852 TL
- ABD enflasyonu: %3.8, faiz indirimi beklentisi azaldı
- İran savaşı, Trump-Çin zirvesi
- Hindistan altın vergisi %6 → %15

### Tur 2 Sorusu
"Altın rekor 5602'den 4700'e düştü (%16). En büyük sebep ne: faiz mi, jeopolitik mi? Merkez bankaları alımı sürüyor mu? Gümüş neden %176 yükseldi?" → Başarılı. Model faiz beklentilerini ana sebep olarak verdi.
