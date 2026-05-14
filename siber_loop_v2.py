import urllib.request
import json
import os
import re
import time
from datetime import datetime

SKILLS_DIR = os.path.expanduser("~/.hermes/skills")
OUT_FILE = os.path.expanduser("~/siber_output.txt")
OLLAMA_MODEL = "gemma4-cpu"

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
        "options": {
            "num_ctx": 4096,
            "temperature": 0.7
        }
    }).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=data, headers={"Content-Type": "application/json"})
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
        code_section = "\n\n## Python Kod Örnekleri\n\n```python\n" + "\n\n".join(code_blocks) + "\n```\n"

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

## Kullanım

Siber guvenlik skill'i. Ollama ({OLLAMA_MODEL}) tarafindan ogretilmistir.
Iz birakmamak ve guvenli test yapmak onceliklidir.
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    return path, name

log("=== SIBER GUVENLIK (gemma4:8B) BASLADI ===")
log("Model: gemma4:latest (8B)")
log("Tum skill'ler: ollama-guvenlik-* olarak kaydedilecek")
log("")

existing = set(f.replace(".md","") for f in os.listdir(SKILLS_DIR) if f.startswith("ollama-guvenlik-"))
log(f"Mevcut guvenlik skill: {len(existing)}")
log("")

TOPICS = [
    # Ag & Port
    "Port Tarama ve Servis Tespiti (Nmap, Python socket)",
    "Ag Zafiyet Taramasi (Nessus, OpenVAS, Python script)",
    "Wireshark ile Trafik Analizi",
    "ARP Spoofing ve MITM Saldirisi (Python Scapy ile)",
    "DNS Spoofing ve Zehirlemesi",
    "VPN ve Tnel Protokolleri",
    
    # Web Guvenligi
    "SQL Injection - Tespit ve Exploit (Python ile)",
    "SQL Injection - Savunma ve Parameterized Queries",
    "XSS Saldirilari - Reflected, Stored, DOM-based",
    "XSS Saldirilari - Savunma ve Output Encoding",
    "CSRF Saldirilari ve SameSite Cerekler",
    "LFI/RFI Zafiyetleri ve Savunma",
    "SSRF Zafiyetleri ve Savunma",
    "JWT Guvenligi ve Token Manipulasyonu",
    "API Guvenlik Testleri ve Rate Limiting",
    "File Upload Zafiyetleri ve Guvenli Dosya Yonetimi",
    "Session Hijacking ve Fixation",
    "OWASP Top 10 - Derinlemesine Analiz",
    
    # Parola & Kripto
    "Hash Kirma Teknikleri (Python ile Hashcat benzeri)",
    "Simetrik ve Asimetrik Sifreleme (Python crypto kodu)",
    "SSL/TLS ve Sertifika Guvenligi",
    "Brute Force ve Dictionary Saldirilari (Python ile)",
    
    # Windows
    "Windows Yetki Yukseltme Teknikleri",
    "Windows Powershell ile Post-Exploit",
    "Windows Process Injection ve API Hooking",
    "Windows Registry ve GPO Guvenligi",
    "Windows Event Log Manipulasyonu",
    "Windows Defender ve AV Bypass",
    
    # Linux
    "Linux Yetki Yukseltme (SUID, Kernel Exploit)",
    "Linux Sistem Loglarindan Kacis",
    "Linux Cron ve Service Manipulasyonu",
    "Linux SUID/SGID ve Capabilities",
    
    # Exploit
    "Buffer Overflow - Temel (Python ile)",
    "ROP Zincirleri ile ASLR Bypass",
    "Format String Zafiyetleri",
    "Use-After-Free ve Heap Exploitation",
    "Fuzzing Teknikleri (Python ile)",
    
    # Reverse & Malware
    "Reverse Engineering - Binary Analizi (Python pefile ile)",
    "Reverse Engineering - Anti-Debug ve Anti-VM",
    "PE/ELF Dosya Analizi (Python ile)",
    "Malware Analizi - Statik ve Dinamik",
    "Shellcode Analizi ve Olusturma",
    
    # Kablosuz
    "WPA/WPA2 Kirma ve El Ayak Izleri",
    "Evil Twin ve Rogue AP Saldirilari",
    "Deauth Saldirilari",
    "Bluetooth Guvenligi",
    
    # Python Araclari
    "Python ile Port Scanner (socket, threading)",
    "Python ile Keylogger",
    "Python ile Reverse Shell ve Bind Shell",
    "Python ile Payload Olusturma ve Encoder/Decoder",
    "Python ile ZIP/PDF Sifre Kirma",
    "Python ile Steganography (veri gizleme)",
    "Python ile Network Monitor",
    "Python ile Brute Force Aracı",
    "Python ile Paket Yakalama ve Analiz (Scapy)",
    "Python ile Web Scraper ve Crawler (guvenlik test)",
    "Python ile Proxy ve Tunnel",
    
    # Iz Birakmama
    "Proxy Zincirleri ve Tor Kullanimi",
    "Log Silme ve Manipulasyonu (Windows/Linux)",
    "Timestomping - Dosya Zaman Damgasi Degistirme",
    "Anti-Forensics - Disk ve Memory'den Kacis",
    "MAC Adres Spoofing ve Parmakizi Gizleme",
    "User-Agent ve Browser Fingerprint Manipulasyonu",
    "C2 Haberlesme ve DNS-over-HTTPS",
    "Tor Hidden Services (.onion) ve I2P",
    "Digital Signature Spoofing",
    "Disk Sifreleme ve Veri Gizleme (Python ile)",
    
    # Araclar (Kali)
    "Metasploit Framework - Modul ve Payload",
    "Burp Suite - Web Zafiyet Tarama",
    "Hydra ve John the Ripper - Parola Kirma",
    "Aircrack-ng Suite - Kablosuz Saldiri",
    "sqlmap - Otomatik SQL Injection",
    "Hashcat - GPU ile Hash Kirma",
    "Responder ve Impacket - Windows Ag",
    "BloodHound - AD Zafiyet Kesfi",
    "Bettercap - Ag Saldiri Platformu",
    "Netcat ve Socat - Ters Kabuk ve Dosya Transferi",
    
    # Test Metodolojisi
    "Penetration Testing Lifecycle - Adim Adim",
    "Reconnaissance - Bilgi Toplama Teknikleri",
    "Zafiyet Analizi ve Exploitasyon",
    "Post-Exploitasyon ve Veri Toplama",
    "Red Team vs Blue Team",
    "Raporlama ve Kanit Sunumu",
    
    # Savunma
    "WAF ve Web Application Firewall Bypass",
    "SIEM ve Log Yonetimi (Splunk, ELK)",
    "EDR ve XDR Cozumleri - Tespit ve Kacis",
    "Honeypot Kurulumu ve Tuzak Sistemleri",
    "Incident Response - Olay Mudahale Plani",
    "Zero Trust Mimarisi",
    "Container Guvenligi (Docker/Kubernetes)",
    "Cloud Guvenligi (AWS/Azure/GCP)",
    "Mobile App Guvenligi (Android/iOS)",
    
    # Guvenli Kodlama
    "Input Dogrulama ve Sanitizasyon (Python)",
    "Guvenli Kimlik Dogrulama ve Session",
    "Guvenli Veri Depolama ve Sifreleme",
    "Guvenli API Tasarimi",
    "OWASP ASVS - Application Security Verification",
    "Dependency Guvenligi ve Supply Chain",
    
    # Sosyal Muhendislik
    "Phishing ve Spear Phishing Teknikleri",
    "Pretexting ve Baiting",
    "Sosyal Muhendislikten Korunma",
    
    # Ozel Konular
    "IoT Cihaz Guvenligi",
    "Active Directory - Kerberos ve NTLM",
    "Pass-the-Hash ve Pass-the-Ticket",
    "DLL Injection ve Reflective Loading (Python/ctypes)",
    "ETW (Event Tracing for Windows) Bypass",
    "AMSI (Anti-Malware Scan Interface) Bypass",
    "Python ile Process Hollowing",
    "Python ile Shellcode Enjeksiyonu",
    "Python ile DLL Side-Loading",
]

