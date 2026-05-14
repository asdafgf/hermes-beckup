import urllib.request, json, os, re, time
from datetime import datetime

SKILLS_DIR = os.path.expanduser("~/.hermes/skills")
OUT = os.path.expanduser("~/siber_cikti.txt")
MODEL = "gemma3:4b"

def log(m):
    print(m, flush=True)
    with open(OUT, "a", encoding="utf-8") as f:
        f.write(m + "\n"); f.flush()

def api(prompt):
    d = json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "options": {"num_ctx": 4096}}).encode()
    r = urllib.request.Request("http://localhost:11434/api/generate", data=d, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=120) as resp:
        return json.loads(resp.read())["response"]

def cname(t):
    t = re.sub(r'[*_#`\'\"\(\)\[\]\?\!\.]', '', t).lower().replace(' ', '-')
    for o, n in {'ı':'i','ğ':'g','ü':'u','ş':'s','ö':'o','ç':'c'}.items(): t = t.replace(o, n)
    return re.sub(r'-+', '-', t).strip('-')[:55]

def save(topic, content, turn):
    cl = cname(topic) or f"ders-{turn}"
    name = f"guvenlik-{cl}"
    path = os.path.join(SKILLS_DIR, f"{name}.md")
    
    kodlar = re.findall(r'```python\n(.*?)```', content, re.DOTALL)
    kod_bolum = "\n\n## Python Kod\n\n```python\n" + "\n\n".join(kodlar) + "\n```" if kodlar else ""
    
    md = f"""---
name: {name}
description: "Siber guvenlik - {MODEL} Tur {turn}: {topic}"
category: guvenlik
created_by: agent
turn: {turn}
created_at: {datetime.now().isoformat()}
---

# {topic}

{content}
{kod_bolum}

---
## Guvenlik Uyarisi
Sadece egitim ve test amaciyla kullanin. Iz birakmamak icin:
- VM/sandbox kullan
- VPN/Tor ile baglan
- Test aginda calis
"""
    with open(path, "w", encoding="utf-8") as f: f.write(md)
    return path, name

# Once Ollama'nin hazir oldugunu test et
for i in range(5):
    try:
        api("Merhaba. EVET yaz.")
        log("Ollama hazir.")
        break
    except:
        log(f"Ollama bekleniyor ({i+1}/5)...")
        time.sleep(5)

KONULAR = [
    "Port Tarama (Nmap, Python socket)",
    "SQL Injection - Tespit ve Exploit (Python ile)",
    "SQL Injection - Savunma (Parameterized Queries)",
    "XSS Saldirilari (Reflected, Stored, DOM) ve Korunma",
    "CSRF ve SameSite Cookie Guvenligi",
    "LFI/RFI Zafiyetleri ve Savunma",
    "SSRF Zafiyetleri",
    "JWT Guvenligi ve Token Manipulasyonu",
    "API Guvenlik Testleri",
    "File Upload Zafiyetleri",
    "Hash Kirma Teknikleri (Python ile)",
    "Simetrik/Asimetrik Sifreleme (Python crypto)",
    "Brute Force ve Dictionary Saldirilari (Python)",
    "ARP Spoofing ve MITM (Scapy ile)",
    "DNS Spoofing",
    "Wireshark ile Trafik Analizi",
    "Windows Yetki Yukseltme",
    "Linux Yetki Yukseltme (SUID, Kernel)",
    "Windows Powershell Post-Exploit",
    "Linux Log Kacis ve Temizlik",
    "Process Injection ve API Hooking",
    "Buffer Overflow Temel (Python ile)",
    "ROP ile ASLR Bypass",
    "Format String Zafiyetleri",
    "Reverse Engineering - Binary Analizi",
    "Malware Analizi (Statik/Dinamik)",
    "Shellcode Olusturma",
    "WPA/WPA2 Kirma",
    "Evil Twin ve Rogue AP",
    "Python ile Keylogger",
    "Python ile Reverse Shell",
    "Python ile Port Scanner (threading)",
    "Python ile Payload Encoder/Decoder",
    "Python ile Steganography",
    "Python ile ZIP/PDF Sifre Kirma",
    "Python ile Brute Force Araci",
    "Python ile Network Monitor (Scapy)",
    "Python ile Web Crawler (guvenlik test)",
    "Python ile Proxy ve Tunnel",
    "Proxy Zincirleri ve Tor",
    "Log Silme - Windows Event Log",
    "Log Silme - Linux syslog/bash_history",
    "Timestomping (Dosya Zaman Damgasi)",
    "Anti-Forensics Teknikleri",
    "MAC Adres Spoofing",
    "User-Agent ve Parmakizi Gizleme",
    "C2 Haberlesme ve DNS-over-HTTPS",
    "Tor Hidden Services (.onion)",
    "Metasploit - Modul ve Payload",
    "Burp Suite - Web Zafiyet Tarama",
    "Hydra ve John the Ripper",
    "Aircrack-ng Suite",
    "Hashcat - GPU Hash Kirma",
    "sqlmap - SQL Injection",
    "Responder ve Impacket - Windows Ag",
    "BloodHound - AD Kesif",
    "Bettercap - Ag Saldirilari",
    "Penetration Test Lifecycle",
    "Reconnaissance - Bilgi Toplama",
    "Red Team vs Blue Team",
    "WAF Bypass Teknikleri",
    "SIEM ve Log Yonetimi",
    "EDR Tespit ve Kacis",
    "Honeypot ve Tuzak Sistemleri",
    "Incident Response",
    "Zero Trust Mimarisi",
    "Container Guvenligi (Docker/K8s)",
    "Cloud Guvenligi (AWS/Azure/GCP)",
    "Guvenli Kodlama - Input Dogrulama",
    "Guvenli Kodlama - Session Yonetimi",
    "Guvenli Kodlama - API Tasarimi",
    "Phishing ve Spear Phishing",
    "IoT Cihaz Guvenligi",
    "Active Directory - Kerberos NTLM",
    "Pass-the-Hash ve Pass-the-Ticket",
    "DLL Injection (Python ctypes ile)",
    "AMSI Bypass Teknikleri",
    "ETW Bypass",
    "Python ile Process Hollowing",
    "Python ile Shellcode Enjeksiyonu",
]

