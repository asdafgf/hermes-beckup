# Ollama Siper Güvenlik Eğitim Döngüsü

## Ne İşe Yarar

Ollama'daki yerel modeli kullanarak siber güvenlik konularında Hermes skill kütüphanesini büyütmek. Her turda farklı bir siber güvenlik konusu işlenir, Python kod örnekleriyle birlikte skill olarak kaydedilir.

## Özellikler

- Önceden yazılmış 100+ siber güvenlik konusu havuzu (tekrar önleme)
- Her konuda Python kodu örneği zorunlu
- Saldırı + savunma + test yöntemi + iz bırakmama birlikte anlatılır
- Skill'ler `ollama-guvenlik-*` önekiyle kaydedilir
- Kesintisiz döngü, kullanıcı durdurana kadar devam eder

## Çalışan Python Kod

```python
import urllib.request
import json
import os
import re
import time
from datetime import datetime

SKILLS_DIR = os.path.expanduser("~/.hermes/skills")
OUT_FILE = os.path.expanduser("~/siber_output.txt")
OLLAMA_MODEL = "gemma3:4b"  # GPU'ya sığan model seç!

def log(msg):
    print(msg, flush=True)
    with open(OUT_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
        f.flush()

def talk(prompt):
    data = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"num_ctx": 4096, "temperature": 0.7}
    }).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate",
        data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.loads(resp.read())["response"]

def cname(text):
    text = re.sub(r'[*_#`\'\"\(\)\[\]\?\!\.]', '', text)
    text = text.lower().replace(' ', '-')
    for o,n in {'ı':'i','ğ':'g','ü':'u','ş':'s','ö':'o','ç':'c'}.items():
        text = text.replace(o, n)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')[:55]

def save_skill(topic, content, turn):
    clean = cname(topic) or f"ders-{turn}"
    name = f"ollama-guvenlik-{clean}"
    path = os.path.join(SKILLS_DIR, f"{name}.md")
    
    code_blocks = re.findall(r'```python\n(.*?)```', content, re.DOTALL)
    code_section = ""
    if code_blocks:
        code_section = "\n\n## Python Kod Örnekleri\n\n```python\n" + \
            "\n\n".join(code_blocks) + "\n```\n"

    md = f"""---
name: {name}
description: "Siber guvenlik - Ollama({OLLAMA_MODEL}) Tur {turn}: {topic}"
category: guvenlik
created_by: agent
turn: {turn}
created_at: {datetime.now().isoformat()}
---

# {topic}

## Ders (Tur {turn})

{content}
{code_section}
---
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    return path

# Konu havuzu (buraya 100+ konu yazılır)
TOPICS = [
    "Port Tarama ve Servis Tespiti (Nmap, Python socket)",
    "SQL Injection - Tespit ve Exploit (Python ile)",
    "ARP Spoofing ve MITM Saldirisi (Python Scapy ile)",
    # ... devamı
]

turn = 1; idx = 0; existing = set()
# ... döngü
```

## Konu Havuzu (100+ konu)

Tam konu listesi `siber_loop_v2.py` dosyasındaki `TOPICS` dizisinde bulunur. Ana başlıklar:

- **Ağ & Port:** Port tarama, zafiyet tarama, Wireshark, ARP spoofing, DNS spoofing, VPN
- **Web Güvenliği:** SQLi, XSS, CSRF, LFI/RFI, SSRF, JWT, API, File Upload, Session hijacking
- **Parola & Kripto:** Hash kırma, şifreleme, SSL/TLS, brute force
- **Windows:** Yetki yükseltme, Powershell, Process injection, Registry, Event log, Defender bypass
- **Linux:** Yetki yükseltme, log kaçış, cron, SUID/SGID
- **Exploit:** Buffer overflow, ROP, Format string, Use-after-free, Fuzzing
- **Reverse & Malware:** Binary analizi, Anti-debug, PE/ELF, Malware analizi, Shellcode
- **Kablosuz:** WPA kırma, Evil twin, Deauth, Bluetooth
- **Python Araçları:** Port scanner, Keylogger, Reverse shell, Payload, Steganography, Scapy
- **İz Bırakmama (OpSec):** Tor, Log silme, Timestomping, Anti-forensics, MAC spoofing, C2, .onion
- **Araçlar (Kali):** Metasploit, Burp Suite, Hydra, Aircrack, sqlmap, Hashcat, BloodHound
- **Test Metodolojisi:** PT lifecycle, Recon, Exploitation, Post-exploit, Red/Blue team
- **Savunma:** WAF, SIEM, EDR, Honeypot, Incident Response, Zero Trust, Container, Cloud
- **Güvenli Kodlama:** Input validation, Session, Data storage, API, ASVS, Supply chain
- **Özel:** IoT, Active Directory (Kerberos/NTLM), Pass-the-Hash, DLL Injection, ETW bypass, AMSI bypass

## Önemli Uyarılar

1. **GPU/VRAM kontrolü yap:** `nvidia-smi` ile VRAM'i kontrol et. 8B+ modeller 8GB VRAM'e sığmaz.
2. **Ollama restart:** Model değişikliğinde `taskkill /F /IM ollama.exe` + `ollama serve` yap.
3. **Skill sayısı:** Her tur 1 skill. `ollama-guvenlik-*` ile filtrele/temizle.
4. **Dosya adı:** Türkçe karakterleri ve `*_#` işaretlerini temizle — Windows hata verir.
