# Gemini CLI Process Communication

## Ne Zaman Kullanılır

Bir terminal'de açık olan CLI AI agent'ına (Gemini CLI, Claude Code CLI vb.) programatik olarak mesaj göndermen gerektiğinde. Örneğin: "Terminalinde açık olan Gemini'ye bir soru gönder, cevabını al ve işleme koy."

## Yöntem

### 1. Önce Hangi CLI'nin Çalıştığını Tespit Et

```python
import subprocess

# tasklist ile process ara (Windows)
result = subprocess.run(
    ["tasklist", "/FI", "IMAGENAME eq python*", "/FO", "CSV", "/NH"],
    capture_output=True, text=True
)
print(result.stdout)

# Veya tüm process'leri tara
result = subprocess.run(
    ["tasklist", "/FO", "CSV", "/NH"],
    capture_output=True, text=True
)
for line in result.stdout.splitlines():
    if any(x in line.lower() for x in ["gemini", "claude", "ai", "agent"]):
        print(line)
```

### 2. Gemini CLI Kurulumu

```bash
npm install -g @google/gemini-cli

# API key ile çalıştır (önceden export et):
export GEMINI_API_KEY="AIzaSy..."
gemini
```

### 3. Gemini CLI'yi Batch/Non-interactive Modda Çağır

Gemini CLI'ye tek seferlik prompt göndermek için interaktif mod yerine **pipe** kullan:

```bash
echo "How to fix ninja build error on Windows?" | gemini --input-mode=pipe
```

### 4. Gemini API'yi Doğrudan Çağır (Her Zaman Çalışır)

CLI aracına bağlanmak mümkün değilse (process stdin'e yazamıyorsan), doğrudan API'yi curl/requests ile çağır:

```python
import requests

GEMINI_KEY = "AIzaSy..."
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"

payload = {
    "contents": [{
        "parts": [{"text": "Soru metni buraya"}]
    }]
}

resp = requests.post(url, json=payload)
print(resp.json()["candidates"][0]["content"]["parts"][0]["text"])
```

### 5. OpenRouter ile Alternatif

```python
import requests

OPENROUTER_KEY = "sk-or-v1-..."
url = "https://openrouter.ai/api/v1/chat/completions"

payload = {
    "model": "google/gemini-2.0-flash-001",
    "messages": [{"role": "user", "content": "Soru metni"}]
}

headers = {
    "Authorization": f"Bearer {OPENROUTER_KEY}",
    "Content-Type": "application/json"
}

resp = requests.post(url, json=payload, headers=headers)
print(resp.json()["choices"][0]["message"]["content"])
```

## Pitfall'lar

- **Rate limit (429):** Gemini free tier'da dakikada 60 istek/günde 1500 istek sınırı var. Kotan dolduysa 1 dakika bekle.
- **WSL vs Windows process:** WSL içinde çalışan Gemini'ye Windows tarafından stdin gönderemezsin. Aynı ortamda olmalı.
- **CLI interaktif mod:** `gemini` (parametresiz) interaktif TUI açar. stdin pipe işe yaramaz. `--input-mode=pipe` veya single prompt flag'i kullan.
- **process("submit")** Hermes'e ait bir fonksiyon değil — sadece Hermes'in background process'leri için geçerli. Senin açtığın terminal'deki process'e müdahale edemez.
