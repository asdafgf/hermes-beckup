# Ollama REST API Kullanım Kılavuzu (14 May 2026)
# Bu session'da test edilmiş ve onaylanmıştır.

## `ollama run` YERİNE `curl REST API`

| Yöntem | Çalışır mı? | PTY Gerekir mi? | Background Uyumlu mu? |
|---------|------------|----------------|----------------------|
| `ollama run` | ❌ Sadece PTY'de | Evet | Hayır |
| `curl -X POST .../api/generate` | ✅ Her zaman | Hayır | Evet |

## API Endpoint

`POST http://localhost:11434/api/generate`

### Request
```json
{"model": "qwen2.5-coder:7b", "prompt": "Soru metni", "stream": false}
```

### Response
```json
{"model":"qwen2.5-coder:7b","response":"Yanıt metni","done":true}
```

### Streaming (stream: true)
Her satır ayrı JSON: `{"response":"token"}`. Son satır `{"done":true}`.
Arka arkaya toplamak için Python loop gerekir.

## Bilinen Sorunlar ve Çözümleri

### 1. "Stopping..." deadlock
Model GPU'dan boşaltılırken takılı kalır.
Çözüm: `taskkill //F //IM ollama.exe` + `ollama serve`
Sadece `ollama stop <model>` yeterli olmaz (bazen sonsuz döngü).

### 2. PTY'siz ollama run
`ollama run` komutu PTY olmadan sadece Braille animasyon karakterleri döndürür.
Çözüm: Asla kullanma. Her zaman curl ile API'ye git.

### 3. JSON'daki False/false hatası
Python `json.dumps({'stream':False})` — büyük F ile.
`{'stream':false}` yazarsan NameError alırsın.

### 4. Uzun prompt'larda timeout
120sn genelde yeterli, ama 31B modellerde 300sn+ gerekebilir.

### 5. Retry deseni
Qwen bazen sessizce hata döndürür. 2 kez retry yap:
```bash
for attempt in 1 2; do
  response=$(curl -s --max-time 120 ...)
  [ -n "$response" ] && break
  sleep 3
done
```
