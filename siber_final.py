import urllib.request, json, os, re, time, sys
from datetime import datetime

SKILLS_DIR = os.path.expanduser("~/.hermes/skills")
OUT = os.path.expanduser("~/.hermes/logs/siber_loop.log")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
MODEL = "gemma3:4b"

def log(m):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {m}"
    print(line, flush=True)
    with open(OUT, "a", encoding="utf-8") as f:
        f.write(line + "\n"); f.flush()

def api(prompt, max_wait=120):
    d = json.dumps({
        "model": MODEL, "prompt": prompt, "stream": False,
        "options": {"num_ctx": 2048, "temperature": 0.7}
    }).encode()
    r = urllib.request.Request("http://localhost:11434/api/generate", data=d,
                                headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=max_wait) as resp:
        return json.loads(resp.read())["response"]

def cname(t):
    t = re.sub(r'[*_#`\'"()\[\]?!.,:;]', '', t).lower().replace(' ', '-')
    for o, n in {'\u0131':'i','\u011f':'g','\u00fc':'u','\u015f':'s','\u00f6':'o','\u00e7':'c'}.items():
        t = t.replace(o, n)
    return re.sub(r'-+', '-', t).strip('-')[:55]

def save(topic, content, turn):
    cl = cname(topic) or f"ders-{turn}"
    name = f"guvenlik-{cl}"
    path = os.path.join(SKILLS_DIR, f"{name}.md")
    kodlar = re.findall(r'```python\n(.*?)```', content, re.DOTALL)
    ks = "\n\n## Python Kod\n\n```python\n" + "\n\n".join(kodlar) + "\n```" if kodlar else ""
    md = f"""---
name: {name}
description: "Siber guvenlik - {MODEL} Tur {turn}: {topic}"
category: guvenlik
created_by: agent
turn: {turn}
created_at: {datetime.now().isoformat()}
---

# {topic}

{content}{ks}

---
## Guvenlik Uyarisi
Sadece egitim ve test icindir. VM/sandbox kullan, VPN/Tor ile baglan.
"""
    with open(path, "w", encoding="utf-8") as f: f.write(md)
    return path, name

# === Ollama'yi bekle ve modeli yukle ===
log("Ollama hazir mi kontrol...")
for i in range(10):
    try:
        urllib.request.urlopen("http://localhost:11434/api/version", timeout=3)
        break
    except:
        log(f"Ollama bekleniyor ({i+1}/10)...")
        time.sleep(3)

# Modeli once yukle (warm-up)
log("Model yukleniyor...")
try:
    api("Merhaba. Sadece HAZIR yaz.", 180)
    log("Model hazir!")
except:
    log("Model yukleme basarisiz!")
    sys.exit(1)

# === MEVCUT SKILL'LER ===
mevcut = set()
for f in os.listdir(SKILLS_DIR):
    if f.startswith("guvenlik-") and f.endswith(".md"):
        mevcut.add(f.replace(".md", ""))

log(f"Mevcut guvenlik skill: {len(mevcut)}")

