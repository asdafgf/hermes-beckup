# Qwen2.5-coder REST API Fix (14 May 2026)

## Sorun
`ollama run qwen2.5-coder:7b` komutu MSYS/git-bash ortamında PTY (pseudo-terminal) olmadan çalışmıyor. Çıktı olarak sadece Braille loading animasyonu (⠋⠹⠸⠼) dönüyor. `timeout` komutu da PTY'siz işe yaramıyor.

Ayrıca `ollama` süreci "Stopping..." state'inde takılıp kalıyor ve yeni istekleri kabul etmiyor.

## Çözüm: REST API Kullan

`ollama run` yerine doğrudan REST API'ye POST yap:

```bash
curl -s --max-time 120 -X POST http://localhost:11434/api/generate \
  -d '{"model":"qwen2.5-coder:7b","prompt":"Soru buraya","stream":false}'
```

JSON'dan `response` alanını çıkarmak için:
```bash
curl -s --max-time 120 -X POST http://localhost:11434/api/generate \
  -d '{"model":"qwen2.5-coder:7b","prompt":"Soru","stream":false}' | \
  python -c "import sys,json; print(json.load(sys.stdin).get('response',''))"
```

### Python ile
```python
import requests, json
resp = requests.post("http://localhost:11434/api/generate",
    json={"model": "qwen2.5-coder:7b", "prompt": "soru", "stream": False},
    timeout=120)
print(resp.json().get("response", ""))
```

## Avantajları
1. PTY gerekmez — background'da çalışır
2. Native timeout (`--max-time 120`) — `timeout` komutuna gerek yok
3. `stream: false` ile tek seferde tam yanıt alınır
4. Çıktı direkt JSON, parse edilebilir

## Ollama Deadlock Çözümü

Model "Stopping..." state'inde takılırsa:

```bash
# Tüm ollama süreçlerini öldür
taskkill //F //IM ollama.exe

# Yeniden başlat
ollama serve
```

Not: `ollama stop qwen2.5-coder:7b` tek başına yeterli değil. Tüm ollama süreçlerini öldürmek gerekiyor.
