---
name: ed-ai-bottleneck-fix
description: "AI asistan darboğaz çözümü: asenkron çalıştırma, timeout yapılandırması, bağlam sınırlandırması. Kullanıcı Eymen'in talebi üzerine, tüm işlemlerde uygulanması zorunlu kurallar."
metadata:
  priority: mandatory
  applies_to: all-operations
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

### Kural 4 — Qwen REST API Kullan (14 Mayıs 2026)
- `ollama run` ASLA kullanma — PTY gerektirir
- `curl -s --max-time 120 -X POST http://localhost:11434/api/generate` kullan
- Ollama "Stopping..." deadlock: `taskkill //F //IM ollama.exe` + `ollama serve`

## Uygulama Kontrol Listesi

- [ ] Sunucu başlatıyorum → background=true
- [ ] Komut >5sn sürecek → timeout değerlendir
- [ ] Çıktı >50 satır → truncation uygula
- [ ] Interaktif komut → background + pty veya başka yöntem
- [ ] Ollama sorgusu → `ollama run` değil, REST API kullan

## Neden Bu Kural Var?
Eymen'in sisteminde AI ajanı terminalde takılıp kalıyordu:
1. Sunucu foreground'da başlatılıp asılı kalıyor
2. Uzun loglar model context'ini doldurup zehirliyor
3. Timeout olmayan komutlar ajanı bloke ediyor
4. `ollama run` PTY'siz çalışmıyor (Windows) → REST API çözümü

Bu skill her işlem **öncesi** kontrol edilmelidir.
