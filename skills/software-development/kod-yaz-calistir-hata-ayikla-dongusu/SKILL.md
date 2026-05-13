---
name: kod-yaz-calistir-hata-ayikla-dongusu
description: "Write Python code → run in terminal → catch errors → fix → repeat until passing. Fully automatic — never ask the user to run it themselves."
version: 2.0.0
author: Eymen
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [vscode, python, debugging, automation, loop]
    related_skills: [systematic-debugging, request-code-review, gorsel-analiz-protokolu]
---

# Kod Yaz → Çalıştır → Hata Ayıkla → Döngüsü

## Ne Zaman Kullanılır

- Kullanıcı "şu işi yapan bir kod yaz" dediğinde
- Herhangi bir Python script yazma + çalıştırma talebinde
- Hata ayıklama döngüsü gerektiren görevlerde
- Altyapı/bağımlılık kurulumu gerektiğinde (pip, scoop, binary)

## Temel Kural

**Kullanıcıya SORMA** — her adımı otomatik yap:
1. Kodu yaz ve Desktop'a kaydet
2. Hemen terminalde çalıştır (`/c/Users/eymen/anaconda3/python.exe` ile, asla `python` kısaltmasını kullanma — Hermes venv'i gösterir, Anaconda gerekir)
3. Hata varsa hemen düzelt (`patch` ile)
4. Doğru sonuç alana kadar tekrarla (maks 3-4 deneme, her denemede farklı yaklaşım)
5. Sonucu göster

## Python Çalıştırma

**KRİTİK:** `python` komutu Hermes venv'ini gösterir. Kod çalıştırırken **tam yol kullan**:
```bash
/c/Users/eymen/anaconda3/python.exe /c/Users/eymen/Desktop/dosya_adi.py
```

**google namespace çakışması:** Hermes venv'inde (`hermes-agent\\venv\\Lib\\site-packages\\google`) boş bir `google` namespace paketi var. Anaconda'nın `google.genai` modülünü import etmeye çalışırken PATH sıralaması nedeniyle önce Hermes venv'indeki `google` bulunur ve `from google import genai` hata verir (`cannot import name 'genai' from 'google'`). Çözüm: her zaman doğrudan Anaconda Python yolunu kullan, asla `python` kısaltmasıyla çalıştırma.

**Interaktif script'ler (input alan):** `input()` fonksiyonu kullanan script'ler PTY'de sonsuz EOF döngüsüne girer. Bunun yerine:
1. Script'i yaz
2. Bir `.bat` dosyası oluştur (Anaconda Python yolunu göstersin)
3. `cmd.exe /c start /B /MIN "Başlık" "C:\path\to\script.bat"` ile ayrı CMD penceresinde aç
4. Kullanıcıya "Yeni CMD penceresi açıldı" bilgisini ver

## Altyapı Kurulum Döngüsü

Python paket/binary kurulumu gerektiğinde:
1. Eksik paket tespiti → `pip list` + try/except import
2. Kurulum → `pip install` veya `scoop install` (büyük dosyalar background'da)
3. Doğrulama → `import X; print(X.__version__)`
4. Hata varsa → Gemini/Claude'a sor, alternatif çözüm dene
5. Çalışana kadar tekrarla

## Çoklu AI Sağlayıcı Stratejisi

| Öncelik | Sağlayıcı | Ne Zaman |
|---|---|---|
| 🥇 **Hermes** (DeepSeek/mevcut model) | Birincil | Her zaman ilk tercih |
| 🥈 **Gemini API** (yedek) | Ücretsiz, model 429 hatası alırsa devreye girer | Kod yazdırma, hata sorma |
| 🥉 **Claude.ai web** (son çare) | Chrome gerekli, manuel | Karmaşık görsel analiz |

Döngü prensibi: Kod yaz → çalıştır → hata → düzelt → çözüm. Sağlayıcı değişir, yöntem değişmez.

## Hata Durumunda

- Hatayı tam metin olarak oku (kısaltma yapma)
- `systematic-debugging` skill'ini uygula (4 aşamalı)
- Çözüm için Gemini API'ye sor (tüm traceback'i gönder)
- Çözülünce prensibi skill olarak kaydet

## Test Stratejisi (Kullanıcı Tercihi)

**Kullanıcı Eymen'in prensibi: "Bölüm bölüm test et, sıkıntı yoksa bir sonraki aşamaya geç, var ise çözene kadar uğraş."**

```python
# 1. Derleme/kontrol et
npx tsc --noEmit 2>&1 | head -20
# Veya:
npx expo export --platform web --output-dir /tmp/test-export 2>&1 | tail -20

# 2. Hata varsa düzelt -> tekrar dene
# 3. Derleme başarılı -> çalıştır
# 4. Çalışma başarılı -> bir sonraki modüle geç

# Hiçbir adımda kullanıcıya sorma. Otomatik yap.
```

Bu prensip özellikle React Native/Expo projelerinde geçerlidir (KiraLog gibi). Derleme hatası → düzelt → tekrar dene döngüsünü kullanıcıya sormadan yap.

## Tesseract Görsel Analizi

Tesseract v5.5.0 kurulu (Scoop ile). Türkçe+İngilizce dil dosyalı. PSM=3 (default) en iyi sonucu verir. Görsel ön işleme (kontrast, threshold) tablo okumasını BOZAR — ham görsel kullan.

```python
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\eymen\scoop\apps\tesseract\current\tesseract.exe"
img = Image.open('gorsel.jpg')
metin = pytesseract.image_to_string(img, lang='tur+eng')
```

## GPU Durumu

RTX 4070 (8.6GB), CUDA 12.5 driver var. PyTorch 2.6.0+cu124 GPU ile çalışıyor. PaddleOCR için PaddlePaddle GPU pip'te bulunamadı — conda gerekli. EasyOCR GPU çalışmıyor (CUDA toolkit eksik).