KONULAR = [
    "Port Tarama (Nmap, Python socket)",
    "SQL Injection - Tespit ve Exploit (Python ile)",
    "SQL Injection - Savunma (Parameterized Queries)",
    "XSS Saldirilari (Reflected, Stored, DOM)",
    "XSS Korunma (Output Encoding, CSP)",
    "CSRF ve SameSite Cookie",
    "LFI/RFI Zafiyetleri",
    "SSRF Zafiyetleri ve Savunma",
    "JWT Guvenligi ve Token Manipulasyonu",
    "API Guvenlik Testleri ve Rate Limiting",
    "File Upload Zafiyetleri",
    "Session Hijacking ve Fixation",
    "OWASP Top 10 Genel Bakis",
    "Hash Kirma (Python ile hashcat benzeri)",
    "Simetrik Sifreleme (Python cryptography)",
    "Asimetrik Sifreleme (RSA, ECC)",
    "SSL/TLS ve Sertifika Guvenligi",
    "Brute Force ve Dictionary Saldirilari",
    "ARP Spoofing ve MITM (Scapy ile)",
    "DNS Spoofing ve Zehirlemesi",
    "Wireshark ile Trafik Analizi",
    "VPN ve Tnel Protokolleri",
    "Windows Yetki Yukseltme",
    "Linux Yetki Yukseltme (SUID, Kernel)",
    "Windows Powershell ile Post-Exploit",
    "Linux Log Kacis ve Temizlik",
    "Windows Event Log Manipulasyonu",
    "Windows Defender ve AV Bypass",
    "Process Injection ve API Hooking",
    "Buffer Overflow (Python ile exploit)",
    "ROP ile ASLR Bypass",
    "Format String Zafiyetleri",
    "Reverse Engineering - Binary Analizi",
    "Malware Analizi - Statik ve Dinamik",
    "Shellcode Olusturma ve Analiz",
    "WPA/WPA2 Kirma",
    "Evil Twin ve Rogue AP",
    "Bluetooth Guvenligi",
    "Python ile Keylogger",
    "Python ile Reverse Shell",
    "Python ile Bind Shell",
    "Python ile Port Scanner (threading)",
    "Python ile Payload Encoder/Decoder",
    "Python ile Steganography (veri gizleme)",
    "Python ile ZIP/PDF Sifre Kirma",
    "Python ile Brute Force Araci",
    "Python ile Network Monitor (Scapy)",
    "Python ile Web Crawler (guvenlik test)",
    "Python ile Proxy ve Tunnel",
    "Python ile Process Hollowing",
    "Python ile Shellcode Enjeksiyonu",
    "Python ile DLL Injection (ctypes)",
    "Proxy Zincirleri ve Tor Kullanimi",
    "Log Silme - Windows/Linux",
    "Timestomping (Dosya Zaman Damgasi)",
    "Anti-Forensics Teknikleri",
    "MAC Adres Spoofing",
    "User-Agent ve Parmakizi Gizleme",
    "C2 Haberlesme ve DNS-over-HTTPS",
    "Tor Hidden Services (.onion)",
    "Metasploit - Modul ve Payload Kullanimi",
    "Burp Suite - Web Zafiyet Tarama",
    "Hydra ve John the Ripper",
    "Aircrack-ng Suite",
    "Hashcat - GPU ile Hash Kirma",
    "sqlmap - Otomatik SQL Injection",
    "Responder ve Impacket",
    "BloodHound - AD Zafiyet Kesfi",
    "Bettercap - Ag Saldiri Platformu",
    "Penetration Test Lifecycle",
    "Bilgi Toplama (Reconnaissance)",
    "Red Team vs Blue Team",
    "WAF Bypass Teknikleri",
    "SIEM ve Log Yonetimi",
    "EDR Tespit ve Kacis Yontemleri",
    "Honeypot ve Tuzak Sistemleri",
    "Incident Response Plani",
    "Zero Trust Mimarisi",
    "Container Guvenligi (Docker/K8s)",
    "Cloud Guvenligi (AWS/Azure/GCP)",
    "Guvenli Kodlama - Input Dogrulama",
    "Guvenli Kodlama - Session ve Auth",
    "Guvenli Kodlama - API Tasarimi",
    "Guvenli Kodlama - Dependency Guvenligi",
    "Phishing ve Spear Phishing",
    "Sosyal Muhendislikten Korunma",
    "IoT Cihaz Guvenligi",
    "Active Directory - Kerberos ve NTLM",
    "Pass-the-Hash ve Pass-the-Ticket",
    "AMSI Bypass Teknikleri",
    "ETW (Event Tracing) Bypass",
    "DLL Side-Loading",
    "Python ile Reflective DLL Loading",
]

turn = 1
idx = 0

while True:
    try:
        if os.path.exists(os.path.expanduser("~/.hermes/STOP")):
            os.remove(os.path.expanduser("~/.hermes/STOP"))
            log("DURDURULDU."); break

        konu = KONULAR[idx % len(KONULAR)]
        idx += 1

        t1 = time.time()
        yanit = api(
            f"Sen siber guvenlik uzmanisin. Hermes AI'ya ogret. Tur {turn}.\n"
            f"Konu: {konu}\n\n"
            f"KURALLAR:\n- 5-10 cumle anlat\n- Python kodu ver (```python)\n- Iz birakmamak icin yapilmasi gerekeni soyle\n- Saldiri ve savunmayi birlikte anlat\n\n"
            f"FORMAT:\nKONU: {konu}\nOGRET: [icerik]\nKOD: [python]\nIZ: [iz birakmamak icin]\nTEST: [test yontemi]"
        )
        sure = time.time() - t1

        path, sname = save(konu, yanit, turn)
        yenimi = sname not in mevcut
        mevcut.add(sname)
        toplam = len([f for f in os.listdir(SKILLS_DIR) if f.startswith("guvenlik-")])

        log(f"Süre: {sure:.0f}s | {'YENI' if yenimi else 'TEKRAR'} | Tur {turn} | {konu}")
        log(f"Dosya: {path} | Toplam: {toplam}")

        time.sleep(0.5)
        turn += 1

    except KeyboardInterrupt:
        log("Klavye ile durduruldu."); break
    except Exception as e:
        log(f"HATA tur {turn}: {e}")
        time.sleep(3)
        turn += 1
        continue
