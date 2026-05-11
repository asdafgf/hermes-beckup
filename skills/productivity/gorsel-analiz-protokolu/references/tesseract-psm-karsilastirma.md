# Tesseract PSM Karşılaştırma Testi

## Vaka: "Sistemlere Göre Uymazlık Dağılımı" (23 sistemli tablo)

**Tarih:** 2026-05-11  
**Görsel:** `img_ce23f3a5e742.jpg` (960×1280 px)  
**Tesseract:** v5.5.0 (Scoop), lang=`tur+eng`

## Sonuçlar

| PSM Modu | Açıklama | Sistem Bulma | Not |
|---|---|---|---|
| **PSM=3** (default) | Otomatik sayfa segmentasyonu | **17 sistem tespit, 14 parse edildi** | ✅ En iyi |
| PSM=4 | Tek sütunlu metin | ~8 sistem, sayılar karışık | ⚠️ Daha kötü |
| PSM=6 | Tekdüzen metin bloğu | 0 sistem, anlamsız karakterler | ❌ Kullanma |

## Ön İşleme Testi

Denenen tüm ön işleme yöntemleri sonucu KÖTÜLEŞTİRDİ:

| Ön İşleme | Bulunan Sistem | Not |
|---|---|---|
| Ham görsel (işlemesiz) | 14/23 | ✅ En iyi |
| 2x büyütme + kontrast + keskinlik | 0/23 | Tablo yapısı bozuldu |
| CLAHE kontrast + threshold | 9/23 | Binary dönüşüm veri kaybı |
| Gaussian blur + threshold | 6/23 | Detaylar silindi |
| 3x büyütme + GPU tensor | 0/23 (timeout) | Çok büyük, işlem süresi aştı |

## Sonuç

**Tesseract en iyi sonucu HAM görselde, PSM=3 ile veriyor.**  
Görsel ön işleme tablo yapısını bozuyor.  
GPU bu iş akışında kullanılmamalı — sadece CPU + PIL yeterli.
