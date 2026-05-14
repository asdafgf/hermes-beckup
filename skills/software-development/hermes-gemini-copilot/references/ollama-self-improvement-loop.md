# Ollama Kendi Kendini Geliştirme Döngüsü

## Ne İşe Yarar

Ollama'daki yerel modellerden bilgi çekerek Hermes'in skill kütüphanesini büyütmek. Ollama her turda yeni bir konu öğretir, Hermes öğrenilen konuyu skill olarak kaydeder.

## Algoritma

```
Ollama → "KONU: [X]" + "DERS: [3-5 cümle]" formatında ders verir
  ↓
Hermes: parse et, clean_name yap, SKILL.md olarak kaydet
  ↓
Hermes: "Teşekkürler, peki pratikte nasıl uygularım?" diye sorar
  ↓
Ollama: cevaplar, "SIRADAKI DERS: [Y]" ile yeni konu belirtir
  ↓
Döngü: kullanıcı durdurana kadar devam eder
```

## Çalışan Python Kod

```python
# full_script.py
"""
Tam çalışan siber güvenlik eğitim döngüsü.
Konu: references/ollama-siber-guvenlik-loop.md dosyasında ayrıntılı.
"""
import os, urllib.request, json, re, time
from datetime import datetime

SKILLS_DIR = os.path.expanduser("~/.hermes/skills")
OLLAMA_MODEL = "gemma3:4b"  # GPU'ya sığan model!

def talk(prompt):
    data = json.dumps({
        "model": OLLAMA_MODEL, "prompt": prompt, "stream": False,
        "options": {"num_ctx": 4096, "temperature": 0.7}
    }).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate",
        data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.loads(resp.read())["response"]

def cname(text):
    text = re.sub(r'[*_#`\'\"\[\]\(\)\?\!\.]', '', text).lower().replace(' ', '-')
    for o,n in {'ı':'i','ğ':'g','ü':'u','ş':'s','ö':'o','ç':'c'}.items():
        text = text.replace(o, n)
    return re.sub(r'-+', '-', text).strip('-')[:55]