recent = []
turn = 1
idx = 0
fails = 0

while True:
    try:
        if os.path.exists(os.path.expanduser("~/.hermes/STOP")):
            os.remove(os.path.expanduser("~/.hermes/STOP"))
            log("DURAKLATILDI."); break

        topic = TOPICS[idx % len(TOPICS)]
        idx += 1
        
        log(f"{'='*60}")
        log(f"TUR {turn}")
        log(f"KONU: {topic}")
        log(f"{'='*60}")

        prompt = (
            f"Sen bir siber guvenlik uzmanisin. Hermes AI'ya siber guvenlik ogretiyorsun. Tur {turn}.\n"
            f"Konu: {topic}\n\n"
            f"KURALLAR:\n"
            f"- Kisa oz anlat (5-10 cumle)\n"
            f"- ```python ile kod ornegi ver\n"
            f"- Iz birakmamak icin yapilmasi gerekeni belirt\n"
            f"- Test/Saldiri ve Savunma yonlerini birlikte anlat\n\n"
            f"FORMAT:\n"
            f"KONU: {topic}\n"
            f"OGRET: [icerik]\n"
            f"KOD: [python kodu]\n"
            f"TEST: [test yontemi]\n"
            f"KORUNMA: [iz birakmamak icin]"
        )

        t1 = time.time()
        resp = talk(prompt)
        t2 = time.time()
        
        path, sname = save_skill(topic, resp, turn)
        is_new = sname not in existing
        existing.add(sname)
        total = len([f for f in os.listdir(SKILLS_DIR) if f.startswith("ollama-guvenlik-")])

        log(f"Suresi: {t2-t1:.0f}s")
        if is_new:
            log(f"✓ YENI SKILL | Tur #{turn} | {topic}")
        else:
            log(f"~ GUNCELLENDI | Tur #{turn} | {topic}")
        log(f"Dosya: {path}")
        log(f"Toplam guvenlik skill: {total}")
        log(f"{'─'*60}")
        log("")

        time.sleep(1)
        turn += 1

    except KeyboardInterrupt:
        log("Klavye durdurdu."); break
    except Exception as e:
        log(f"HATA tur {turn}: {e}")
        import traceback; traceback.print_exc()
        time.sleep(5); turn += 1; continue
