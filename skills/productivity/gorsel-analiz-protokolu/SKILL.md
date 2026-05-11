---
name: gorsel-analiz-protokolu
description: Tesseract OCR + Gemini API ile görsel analiz, tablo/matematik doğrulama, Claude.ai web yedekleme ve EasyOCR/LLaVA/PaddleOCR alternatifleri protokolü.
---

# Görsel Analiz Protokolü

Eymen'in bir resim paylaştığı her durumda otomatik olarak uygulanır.

## Güvenilirlik Sıralaması (en güvenilirden en az güvenilire)

| Sıra | Yöntem | Güvenilirlik | Kredi | Not |
|---|---|---|---|---|
| 🥇 | **Claude.ai web** (manuel) | ✅ Çok yüksek | Ücretsiz (free) | Chrome gerekli — zaten kurulu |
| 🥇 | **Tesseract OCR + Python** (otomatik, yerel) | ✅ Yüksek (temiz tablolarda) | Yok | v5.5.0 kurulu, Türkçe+İngilizce dil dosyalı |
| 🥈 | **Gemini API** (otomatik) | ⚠️ Orta — tutarsız | Ücretsiz kota | Tablo okumada hata yapabiliyor |
| 🥉 | **EasyOCR CPU** (otomatik) | ⚠️ Yavaş, anlamsız çıktı | Yok | CUDA sorunu var, CPU modu çok yavaş |
| 🔬 | **LLaVA / Ollama** | ❌ Deneysel | Yok | v0.23.2'de image okuma çalışmıyor |
| 🔬 | **PaddleOCR** (GPU planlı) | ⚠️ Kuruldu, test edilmedi | Yok | CUDA Toolkit gerekli (şu an yok) |

**Öncelik sırası (otomatik):**
1. Tesseract ile oku (yerel, ücretsiz, hızlı) → çıktıyı pandas ile doğrula
2. Tesseract başarısız olursa → Gemini API (yedek)
3. İkisi de tutarsızsa → Claude.ai web (manuel, en güvenilir)

**Kural:** İlk resim paylaşımında Gemini API ile analiz yap. Tutarsızlık varsa veya kullanıcı "yanlış okudu" derse, Claude.ai web'e yönlendir.

## Adımlar

### 1. Tesseract OCR ile Yerel Görsel Analiz (öncelikli, otomatik)

```python
import pytesseract
from PIL import Image

# Tesseract binary yolu (Scoop ile kuruldu)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\eymen\scoop\apps\tesseract\current\tesseract.exe"

# Görseli oku (Türkçe + İngilizce)
img = Image.open('resim_yolu.jpg')
metin = pytesseract.image_to_string(img, lang='tur+eng')

# Çıktıyı parse et, pandas DataFrame'e çevir
# (parse işlemi için referans: Desktop\goruntu_analiz.py)
```

**Kurulu:** Tesseract v5.5.0 (Scoop ile), `tur.traineddata` ve `eng.traineddata` mevcut.
**Performans:** CPU'da çalışır, ~5-10sn. Gemini'den daha tutarlı sonuç verir.
**Sınırlama:** Tablo yapısını otomatik parse edemeyebilir (OCR hataları) — manuel düzeltme gerekebilir.
**PSM modu:** PSM 3 (default) en iyi sonucu verir. PSM 4 ve 6 daha kötü okur. `--psm 6` anlamsız karakterler üretir.

