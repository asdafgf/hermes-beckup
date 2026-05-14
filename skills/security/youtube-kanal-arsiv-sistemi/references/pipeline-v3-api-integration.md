# Claude + Gemini Dual-API Skill Generation Pipeline (v5)

## Overview
After transcripts are extracted, try **Gemini first**, then **OpenRouter (GPT-4o-mini)**, then **Ollama (qwen2.5-coder:7b)**, then **fallback**.
**Her API tek deneme yapar** — başarısız olursa hemen sıradakine geçer.

## API Key Discovery Order
```python
def get_api_key(var_name):
    """1. Environment variable → 2. PowerShell User env var"""
    val = os.environ.get(var_name, "")
    if val:
        return val
    try:
        result = subprocess.run(
            ["powershell.exe", "-Command", 
             f"[System.Environment]::GetEnvironmentVariable('{var_name}','User')"],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip()
    except:
        return ""
```

## Priority (v5, AKTİF)
1. **Gemini** (`GOOGLE_API_KEY`) — tek deneme, 429'da hemen geç
2. **OpenRouter GPT-4o-mini** (`OPENROUTER_API_KEY`) — çoğu işi bu görür
3. **Ollama qwen2.5-coder:7b** (yerel, sınırsız)
4. **Ollama gemma4:latest** (alternatif)
5. **Fallback** — transcript excerpt as skill

## Gemini API Call (tek deneme, retry yok)
```python
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"
# ⚠️ DİKKAT: f-string'de {GOOGLE_API_KEY} kullan, *** placeholder koyma!
try:
    r = requests.post(url, json=..., timeout=30)
    if r.status_code == 200: return parse(r)
    if r.status_code == 429: log("⏳ Gemini kota dolu")  # hemen geç, bekleme
except: pass
return None
```

## OpenRouter (GPT-4o-mini)
```python
url = "https://openrouter.ai/api/v1/chat/completions"
headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
model = "openai/gpt-4o-mini"  # ucuz, hızlı, güvenilir
payload = {"model": model, "messages": [...], "max_tokens": 2000}
```

## OpenRouter Claude Modelleri (Güncel)
```bash
# Doğru model ID'sini bul:
curl -s "https://openrouter.ai/api/v1/models" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  | python -c "import sys,json; d=json.load(sys.stdin); [print(m['id']) for m in d.get('data',[]) if 'sonnet' in m['id'].lower()]"
```
**Mayıs 2026 itibarıyla geçerli:**
- `anthropic/claude-sonnet-4.6` ✅
- `anthropic/claude-sonnet-4.5` ✅
- `anthropic/claude-sonnet-4` ✅
- `anthropic/claude-sonnet-4-20250514` ❌ GEÇERSİZ (400 Bad Request)

## Best Selection Logic
```python
if gemini_result and openrouter_result:
    content = gemini_result if len(gemini_result) > len(openrouter_result) else openrouter_result
elif gemini_result: ...
elif openrouter_result: ...
elif ollama_result: ...
else: content = fallback_skill(...)
```

## ⚠️ PERFORMANS KRİTİK: Retry Yok!
**ESKİ (çöker):** 3 retry with 10s+20s+30s backoff = 60s kayıp. Script 120s timeout'unda çöker.
**YENİ (çalışır):** Tek deneme, başarısızsa hemen sonraki API'ye geç. Video başına ~4-8sn.

## Script Sürüm Kirliliği
- Dosya adı `otomatik_skill_uretici_v4.py` ama içerik **v5** olabilir (Ollama eklendi)
- İlk 5 satırda başlığı kontrol et
- `def ask_ollama` varsa → v5
- Gemini URL'inde `***` varsa → fix gerek

## Prompt Template for OpenRouter/Ollama
```
Create a Hermes Agent SKILL.md from this cybersecurity video.
Video: https://youtu.be/{video_id} Channel: {kanal}
Requirements: name=kebab-case, description=summary, body=guide, category=security
SKILL.md only:
{text[:10000]}
```

## Cron Job Schedule
- Runs every **5 minutes** via `hermes cronjob`
- Script: `~/.hermes/scripts/otomatik_skill_uretici_v4.py`
- Processes ALL unprocessed .srt files across all known channel directories
- Tracks processed videos via `processed_ids_v4.txt`
- Bu session'da ~40 video/90sn hızında çalıştı (OpenRouter GPT-4o-mini ile)

## User Preference (Eymen)
- "Bana sorma" — execute autonomously, never ask
- Hızlı başarısız ol, bekleme
- Gemini varsa dene ama 429'da hemen geç
- OK with fallback when APIs totally unavailable
- Values clean, meaningful skill names (not `all-righty`, `hey-everyone`)
