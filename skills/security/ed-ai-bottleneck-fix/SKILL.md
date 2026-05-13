---
name: ed-ai-bottleneck-fix
description: "AI asistan darboğaz çözümü: asenkron çalıştırma, timeout yapılandırması, bağlam sınırlandırması. Kullanıcı Eymen'in talebi üzerine, tüm işlemlerde uygulanması zorunlu kurallar."
---
# ED AI Bottleneck Fix — Darboğaz Çözümü

## Zorunlu Kurallar (Her İşlem Öncesi Uygulanır)

### Kural 1 — Asenkron Çalıştırma Direktifi
Sunucu başlatan, log dinleyen veya kendi kendine kapanmayan bir terminal komutu çalıştıracaksan:
- **KESİNLİKLE** arka planda çalıştır (`background=true`)
- Asla interaktif girdi bekleyen komut yazma
- Sunucu başlattıysan hemen ardından readiness check yap (`curl`, `nc`, `grep log`)
- `sleep` ile bekleme yapma — health check veya log sinyali kullan

### Kural 2 — Süre Aşımı (Timeout) Yapılandırması
- Foreground komutlarda timeout 30sn'yi aşarsa **zaten** terminal öldürülür
- Background komutlarda `notify_on_complete=true` kullan
- process(action='wait') ile bloklarken timeout ver
- Ajan asla 30sn+ foreground komutta takılı kalmamalı

### Kural 3 — Bağlam Sınırlandırması (Context Truncation)
- Uzun terminal çıktıları model context'ini şişirir
- Uzun log varsa: **baş + son** al, ortasını kırp
  - Baş: ilk 30 satır
  - Son: son 20 satır
  - Ortası: `... [X satır atlandı] ...`
- `terminal()` çıktısı > 50 satırsa truncation uygula
- Model context şişmesini engellemek için gereksiz logları session'a taşıma

## Uygulama Kontrol Listesi

- [ ] Sunucu başlatıyorum → background=true
- [ ] Komut >5sn sürecek → timeout değerlendir
- [ ] Çıktı >50 satır → truncation uygula
- [ ] Interaktif komut → background + pty veya başka yöntem

## Neden Bu Kural Var?
Eymen'in sisteminde AI ajanı terminalde takılıp kalıyordu:
1. Sunucu foreground'da başlatılıp asılı kalıyor
2. Uzun loglar model context'ini doldurup zehirliyor
3. Timeout olmayan komutlar ajanı bloke ediyor

Bu skill her işlem **öncesi** kontrol edilmelidir.
