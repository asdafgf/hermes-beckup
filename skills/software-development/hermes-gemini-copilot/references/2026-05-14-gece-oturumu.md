# 14 Mayıs 2026 — Gece Oturumu Özeti

## Yapılanlar

### İnternetten Konu Bulma (8 konu)
1. Bettercap WiFi Keşfi (wifi)
2. scrcpy Android Ekran (android)
3. ADB TCP/IP Güvenlik (android)
4. WiFi Deauth WPA3 (wifi)
5. Android Konum Takibi (android)
6. BadUSB Flipper Zero (saldiri)
7. Zero-Day 2025-2026 Trend (ileri)
8. LockBit Ransomware 4.0 (saldiri)

### Android Saldırıları Serisi (4 konu, öncelikli)
9. Android Zero-Day Qualcomm Zafiyetleri (android)
10. Android Bankacılık Truva Atları (android)
11. Android NFC Relay SuperCard X (android)
12. Android AccessibilityService Keylogging (android)

## Teknik Öğrenimler

| Konu | Çözüm |
|------|-------|
| ollama run PTY'siz çalışmıyor | curl ile REST API (http://localhost:11434/api/generate) |
| Ollama "Stopping..." deadlock | taskkill //F //IM ollama.exe + ollama serve |
| Python JSON false vs False | stream:False string literali Python'da hata verir |
| grep -c boş integer | KOD_KONTROL=${KOD_KONTROL:-0} ile koru |
| sleep 240 çok uzun | Max 15sn, kullanıcı "ne bekliyorsun" derse çok yavaşsın |
| Hata olunca 3 deneme bekleme | Direkt Gemini'ye yönlen, ilk hatada |

## Skill Kayıtları

Her konu: ~/.hermes/skills/security/<skill-adi>/SKILL.md + references/qwen_yanit.txt
Toplam: ~18 skill bu oturumda (önceki 9 + 9 yeni)
