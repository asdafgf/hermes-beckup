# OpenRouter API Key Kurulum ve Test Notları

## PowerShell User Değişkenine Kaydetme (Kalıcı)
```powershell
[System.Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY','sk-or-v1-...','User')
```

Bu yöntemle key, makine yeniden başlatılsa bile kalıcı olur. Bash/Python'dan okumak için:
```python
import subprocess
r = subprocess.run(["powershell.exe", "-Command",
    "[System.Environment]::GetEnvironmentVariable('OPENROUTER_API_KEY','User')"],
    capture_output=True, text=True, timeout=5)
key = r.stdout.strip()
```

## OpenRouter'da Çalışan/Çalışmayan Modeller (14 Mayıs 2026)

| Model | Durum | HTTP |
|-------|-------|------|
| `anthropic/claude-3.5-sonnet` | ❌ Çalışmıyor | 404 |
| `anthropic/claude-sonnet` | ❌ Çalışmıyor | 400 |
| `google/gemini-2.0-flash-001` | ✅ Çalışıyor | 200 |
| `google/gemini-2.0-flash` | ❌ Çalışmıyor | 400 |
| `openai/gpt-4o-mini` | ✅ Çalışıyor | 200 |
| `openai/gpt-4o` | ✅ Çalışıyor | 200 |

**Not:** Claude modelleri Türkiye'den OpenRouter'da çalışmıyor olabilir (bölgesel kısıtlama). GPT-4o-mini en güvenilir seçenek.

## Test Komutu
```bash
curl -s -X POST "https://openrouter.ai/api/v1/chat/completions" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-4o-mini", "messages": [{"role": "user", "content": "hello"}], "max_tokens": 10}'
```

## Pipeline v5'te Kullanım
Pipeline sırayla dener: Gemini API → OpenRouter (GPT-4o-mini) → Ollama qwen2.5-coder → Ollama gemma4 → fallback