**Parse stratejisi (goruntu_analiz_v3.py'deki yaklaşım):**
- Bilinen sistem adları listesini (`BILINEN_SISTEMLER`) kullanarak OCR çıktısını eşleştir
- Her satırda sistem adını bul, hemen ardından gelen sayıları oku
- `regex` ile sayıları ayıkla, 0-200 aralığındakileri değer olarak kabul et
- TOPLAM satırındaki sayıları bildirilen toplam olarak al

### 2. Gemini API ile Görsel Analiz (yedek, otomatik)

```bash
cd ~ && /c/Users/eymen/anaconda3/python.exe -c "
import google.generativeai as genai
import PIL.Image
genai.configure(api_key=open('.gemini_api_key').read().strip())
model = genai.GenerativeModel('gemini-2.5-flash')
img = PIL.Image.open('resim_yolu.png')
response = model.generate_content(['Bu görselde ne var? Tüm yazıları, sayıları, tablo varsa tüm hücreleri eksiksiz oku.', img])
print(response.text)
"
```

**Prompt ipuçları (tablo doğruluğu için kritik):**
- Spesifik prompt yaz: hangi sütunlar, hangi format
- Örnek: `"Bu tabloda SİSTEM, 2022, 2023, 2024, 2025, 2026 sütunları var. HER hücreyi virgülle ayırarak oku."`
- Model referansı: `google.generativeai` paketi deprecated, `google.genai`'ye geçiş yapılmalı (FutureWarning)

### 2. Tablo ve Matematik Doğrulama

Gemini çıktısında tablo tespit edilirse:
- OCR değerlerini Python listesine aktar
- Şu işlemleri **otomatik hesapla ve karşılaştır**:
  - Toplama (sütun/satır toplamları)
  - Çıkarma (fark/bakiye)
  - Yüzde hesapları (%)
  - Oran hesapları (A/B)
  - PVT özet tabloları
- Her işlemi adım adım yeniden hesapla
- **Tutarsızlık varsa:** önce OCR hatası mı yoksa tablo hatası mı ayırt et
- Yanlışsa: TESPİT ET → UYAR → DÜZELTİLMİŞ HALİNİ SUN

**⚠️ Tuzak:** Gemini tablo okumada 3 seferde 3 farklı sonuç verebilir. Eğer hesaplanan toplamlar bildirilen toplamlarla uyuşmuyorsa, ilk şüphelenilecek şey OCR hatasıdır, tablo hatası değil. Kullanıcıya "OCR tutarsız olabilir, Claude.ai'den teyit edelim mi?" diye sor.

### 3. Claude.ai Web (manuel, en güvenilir)

Eymen Chrome'da `chat.claude.ai`'ye giriş yapmış durumda. Görsel analiz için Claude.ai web önerildiğinde:
- Görsel dosya yolunu söyle (cache'den)
- Kullanıcı manuel olarak yükler
- Claude.ai free tier'da çalışır

### 4. EasyOCR (alternatif — CPU, yavaş)
```python
import easyocr
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'  # OpenMP çakışmasını önler
reader = easyocr.Reader(['tr','en'], gpu=False)  # GPU çalışmıyor
sonuc = reader.readtext('resim_yolu.png', detail=1, paragraph=True)
```

Sorun: CUDA bulamıyor (GPU=False), CPU modunda model indirme çok yavaş (timeout).

### 5. Ollama + LLaVA (deneysel — şimdilik çalışmıyor)

Ollama v0.23.2'de `--image` flag'i yok. Stdin'den resim besleme de çalışmıyor (anlamsız çıktı üretiyor). LLaVA 7B modeli (4.7 GB) indirildi ama kullanılamıyor. Bekle: Ollama güncellenince yeniden dene.

## Önemli Dersler (Öğrenilmiş)
- **Tesseract PSM sıralaması (kritik):** PSM=3 (varsayılan) en iyi sonucu verdi (17/23 sistem tespit etti, parse sonrası 14/23). PSM=4 ile sayılar karıştı. PSM=6 anlamsız karakterler üretti (0/23). **Hiçbir zaman `--psm 6` kullanma.**
- **Görsel ön işleme tabloyu BOZAR:** Kontrast artırma + 2x büyütme + Gaussian blur sonrası Tesseract 14/23'ten 0/23'e düştü. Ham görsel en iyisidir. GPU'yu bu iş için kullanma.
- Gemini OCR aynı görsel için 3 farklı okuma yaptı, hiçbiri toplamlarla uyuşmadı. Tesseract daha tutarlı.
- EasyOCR CPU modu tablo görsellerinde anlamsız karakterler döndürdü (OpenMP çakışması + CUDA yok). Tesseract kullan.
- Claude Code CLI (v2.1.123) login olmadığı için çalışmadı. Chrome + Claude.ai web kullan.
- OCR tutarsızlığı (9 puan fark) bildirilen toplamın tamamını kapsamayan eksik okumalardan kaynaklanır — tablo hatası değil OCR hatasıdır.
- **En güvenilir yöntem:** Claude.ai web'e görseli yüklemek.
- **Otomatik yöntem:** Tesseract (ham, işlemesiz, PSM=3) + pandas ile oku + doğrula.

## Referanslar
- `scripts/tesseract_tablo_oku.py` — Tek script: Tesseract oku + akilli parse + pandas dogrula.
- `scripts/goruntu_analiz_v3.py` — Guncel versiyon: PSM otomatik secimi + akilli parse + dogrulama.
- `references/tesseract-psm-karsilastirma.md` — PSM modlarının karşılaştırmalı test sonuçları (PSM=3 kazanır)
- `references/github-repo-paketleme.md` — GitHub reposu yapisi ve push talimati (hermes-skill-turkce)
- Desktop'ta hazir: `goruntu_analiz_v4.py`, `tablo_dogrula_manuel.py`, `alternatif_cozum.py`

## İlgili Skill'ler
- `systematic-debugging` — 4 asamali hata ayiklama (AI yardim dahil)
- `kod-yaz-calistir-hata-ayikla-dongusu` — kod yaz/calistir/hata ayikla dongusu

## Bağımlılıklar
- Python: Pillow, google-generativeai (Anaconda'da)
- Tesseract: v5.5.0 (Scoop ile), tur+eng dil dosyalı
- Chrome: Claude.ai web için gerekli
- İsteğe bağlı: easyocr, ollama (llava modeli)