def save_skill(topic, content, turn):
    name = f"ollama-guvenlik-{cname(topic)}"
    path = os.path.join(SKILLS_DIR, f"{name}.md")
    code_blocks = re.findall(r'```python\n(.*?)```', content, re.DOTALL)
    code_section = "\n\n## Kod\n\n```python\n" + "\n\n".join(code_blocks) + "\n```\n" if code_blocks else ""
    md = f"""---
name: {name}
description: "Siber guvenlik - Tur {turn}: {topic}"
category: guvenlik
created_by: agent
turn: {turn}
created_at: {datetime.now().isoformat()}
---
# {topic}
{content}{code_section}
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    return path

# 100+ konulu havuz
TOPICS = ["Port Tarama (Nmap, Python socket)", ...]

turn = 1; idx = 0; existing = set()
while True:
    topic = TOPICS[idx % len(TOPICS)]; idx += 1
    resp = talk(f"...ogret: {topic}...")
    path = save_skill(topic, resp, turn)
    print(f"✓ Tur {turn}: {topic}")
    time.sleep(2); turn += 1
```

## Formatlama — Ollama'nın cevap yapısı

Ollama'nın şu formatta cevap vermesi beklenir:

```
KONU: [konu başlığı]
DERS: [ders içeriği - 3-5 cümle]
KATEGORİ: [programlama|sistem|veri-bilimi|guvenlik|ai|donanim|ag|genel]
```

Takip sorusu sonrası:
```
... (cevap metni)
SIRADAKI DERS: [yeni konu]
```

## Bilinen Tuzaklar

### 1. Star karakteri hatası
Ollama bold için `**KONU**` formatı kullanırsa, bu `*` karakteri Windows'ta geçersiz dosya adıdır.
`OSError: [Errno 22] Invalid argument: '...\\ollama-**kriptosifreleme-temelleri**.md'`

**Çözüm:** `clean_name()` fonksiyonu ile tüm `*_#` karakterlerini temizle.

### 2. Ollama tekrar eden konular
Aynı model benzer konuları tekrar tekrar önerebilir. Prompt'ta "Her derste FARKLI bir konu, kesinlikle tekrar etme" vurgusu yapılmalı.

### 3. Timeout
`gemma4:latest` (31B) gibi büyük modeller 60sn'de yetişmeyebilir. `--max-time 120` veya `urllib` timeout=120 kullanılmalı. Daha hızlı döngü için `gemma3:4b` (~1.5sn/cevap) önerilir.

### 4. Arka plan çalıştırma
Uzun döngüler `terminal(background=true, notify_on_complete=true)` ile çalıştırılmalı. Kullanıcı akışı izlerken Hermes de diğer işlere devam edebilir.

### 5. Skill patlaması
Her tur yeni bir skill dosyası oluşturur. 50+ turda skills/ dizini kalabalıklaşır. `ollama-*` önekiyle toplu silme/temizlik yapılabilir:
```bash
rm ~/.hermes/skills/ollama-*.md
```

### 6. Model seçiminde GPU/VRAM kontrolü (KRİTİK)
**RTX 4070 Laptop = 8GB VRAM.** Her model bu GPU'ya sığmaz. Seçim yaparken VRAM kontrolü zorunludur:

| Model | Boyut | GPU'ya sığar? | Hız |
|-------|-------|--------------|-----|
| `gemma3:4b` | 4.3GB | ✅ Evet (tam GPU) | ~5sn/tur |
| `mistral:latest` | 4.0GB | ✅ Evet (tam GPU) | ~5sn/tur |
| `gemma4:latest` (8B) | 9.6GB | ❌ 8GB VRAM'e sığmaz | CPU'da ~2-3dk/tur |
| `gemma4:31b` | 18.5GB | ❌ Hiç sığmaz | CPU'da çok yavaş |

**Kural:** Model seçerken önce `ollama ps` ve `nvidia-smi` ile VRAM durumunu kontrol et. Eğer model GPU'ya sığmıyorsa CPU mode (`num_gpu: 0`) dene — ama çok yavaş olur (30-180sn/tur). En hızlı seçenek GPU'ya tam sığan modeli kullanmaktır.

**CPU mode denemesi başarısız oldu (13 May 2026):**
`ollama create gemma4-cpu -f` ile Modelfile oluşturup `PARAMETER num_gpu 0` ayarı yapıldı ancak model yüklenemedi (curl timeout). Doğrudan API'da `"options": {"num_gpu": 0}` da çalışmadı. 8B model CPU'da da stabil çalışmadı.

### 7. Konu havuzu yaklaşımı (siber güvenlik varyantı)
Ollama döngüsü için genel prompt yerine **önceden yazılmış konu havuzu** kullanmak daha efektiftir. Özellikle siber güvenlik gibi spesifik bir alanda Ollama'nın rastgele konu seçmesi yerine, 100+ konuluk havuzdan sırayla işlemek daha verimlidir.

Detaylı siber güvenlik döngüsü: `references/ollama-siber-guvenlik-loop.md`

### 8. Ortam temizliği (Ollama restart)
Model değiştirirken veya döngü hata verdiğinde:
1. `cmd.exe //c "taskkill /F /IM ollama.exe"` ile tüm ollama süreçlerini öldür
2. `ollama serve`'i background'da yeniden başlat
3. 5-8sn bekle, sonra `curl http://localhost:11434/api/version` ile hazır olduğunu doğrula

## Kullanım Senaryoları

- **Bilgi aktarımı:** Ollama'daki fine-tune edilmiş modellerin bilgisini Hermes skill'lerine dönüştürmek
- **Müfredat öğrenimi:** Her tur farklı bir konu — programlama, güvenlik, ağ, donanım, veri bilimi
- **Sürekli gelişim:** Kullanıcı izlerken arka planda otomatik skill üretimi