mevcut = set(f.split(".md")[0] for f in os.listdir(SKILLS_DIR) if f.startswith("guvenlik-"))
log(f"=== SIBER GUVENLIK BASLADI ===")
log(f"Cihaz: RTX 4070 8GB + i7-13700HX")
log(f"Model: {MODEL} (3.3GB - GPU'ya tam sigar)")
log(f"Mevcut guvenlik skill: {len(mevcut)}")
log(f"Hedef: {len(KONULAR)} farkli konu + sonsuz dongu")
log("")

turn = 1
idx = 0

while True:
    try:
        if os.path.exists(os.path.expanduser("~/.hermes/STOP")):
            os.remove(os.path.expanduser("~/.hermes/STOP")); log("DURDURULDU."); break

        konu = KONULAR[idx % len(KONULAR)]
        idx += 1

        log(f"{'='*60}")
        log(f"TUR {turn}")
        log(f"KONU: {konu}")
        log(f"{'='*60}")

        t1 = time.time()
        yanit = api(
            f"Sen siber guvenlik uzmanisin. Hermes AI'ya ogret. Tur {turn}.\n"
            f"Konu: {konu}\n\n"
            f"KURALLAR:\n- 5-10 cumle anlat\n- ```python ile kod ornegi ver\n- Iz birakmamak icin yapilmasi gerekeni belirt\n- Saldiri ve savunma yonlerini anlat\n\n"
            f"FORMAT:\nKONU: {konu}\nOGRET: [icerik]\nKOD: [python kodu]\nIZ: [iz birakmamak icin]\nTEST: [test yontemi]"
        )
        sure = time.time() - t1

        path, sname = save(konu, yanit, turn)
        yenimi = sname not in mevcut
        mevcut.add(sname)
        toplam = len([f for f in os.listdir(SKILLS_DIR) if f.startswith("guvenlik-")])

        log(f"Süre: {sure:.0f}s")
        log(f"{'YENI' if yenimi else 'TEKRAR'} SKILL | Tur {turn} | {konu}")
        log(f"Dosya: {path}")
        log(f"Toplam guvenlik skill: {toplam}")
        log(f"{'─'*60}")
        log("")

        time.sleep(1)
        turn += 1

    except KeyboardInterrupt:
        log("Klavye durdurdu."); break
    except Exception as e:
        log(f"HATA tur {turn}: {e}")
        import traceback; traceback.print_exc()
        time.sleep(5); continue
