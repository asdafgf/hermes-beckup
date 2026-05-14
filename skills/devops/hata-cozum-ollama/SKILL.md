---
name: hata-cozum-ollama
description: Hata çözüm döngüsü — 2 kez kendi dene, çözülmezse Ollama'ya sor, çözüm yoksa Python kodu ürettirip çalıştır.
---

# Hata Çözüm Döngüsü (Ollama Destekli)

Bu skill, terminal/sistem hatalarını çözmek için 4 aşamalı otomatik döngüyü tanımlar.

## Kural

Kullanıcı önceden onay vermiştir. **Sormadan uygula.**

## Akış

### Aşama 1 — Kendi çözümünü dene (2 deneme)
- Hatayı anla, normal araçlarınla (terminal, search_files, web_search) çözmeyi dene
- 2 farklı yaklaşım dene
- İkisi de başarısız olursa → **Aşama 2'ye geç**

### Aşama 2 — Ollama'ya sor
- `gemma3:4b` modelini kullan (hızlı, GPU'ya sığar)
- NOT: `gemma4:31b` (31B) 8GB VRAM'e sığmaz, çok yavaş. Kullanma.
- Şu formatla sor:
```
echo "[HATA MESAJI ve BAĞLAM]" | ollama run gemma4:31b
```
- Çıktıyı al, uygula
- Çalışırsa → bitir
- Çalışmazsa → **Aşama 3'e geç**

### Aşama 3 — Ollama'dan Python kodu iste
- Hatayı ve çıktıyı olduğu gibi Ollama'ya yapıştır, şu promptla:
```
echo "Su sorunu cozmek icin python kodu uret: [HATA]

Kod dogrudan calistirilabilir olmali, tek bir .py dosyasi." | ollama run gemma3:4b
```
- Gelen Python kodunu bir .py dosyasına yaz
- `python /c/Users/eymen/.../cozum.py` ile çalıştır
- Çalışırsa → bitir
- Çalışmazsa → kullanıcıya durumu raporla, hatayı göster

## Ollama Model Durumu Kontrol

```bash
ollama ps            # aktif model(ler) ve VRAM kullanimi
nvidia-smi           # GPU VRAM durumu
ollama list          # hangi modeller var?
```

## Uzun Prompt'lar ve JSON Dosya Tekniği

Bash'ta inline JSON ile Türkçe/unicode prompt'lar kaçış hatası verir:
```bash
# BAD — syntax error:
#   curl -d '{"prompt":"Uzun Türkçe prompt..."}'
#
# GOOD — JSON'u dosyaya yaz, -d @file ile gönder:
echo '{"model":"qwen2.5-coder:7b","prompt":"Sorunu detayli anlatan uzun Turkce metin...","stream":false,"options":{"num_gpu":0}}' > /tmp/cozum_prompt.json
curl -s --max-time 180 -X POST http://localhost:11434/api/generate -d @/tmp/cozum_prompt.json
rm -f /tmp/cozum_prompt.json

# Yanıtı ayıklamak için:
curl -s --max-time 180 -X POST http://localhost:11434/api/generate -d @/tmp/cozum_prompt.json | python3 -c "import sys,json; print(json.load(sys.stdin)['response'])"
```

## Önemli Notlar
- Ollama aktif değilse önce `ollama serve`'i background'da başlat
- **Model seçimi:** GPU'ya sığan model kullan. `gemma3:4b` (4.3GB) en hızlı seçenek. `gemma4:31b` (18.5GB) çok yavaş — sadece kritik durumlarda kullan.
- Ollama'nın ps çıktısını kontrol et (`ollama ps`)
- Python çalıştırırken `ollama ps`'den modelin hâlâ aktif olduğunu kontrol et
- Uzun süren işlemlerde model context timeout olabilir, tekrar `ollama run` gerekebilir
- Bash'ta uzun prompt'lar için her zaman `-d @/tmp/file.json` kullan
