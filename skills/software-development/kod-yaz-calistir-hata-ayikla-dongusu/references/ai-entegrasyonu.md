# AI Modellerini Döngüye Ekleme (Claude + Gemini)

Bu döngü sadece benim (Claude) ürettiğim kodlarla sınırlı değil. Gemini de aynı şekilde kullanılabilir.

## Gemini'yi Döngüye Sokma

### 1. API Anahtarı

Google AI Studio'dan al: https://aistudio.google.com/apikey

Anahtarı şuraya kaydet: `~/.gemini_api_key` (hermes tarafından otomatik okunur)

### 2. API'ye Bağlanma (requests ile, google-genai kütüphanesi olmadan)

```python
import requests, json, os

key = open(os.path.expanduser("~/.gemini_api_key")).read().strip()
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

payload = {"contents": [{"parts": [{"text": prompt}]}]}

r = requests.post(f"{url}?key={key}", json=payload, timeout=30)
data = r.json()
text = data["candidates"][0]["content"]["parts"][0]["text"]
```

### 3. Kullanılabilir Modeller (Mayıs 2026 itibarıyla)

- `gemini-2.5-flash` — önerilen (hızlı + kaliteli)
- `gemini-2.5-pro` — daha derin analiz
- `gemini-2.0-flash` — eski ama stabil
- `gemini-3-pro-preview` — en yeni (preview)

Modelleri listele: `https://generativelanguage.googleapis.com/v1beta/models?key={key}`

### 4. 429 (Too Many Requests) Yönetimi

```python
for deneme in range(3):
    r = requests.post(...)
    if r.status_code == 429:
        time.sleep(4)
        continue
    r.raise_for_status()
    break
```

## Claude vs Gemini — Karşılaştırma (Mayıs 2026)

| Kriter | Claude (Hermes) | Gemini (API) |
|---|---|---|
| Kod kalitesi (ilk deneme) | ✅ Yüksek | ⚠️ Orta |
| Hata oranı | Düşük | Orta-Yüksek |
| Düzeltme ihtiyacı | Az | Sık |
| Hız | Anında | 2-5 sn gecikme |
| Kotasız | ✅ Evet | ❌ 60 istek/dakika (ücretsiz) |
| Türkçe çıktı | ✅ Doğal | ⚠️ Bazen garip |
| Windows API bilgisi | ✅ İyi | ⚠️ Ortalama |
| VS Code açma | ✅ `code` komutu | ❌ API üzerinden yok |

## Kullanım Deseni

1. **Ben (Claude)** kodu yazarım — daha az hata, daha temiz
2. **Gemini'yi** alternatif/karşılaştırma için kullan
3. İkisini aynı döngüde kullan: Claude yazsın, Gemini alternatif versiyon üretsin, hangisi daha iyiyse onu al

## Önemli Uyarılar

- Gemini'nin kodunu asla sorgusuz kabul etme — test et
- `ThreadPoolProcessor` gibi hayali sınıflar üretebilir — düzelt
- Windows encoding (cp857, utf-8) konusunda sık hata yapar — elle düzelt
- 429 hatası alınırsa bekle ve dene (max 3)
