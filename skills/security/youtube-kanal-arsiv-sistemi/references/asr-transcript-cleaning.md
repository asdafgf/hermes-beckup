# YouTube ASR Transcript Temizleme ve Skill İsmi Oluşturma

## Sorun
YouTube otomatik altyazı (ASR) transcript'lerinde 3 yaygın kirlilik:
1. **Tekrarlanan kelimeler**: `for later for later for later but but but`
2. **Giriş cümleleri**: `hey everyone`, `all righty`, `welcome back`, `before we dive into this video`
3. **[Music] etiketleri**: `[Music] [Music] [Music]`

## Çözüm 1: ASR Tekrarlarını Temizle
```python
import re
text = re.sub(r'(\b\w+\b)( \1\b){2,}', r'\1', text)
```

## Çözüm 2: Skill İsmi Üretme

```python
# 1. Önce keyword'lerden dene (en iyi sonuç)
keywords = extract_keywords(text)  # güvenlik terim havuzundan
if keywords:
    name = '-'.join(keywords[:3])
    name = re.sub(r'[^a-z0-9-]', '', name.lower())

# 2. Cümle başlığından dene (keyword yoksa)
skip_patterns = [
    r'^hey\b', r'^all right', r'^alrighty', r'^hello\b',
    r'^well hey', r'^before dive', r'^what.s\b', r'^righty',
    r'^thanks', r'^welcome', r'^guys\b', r'^everyone\b',
    r'^okay\b', r'^so\b', r'^now\b',
]
for sp in skip_patterns:
    if re.search(sp, first_sentence.lower()):
        # 2. cümleyi dene
        parts = text.split('.')
        if len(parts) > 1:
            first_sentence = parts[1].strip()
        break

words = first_sentence.split()[:6]
name = '-'.join([w.lower().strip('.,!?') for w in words if len(w) > 2])
name = re.sub(r'[^a-z0-9-]', '', name)
```

## Çözüm 3: Toplu Temizlik (Silinecek Skill'leri Belirleme)

### Aşama 1 — Giriş cümlesi kalıpları
```python
garbage_patterns = [
    r'^music[\- ]', r'^hey[\- ]', r'^hello[\- ]', r'^alrighty',
    r'^all[\- ]?right', r'^well[\- ]hey', r'^thanks[\- ]much',
    r'^before[\- ]dive', r'^guys[\- ]', r'^everyone[\- ]',
    r'^whats[\- ]going', r'^hows[\- ]going', r'^righty[\- ]',
    r'^for[\- ]later', r'^this[\- ]video', r'^lets[\- ]',
    r'^gonna[\- ]', r'^okay[\- ]', r'^so[\- ]',
    r'^now[\- ]again', r'^short[\- ]video', r'^just[\- ]',
    r'^alrighty$', r'^all[\- ]right$', r'^python$',
    r'^theres[\- ]', r'^ill[\- ]start', r'^weve[\- ]now',
]
```

### Aşama 2 — Anlamlı keyword içermeyenler
```python
meaningful_keywords = [
    'malware', 'ransomware', 'phishing', 'exploit', 'payload',
    'backdoor', 'trojan', 'windows', 'linux', 'bash', 'python',
    'powershell', 'active', 'entra', 'azure', 'network', 'firewall',
    'cisco', 'ccna', 'ai', 'gpt', 'cloud', 'docker', 'kubernetes',
    'ctf', 'hack', 'android', 'root', 'wireshark', 'nmap',
    'password', 'credential', 'bypass', 'vpn', 'tor',
]
def is_meaningful(name):
    name_lower = name.lower().replace('-', '')
    return any(kw.replace('-', '') in name_lower for kw in meaningful_keywords)
```

### Korunacak Özel Skill'ler
```python
protected = [
    'john-hammond-siber-guvenlik-arsivi',
    'siber-guvenlik-agentic-ai',
    # ... tüm siber-guvenlik-* skill'leri
    'youtube-kanal-arsiv-sistemi',
]
```

## Sonuç
- 1.208 skill'den → 532 anlamsız silindi → **324 temiz skill kaldı**
- Anlamlı/Anlamsız oranı: ~%45 temiz
