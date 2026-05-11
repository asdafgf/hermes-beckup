# Gemini OCR Tutarsızlık Dokümantasyonu

## Vaka: "Sistemlere Göre Uymazlık Dağılımı" Tablosu

**Tarih:** 2026-05-11
**Dosya:** `img_ce23f3a5e742.jpg`
**Model:** gemini-2.5-flash

### 3 farklı analiz, 3 farklı sonuç

Aynı görsel, aynı model, 3 farklı prompt ile sorgulandı:

#### Analiz 1 (genel prompt: "tüm yazıları oku")
| Sistem | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|
| PERVANE | 0 | 6 | 17 | 16 | 6 |
| MOTOR | 4 | 20 | 5 | 14 | 11 |
| UÇAK LASTİĞİ | 9 | 0 | 0 | 11 | 1 |
| ... | | | | | |
| TOPLAM | 104 | 106 | 95 | 109 | 64 |
| Hesaplanan | 95 | 90 | 93 | 104 | 60 |

#### Analiz 2 (detaylı prompt: "her satırı eksiksiz oku")
| Sistem | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|
| PERVANE | 0 | 6 | 5 | 16 | 6 | ← farklı!
| MOTOR | 4 | 20 | 17 | 14 | 11 | ← farklı!
| UÇAK LASTİĞİ | 2 | 0 | 0 | 5 | 1 | ← farklı!
| ... | | | | | |
| TOPLAM | 104 | 106 | 95 | 109 | 64 |

#### Analiz 3 (spesifik format: "SİSTEM: değer1,değer2,...")
| Sistem | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|
| PERVANE | 0 | 6 | 5 | 6 | 6 | ← yine farklı!
| MOTOR | 4 | 20 | 17 | 14 | 11 |
| UÇAK LASTİĞİ | 2 | 0 | 0 | 5 | 2 | ← farklı!
| TOPLAM | 104 | 106 | 95 | 109 | 64 |

### Gözlemler
1. **TOP satırları (ilk 5-6 sistem)** genelde tutarlı okunuyor
2. **Alt satırlar** (sistem sayısı arttıkça) karışıyor — Gemini satır/sütun eşlemesini kaybediyor
3. **Sistem isimleri** farklı analizlerde farklı satırlara düşebiliyor (BORDA ↔ ELEKTRONİK)
4. **TOPLAM satırı** her seferinde doğru okundu — ama iç değerler yanlışsa toplam da anlamsız
5. **Hesaplanan toplam ≠ bildirilen toplam** — bu OCR hatasının ana sinyali

### Dersler
- Gemini tablo okumada **güvenilir değil**, özellikle 15+ satırlı tablolarda
- Prompt formatı ("virgülle ayır", "eksiksiz oku") sonucu çok az değiştiriyor
- TOPLAM doğru okunsa bile iç değerler yanlış olabilir
- **İlk şüphe her zaman OCR'a** — tablo hatasına değil
- Claude.ai web bu tür tablolarda çok daha başarılı

### Çözüm Önerisi
Karmaşık tablolarda (>10 satır, >3 sütun):
1. Gemini'yi dene
2. Python ile hesaplamaları doğrula
3. Tutarsızlık varsa → Claude.ai web'e yönlendir
4. Gelecekte: `google.genai` (yeni SDK) ile tekrar test et
