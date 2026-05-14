---
name: paralel-skill-uretici
description: "YouTube transcript'lerinden paralel (3 thread) olarak Hermes Agent skill'i üretir. Aynı anda 3 video işler, sırayla dener: OpenRouter GPT-4o-mini (öncelikli) → Gemini API → Ollama qwen2.5-coder → Fallback. Önbellek ile tekrar sorgulamayı önler. Cronjob ile her 15 dk'da otomatik çalışır. Asla kullanıcıya sormaz."
version: 2.0
author: hermes
category: devops
tags: [paralel, otomasyon, skill-uretimi, transcript, ollama, gemini, openrouter, pipeline, otomatik]
source: "Hermes Agent oturumu 14 Mayıs 2026 - v8 fixes"
---

# 🚀 Paralel Skill Üretici v8 (GÜNCELLENMİŞ)

## 🎯 Ne Zaman Kullanılır

- YouTube kanallarından transcript çekildiğinde bunları skill'e dönüştürmek için
- Çok sayıda video (>100) hızlıca işlenmesi gerektiğinde
- API kotası sorunu yaşandığında (Ollama yedek)
- Kullanıcıya sormadan otomatik skill üretimi istendiğinde

---

## ⚙️ Nasıl Çalışır

```
┌─────────────────────────────────────────────────────┐
│                   PARALEL SKILL ÜRETİCİ              │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ThreadPoolExecutor (3 worker)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Worker 1 │  │ Worker 2 │  │ Worker 3 │          │
│  │ Video A  │  │ Video B  │  │ Video C  │          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│       │              │              │                │
│       ▼              ▼              ▼                │
│  ┌──────────────────────────────────────┐           │
  │  Sıralı Model Denemeleri              │           │
  │  1. OpenRouter GPT-4o-mini (en hızlı)  │           │
  │  2. Gemini API (varsa)                  │           │
  │  3. Ollama qwen2.5-coder (semaphore 1!) │           │
  │  4. Fallback (transcript özeti)         │           │
  └──────────────────────────────────────┘           │
│                                                     │
│  ┌──────────────────────────────────────┐           │
│  │  Önbellek (skill_cache.json)         │           │
│  │  Aynı video tekrar sorgulanmaz       │           │
│  └──────────────────────────────────────┘           │
│                                                     │
│  ▼ Security kategorisine SKILL.md olarak kaydedilir │
└─────────────────────────────────────────────────────┘
```

## 🚀 Hemen Başlatma

```bash
# 1. En son script (v8 - önerilen)
python3 ~/AppData/Local/hermes/scripts/paralel_uretici_v8.py

# 2. Veya cronjob ile otomatik
# (cronjob: "otomatik-skill-uretici", her 15 dk)
#
# 3. Cronjob script'ini güncellemek için:
cp ~/AppData/Local/hermes/scripts/paralel_uretici_v8.py ~/AppData/Local/hermes/scripts/paralel_uretici.py
```

## 📂 Dosya Yapısı

```
~/AppData/Local/hermes/scripts/
├── paralel_uretici_v6.py        ← Eski (timeout sorunlu)
├── paralel_uretici_v7.py        ← v7 (dict snapshot fix)
└── paralel_uretici_v8.py        ← ✅ Mevcut (önerilen, semaphore + health check)

~/.hermes/skills/devops/paralel-skill-uretici/
├── SKILL.md                     ← Bu skill
└── references/
    └── v8-fixes-2026-05-14.md   ← V8 hata çözüm kaydı

~/Desktop/transcript_skills/
├── paralel_uretici_v6.py        ← Eski script
├── paralel_log.txt              ← İşlem log'u
├── skill_cache.json             ← Önbellek (tekrar sorgulama yok)
└── kaydedilen/                  ← Yedek skill'ler
```

## 🔧 Teknik Detaylar

### API'ler
```python
# API key'ler PowerShell User değişkenlerinden alınır:
# GOOGLE_API_KEY = Gemini için
# OPENROUTER_API_KEY = OpenRouter için
# Ollama = localhost:11434 (hiç key gerekmez)
```

### Qwen'den Python kodu üretme (14 Mayıs 2026 eklentisi)

Qwen2.5-Coder'dan Python çözüm kodu üretmek için özel yaklaşım gerekir:

**Sorun:**
- Qwen 7B uzun prompt'larda timeout (180sn+) yiyor
- Bash inline JSON'da parantez sorunu çıkıyor
- `delegate_task` provider hatası (API key yoksa) çalışmıyor

**Çözüm — 3 paralel curl:**
```bash
# 1. Dizini oluştur
mkdir -p /c/Users/eymen/Desktop/qwen_solutions

# 2. 3 paralel curl başlat (her biri farklı PID)
curl -s -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5-coder:7b","prompt":"Skill: SKILL_ADI. ACIKLAMA. Sadece kodu yaz, kod ```python ile baslasin.","stream":false,"options":{"num_predict":800,"temperature":0.3}}' \
  > /c/Users/eymen/Desktop/qwen_solutions/response_1.json 2>&1 &
