---
name: mevcut-ollama-modelleri-entegrasyonu
description: "Mevcut Ollama modellerinin Hermes'e entegrasyonu. Hiçbir indirme gerekmez — zaten var olan 15 modelin hangi amaçla kullanılacağı: qwen2.5-coder (kod), deepseek-coder (alternatif kod), llava (vision/görsel), gemma4 (genel/sohbet), gemma4:31b (en güçlü), hermes3 (hafif)."
version: 1.0
author: hermes
category: mlops
tags: [ollama, models, llava, vision, deepseek, gemma, integration]
---

# Mevcut Ollama Modelleri Entegrasyonu

## 🎯 Ne Zaman Kullanılır
- Yeni bir model indirmeden önce mevcut modelleri kontrol et
- Hangi modelin hangi görev için uygun olduğunu sorgularken
- Vision analizi, kodlama veya sohbet için doğru modeli seçerken

---

## 🗺️ MODEL HARİTASI

### Kodlama / Debug
```bash
# Birincil: qwen2.5-coder:7b (4.7 GB) — şu an aktif kullanılan
curl -s --max-time 180 -X POST http://localhost:11434/api/generate \
  -d '{"model":"qwen2.5-coder:7b","prompt":"...","stream":false}'

# Alternatif: deepseek-coder:6.7b (4.1 GB) — daha hafif, farklı perspektif
curl -s --max-time 180 -X POST http://localhost:11434/api/generate \
  -d '{"model":"deepseek-coder:6.7b-instruct-q4_K_M","prompt":"...","stream":false}'
```

### Vision / Görsel Analiz
```bash
# LLaVA 7B (4.7 GB) — Storyboard, diyagram, ekran görüntüsü analizi
curl -s --max-time 180 -X POST http://localhost:11434/api/generate \
  -d '{"model":"llava:7b","prompt":"Bu görselde ne var?","images":["base64_encoded_image"],"stream":false}'
```

### Genel Sohbet / Analiz
```bash
# En güçlü: gemma4:31b (19 GB)
curl -s --max-time 300 -X POST http://localhost:11434/api/generate \
  -d '{"model":"gemma4:31b","prompt":"...","stream":false}'

# Dengeli: gemma4:latest (9.6 GB) — Türkçe destek
curl -s --max-time 180 -X POST http://localhost:11434/api/generate \
  -d '{"model":"gemma4:latest","prompt":"...","stream":false}'

# Hızlı: gemma3:4b (3.3 GB) — basit sorgular için
curl -s --max-time 60 -X POST http://localhost:11434/api/generate \
  -d '{"model":"gemma3:4b","prompt":"...","stream":false}'

# Hafif: hermes3:latest (4.7 GB)
curl -s --max-time 120 -X POST http://localhost:11434/api/generate \
  -d '{"model":"hermes3:latest","prompt":"...","stream":false}'

# Mistral (4.4 GB)
curl -s --max-time 120 -X POST http://localhost:11434/api/generate \
  -d '{"model":"mistral:latest","prompt":"...","stream":false}'
```

### Çok Hızlı / Basit
```bash
# qwen2.5-coder:1.5b-base (986 MB) — basit kod tamamlama
curl -s --max-time 30 -X POST http://localhost:11434/api/generate \
  -d '{"model":"qwen2.5-coder:1.5b-base","prompt":"def hello():","stream":false}'
```

---

## ⚖️ KARŞILAŞTIRMA TABLOSU

| Model | Boyut | Parametre | Hız | Kullanım |
|-------|-------|-----------|-----|----------|
| gemma3:4b | 3.3 GB | 4B | ⚡Çok hızlı | Basit sohbet |
| qwen2.5-coder:1.5b | 986 MB | 1.5B | ⚡En hızlı | Basit kod |
| deepseek-coder:6.7b | 4.1 GB | 6.7B | 🟡Orta | Alternatif kod |
| qwen2.5-coder:7b | 4.7 GB | 7B | 🟡Orta | Ana kod modeli |
| llava:7b | 4.7 GB | 7B | 🟡Orta | Vision/görsel |
| hermes3 | 4.7 GB | ? | 🟡Orta | Sohbet |
| mistral | 4.4 GB | 7B | 🟡Orta | Sohbet |
| gemma4:latest | 9.6 GB | 4B | 🟢İyi | Genel amaç |
| gemma4-cpu | 9.6 GB | 4B | 🟢İyi (CPU) | CPU'da çalışma |
| gemma4:31b | 19 GB | 31B | 🐢Yavaş | En derin analiz |

---

## 💡 ENTEGRASYON STRATEJİSİ

### Storyboard Vision Analizi (watch-youtube pipeline'ında)
Şu an DeepSeek vision desteklemediği için storyboard'lar analiz edilemiyor. **LLaVA:7b** ile çözüm:

```python
import base64, json, urllib.request

def analyze_image_with_llava(image_path, question):
    with open(image_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    
    payload = json.dumps({
        'model': 'llava:7b',
        'prompt': question,
        'images': [b64],
        'stream': False
    })
    
    req = urllib.request.Request(
        'http://localhost:11434/api/generate',
        data=payload.encode(),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read())['response']
```

### Skill Üretimi (YouTube Transcript → Hermes Skill)
Ollama modelleri, YouTube transcript'lerini Hermes Agent SKILL.md formatına çevirmek için API'lere alternatif olarak kullanılır:
```python
def ask_ollama_for_skill(text, model="qwen2.5-coder:7b"):
    prompt = f"""Create a Hermes Agent SKILL.md from this transcript.
name: short kebab-case, description: one sentence, body: step-by-step, category: security
SKILL.md only:
{text[:10000]}"""
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False,
                          "options": {"num_predict": 2000, "temperature": 0.3}})
    r = requests.post("http://localhost:11434/api/generate", data=payload,
                      headers={"Content-Type":"application/json"}, timeout=180)
    return r.json().get("response","")
```

**Sıralama:** Gemini API → OpenRouter → qwen2.5-coder → gemma4 → fallback (transcript özeti)

Ollama'nın avantajı: hiç kota derdi yoktur, sınırsız ve ücretsizdir.

### İkinci Görüş (Second Opinion)
Kod incelemesinde iki farklı modelin görüşünü al:
1. **qwen2.5-coder:7b** (birincil)
2. **deepseek-coder:6.7b** (ikincil — farklı perspektif)

### Model Seçim Kılavuzu
| Görev | Önerilen Model |
|-------|---------------|
| Kod yazma/debug | qwen2.5-coder:7b |
| Kod ikinci görüş | deepseek-coder:6.7b |
| Görsel analiz | llava:7b |
| Uzun analiz/rapor | gemma4:latest |
| En derin analiz | gemma4:31b |
| Hızlı basit soru | gemma3:4b veya hermes3 |
| Basit kod tamamlama | qwen2.5-coder:1.5b |

---

## 📚 İlgili Skill'ler
- ollama-sohbet — Ollama modelleriyle sohbet
- python-oto-debug-dongusu — Kod debug
- watch-youtube — Storyboard + vision analizi
