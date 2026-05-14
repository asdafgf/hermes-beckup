# Qwen2.5-Coder → Python Çözüm Kodu Üretme

## Problem

288 skill'in her biri için Qwen2.5-Coder'dan çalıştırılabilir Python kodu üretmek.
Her skill bir SKILL.md dosyası, her Python çözümü tek bir .py dosyası olacak.

## Engeller

1. **delegate_task çalışmıyor** — Provider hatası (Google API key yok). Terminal-based bypass gerekli.
2. **Qwen timeout** — 180sn+ sürebilen generate çağrıları
3. **Bash parantez sorunu** — MSYS/git-bash `(` karakterini subshell olarak yorumlar
4. **Tek GPU'da concurrent sınırı** — Qwen 7B tek seferde 1 request kaldırır

## Çözüm: 3 Paralel Background Curl

### Adım 1: Dizini oluştur
```bash
mkdir -p /c/Users/eymen/Desktop/qwen_solutions
```

### Adım 2: 3 ayrı terminal ile aynı anda curl
```bash
# Terminal 1
curl -s -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5-coder:7b","prompt":"Skill: ai-review-insight-extractor. CSVden urun yorumlarini oku, pros/cons cikar. Sadece kodu yaz, kod ```python ile baslasin.","stream":false,"options":{"num_predict":800,"temperature":0.3}}' \
  > /c/Users/eymen/Desktop/qwen_solutions/response_1.json 2>&1

# Terminal 2
curl -s -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5-coder:7b","prompt":"Skill: anthony-sottile-markdown-git-tricks. Markdown satir sonu duzeltme. Sadece kodu yaz.","stream":false,"options":{"num_predict":800,"temperature":0.3}}' \
  > /c/Users/eymen/Desktop/qwen_solutions/response_2.json 2>&1
```

### Adım 3: response JSON'dan .py çıkar
```bash
python3 -c "
import json
with open('response_1.json') as f:
    r = json.load(f)
code = r['response']
# ```python ... ``` bloğunu çıkar
import re
m = re.search(r'```python\n(.*?)```', code, re.DOTALL)
if m:
    code = m.group(1)
with open('ai-review-insight-extractor.py', 'w') as f:
    f.write(code)
"
```

## Alternatif: Python Script Yaklaşımı

Daha sağlam: `write_file` ile bir Python script'i yaz, background terminal ile çalıştır.

```python
# qwen_skill_runner.py — her skill için sırayla Qwen'e sorar
import json, urllib.request, os, time

OLLAMA_URL = "http://localhost:11434/api/generate"
OUTPUT_DIR = os.path.expanduser("~/Desktop/qwen_solutions")

def query_qwen(prompt, max_tokens=800):
    payload = {
        "model": "qwen2.5-coder:7b",
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": max_tokens, "temperature": 0.3}
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode()).get("response", "")
```

## Prompt Tasarımı

Qwen'den Python kodu almak için prompt'lar şöyle olmalı:

```
Skill: SKILL_ADI. ACIKLAMA. Tek bir Python scripti yaz. 
Hic API gerekmesin. pip install ile kurulabilir kutuphaneler kullan.
Konsoldan calistirilabilir olsun. Ornek girdi/cikti gostersin.
Sadece kodu yaz, kod ```python ile baslasin.
```

**Kritik:** Son satır (`Sadece kodu yaz, kod ```python ile baslasin`) çıktıyı temiz tutar.

## Zaman Tahmini

| Yöntem | Hız | 288 skill süre |
|--------|-----|----------------|
| 3 paralel curl (mevcut) | ~3 dk/3 skill | ~5 saat |
| Python script (tek sıra) | ~2 dk/skill | ~10 saat |
| Python script + ThreadPool | ~4 dk/3 skill | ~6.5 saat |