```

**Daha iyi yaklaşım — Python script'i yaz ve çalıştır:**
```python
# write_file ile Desktop'a kaydet, sonra background terminal ile çalıştır
# Python script ThreadPoolExecutor + Semaphore(1) kullanır
# response'dan ```python ... ``` bloğunu çıkarıp .py dosyasına kaydeder
```

### Paralel İşlem
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_WORKERS = 3  # Aynı anda 3 video

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {executor.submit(process_one_video, v): v for v in batch}
    for future in as_completed(futures):
        r = future.result()
```

### Önbellek
```python
# skill_cache.json
# Anahtar: "kanal:video_id"
# Değer: SKILL.md içeriği
cache = {}
CACHE_FILE = "skill_cache.json"
```

### Cronjob
```bash
# Her 15 dk'da bir çalışır, 96 kez (24 saat)
schedule: "*/15 * * * *"
repeat: 96
```

## ⚡ Hız Karşılaştırması

| Versiyon | Yöntem | Hız | Not |
|----------|--------|-----|-----|
| v4 (tek sıra) | 1 video, sıralı modeller | ~2 video/dk | |
| **v6 (paralel)** | 3 video, paralel modeller | ~6-9 video/dk | Ollama concurrent timeout sorunu var |
| **v7 (fix)** | cache dict snapshot, 120 batch | ~5-6 video/dk | hala Ollama timeout |
| **v8 (current)** | OpenRouter öncelikli, semaphore + health check | ~5 video/dk | en kararlı |
| + Önbellek | Aynı video tekrar işlenmez | Ekstra hız | |

### Gerçek Dünya Performansı (v8, 14 Mayıs 2026)
| Kaynak | Adet | Süre | Başarı |
|--------|------|------|--------|
| OpenRouter GPT-4o-mini | 78 video | ~5 dk (ilk batch'ler) | ✅ En hızlı |
| Fallback (her API başarısız) | 63 video | ~20 dk | ⚠️ Ollama timeout sonrası |
| **Toplam** | **144 video** | **27 dk** | **5.3 video/dk** |

### Önemli: API Öncelik Sırası (v8)
```
OpenRouter GPT-4o-mini → (en hızlı, en kaliteli, ~10-15 sn/video)
  ├── başarılı → kaydet
  └── başarısız → Gemini deneme
                     ├── başarılı → kaydet
                     └── başarısız → Ollama qwen2.5-coder:7b
                                        ├── başarılı → kaydet (semaphore ile!)
                                        └── başarısız → Fallback (transcript özeti)
```

## 🛠️ Sorun Giderme

### Ollama concurrent timeout (⚠️ YAYGIN)
```bash
# qwen2.5-coder:7b tek GPU'da sadece 1 concurrent request kaldırır.
# 3 worker aynı anda istek atarsa hepsi timeout yer → fallback'e düşer
# 
# Çözüm: Semaphore(1) ile 1 thread sınırı + health check
#   with ollama_sem:
#       health = requests.get("http://localhost:11434/api/tags", timeout=5)
#       # sadece sağlıklıysa generate isteği gönder
#
# Kodda bunu kontrol et:
#   ollama_sem = Semaphore(1)  # <-- ThreadPoolExecutor dışında tanımlanmalı
```

### dict changed size during iteration (⚠️ CONCURRENT)
```python
# ThreadPoolExecutor içinde save_cache() hata verir çünkü
# cache dict'i başka thread tarafından değiştirilirken iterasyona girer.
#
# Çözüm: dict(cache) ile snapshot al:
#   json.dump(dict(cache), f, ensure_ascii=False, indent=2)
```

### Ollama bağlantı hatası
```bash
# Ollama deadlock
taskkill //F //IM ollama.exe
ollama serve &
sleep 5
# Tekrar dene
```

### Gemini API yanıt vermiyor (API key geçerli ama istek formatı)
```bash
# varsayılan prompt "gpt-4o-mini" tarzı olabilir, Gemini farklı endpoint kullanır
# curl ile test:
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GOOGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Create a SKILL.md from this transcript."}]}]}'
```

### 'hermes-agent' isimli çok sayıda skill
```python
# OpenRouter boş/generic isim döndüğünde olur
# Çözüm: extract_name() 'hermes-agent'ı reddetmeli:
#   if n2 and len(n2) >= 3 and n2 != 'hermes-agent':
#       return n2
```

### Önbellek temizleme (gerekirse)
```bash
rm ~/Desktop/transcript_skills/skill_cache.json
```

### Log kontrol
```bash
tail -50 ~/Desktop/transcript_skills/paralel_log.txt
```

## 🔗 İlgili Skill'ler ve Referanslar
- `references/v8-fixes-2026-05-14.md` — V8 hata çözümleri ve performans notları
- `references/qwen-to-python-codegen.md` — Qwen2.5-Coder'dan Python çözüm kodu üretme kılavuzu (paralel curl + ThreadPoolExecutor yaklaşımları)
- john-hammond-siber-guvenlik-arsivi — Video arşiv yönetimi
- mevcut-ollama-modelleri-entegrasyonu — Ollama model kullanımı
- ollama-sohbet — Ollama API ve deadlock kurtarma
- hermes-gemini-copilot — API key yönetimi
- youtube-kanal-arsiv-sistemi — YouTube kanal arşivleme
