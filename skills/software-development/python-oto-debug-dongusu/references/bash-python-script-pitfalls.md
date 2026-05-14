# Bash & Python Script Hazırlama Tuzakları (Windows git-bash)

Bu referans, Hermes'in Windows git-bash ortamında script yazarken karşılaştığı yaygın syntax hatalarını ve çözümlerini içerir.

## 1. Bash Parantez Tuzağı

**Sorun:** Windows git-bash'te `echo` ve `# yorum` satırlarında parantez `()` kullanmak syntax hatası verir.

```
# HATALI:
echo "=== KONU 1: Agentic AI (Otonom Ajanlar) ==="
# Bu da hatalı: # ===== KONU 1: SIFIR GUVEN (ZT) =====

# DOĞRU:
echo "=== KONU 1: Agentic AI ==="
# -- KONU 1: SIFIR GUVEN ZT --
```

**Neden:** Bash parantezleri alt-shell olarak yorumlar. Yorum satırındaki `(metin)` bile syntax error'a yol açar.

**Çözümler:**
- `(...)` yerine `[...]` kullan: `echo "Sifir Guven [Zero Trust]"`
- Veya parantezi tamamen kaldır
- `sed` ile toplu temizlik yaparken fonksiyon isimlerini koru:
  ```bash
  # SADECE yorum ve echo satırlarını temizle, fonksiyon tanımlarını koru
  sed -i '/^#/ s/(/[/g; /^#/ s/)/]/g; /^echo/ s/(/[/g; /^echo/ s/)/]/g' script.sh
  ```

## 2. Python Tek Tırnak / Apostrof Tuzağı

**Sorun:** Python'da tek tırnaklı string içinde apostrof kullanmak syntax hatası verir.

```python
# HATALI:
prompt = 'Sen CLAUDE CODE'sun. ...'  # 'sun' tanımsız string

# DOĞRU - çift tırnak:
prompt = "Sen CLAUDE CODE'sun. ..."

# DOĞRU - escape:
prompt = 'Sen CLAUDE CODE\'sun. ...'

# EN İYİSİ - json.dumps() kullan:
payload = json.dumps({"prompt": "Sen CLAUDE CODE'sun..."})
```

## 3. Windows /tmp/ Yok

**Sorun:** Linux'ta `/tmp/` çalışır, Windows'ta çalışmaz.

```bash
# HATALI:
echo "$payload" > /tmp/payload.json   # Windows'ta dosya oluşmaz

# DOĞRU - geçerli dizini kullan:
echo "$payload" > payload.json

# DOĞRU - AppData Local Temp:
TEMP_DIR="$HOME/AppData/Local/Temp"
echo "$payload" > "$TEMP_DIR/payload.json"

# EN İYİSİ - Python ile yaz:
python -c "
import json
with open('payload.json', 'w') as f:
    f.write(json.dumps({...}))
"
```

## 4. curl Payload Gönderme

**Sorun:** Uzun prompt'ları curl komut satırına gömmek tırnak çakışmasına yol açar.

```bash
# HATALI - tırnak iç içe:
curl -d '{"prompt":"... 'içinde tek tırnak' ..."}' ...

# DOĞRU - önce dosyaya yaz, sonra curl -d @file:
python -c "
import json
payload = json.dumps({'model':'qwen2.5-coder:7b','prompt':'metin','stream':False})
with open('payload.json','w') as f: f.write(payload)
"
curl -s -X POST http://localhost:11434/api/generate -d @payload.json

# YA DA - urllib.request kullan (Python içinden):
import urllib.request, json
req = urllib.request.Request(
    'http://localhost:11434/api/generate',
    data=json.dumps({...}).encode(),
    headers={'Content-Type': 'application/json'}
)
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())['response']
```

## 5. Python `False` vs `false` (JSON)

**Sorun:** Python `json.dumps({'stream':False})` doğru, `{'stream':false}` NameError verir.

```python
# DOĞRU:
payload = json.dumps({'model':'x','prompt':'y','stream':False})

# YANLIŞ - NameError: name 'false' is not defined:
payload = json.dumps({'model':'x','prompt':'y','stream':false})
```
