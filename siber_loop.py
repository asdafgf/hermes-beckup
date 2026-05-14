import urllib.request
import json
import os
import re
import time
from datetime import datetime

SKILLS_DIR = os.path.expanduser("~/.hermes/skills")
OUT_FILE = os.path.expanduser("~/ollama_loop_output.txt")
OLLAMA_MODEL = "gemma4:31b"

def log(msg):
    print(msg, flush=True)
    with open(OUT_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
        f.flush()

def talk(prompt):
    data = json.dumps({"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read())["response"]

def cname(text):
    text = re.sub(r'[*_#`\'\"\(\)\[\]\?\!]', '', text)
    text = text.lower()
    for o,n in {'ı':'i','ğ':'g','ü':'u','ş':'s','ö':'o','ç':'c',' ':'-','.':''}.items():
        text = text.replace(o, n)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')[:55]

def save_skill(topic, content, turn):
    clean = cname(topic) or f"ders-{turn}"
    name = f"ollama-guvenlik-{clean}"
    path = os.path.join(SKILLS_DIR, f"{name}.md")
    
    # Extract Python code blocks
    code_blocks = re.findall(r'```python\n(.*?)```', content, re.DOTALL)
    code_section = ""
    if code_blocks:
        code_section = "\n\n## Python Kod Örneği\n\n```python\n" + "\n".join(code_blocks) + "\n```\n"

    md = f"""---
name: {name}
description: "Siber guvenlik - Ollama(gemma4:31b) tarafindan ogretildi (Tur {turn}): {topic}"
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

Siber güvenlik becerisi. Ollama (gemma4:31b) tarafından öğretilmiştir.
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    return path, name

log("=== SIBER GUVENLIK EGITIM DONGUSU BASLADI ===")
log(f"Model: {OLLAMA_MODEL}")
log(f"Kategori: guvenlik (tum skill'ler ollama-guvenlik-* olarak kaydedilecek)")
log(f"Cikti: {OUT_FILE}")
log("")

existing = set(f.replace(".md","") for f in os.listdir(SKILLS_DIR) if f.startswith("ollama-guvenlik-"))
log(f"Mevcut guvenlik skill: {len(existing)}")
log("")

TOPICS_POOL = [
    "Port Tarama ve Servis Tespiti (Nmap ile)",
    "Ag Zafiyet Taramasi (Nessus, OpenVAS)",
    "Web Uygulama Guvenligi - SQL Injection",
    "Web Uygulama Guvenligi - XSS Saldirilari",
    "Web Uygulama Guvenligi - CSRF",
    "Web Uygulama Guvenligi - LFI/RFI",
    "Web Uygulama Guvenligi - SSRF",
    "Sifreler ve Kriptografi - Hash Kirma Teknikleri",
    "Sifreler ve Kriptografi - Simetrik/Asimetrik Sifreleme",
    "Sifreler ve Kriptografi - SSL/TLS ve Sertifikalar",
    "Ag Guvenligi - Firewall Kurallari ve Bypass",
    "Ag Guvenligi - IDS/IPS Atlatma Teknikleri",
    "Ag Guvenligi - VPN ve Tnel Protokolleri",
    "Ag Guvenligi - Wireshark ile Trafik Analizi",
    "Ag Guvenligi - ARP Spoofing ve MITM",
    "Ag Guvenligi - DNS Spoofing ve Zehirlemesi",
    "Windows Guvenligi - AD ve Yetki Yukseltme",
    "Windows Guvenligi - Powershell ile Post-Exploit",
    "Windows Guvenligi - Registry ve GPO Guvenligi",
    "Windows Guvenligi - Process Injection ve API Hooking",
    "Linux Guvenligi - Yetki Yukseltme Teknikleri",
    "Linux Guvenligi - Kernel Exploitlari",
    "Linux Guvenligi - Sistem Loglarindan Kacis",
    "Linux Guvenligi - Cron ve Service Manipulasyonu",
    "Linux Guvenligi - SUID/SGID ve Capabilities",
    "Web Guvenligi - JWT Guvenligi ve Token Manipulasyonu",
    "Web Guvenligi - API Guvenlik Testleri",
    "Web Guvenligi - OWASP Top 10 Derinlemesine",
    "Web Guvenligi - Rate Limiting ve Bypass",
    "Web Guvenligi - File Upload Zafiyetleri",
    "Web Guvenligi - Session Hijacking ve Fixation",
    "Sosyal Muhendislik ve Phishing Teknikleri",
    "Sosyal Muhendislik - Spear Phishing",
    "Sosyal Muhendislik - Pretexting ve Baiting",
    "Sosyal Muhendislik - Tailgating ve Shoulder Surfing",
    "Reverse Engineering - Binary Analizi",
    "Reverse Engineering - Debugging Teknikleri (GDB, x64dbg)",
    "Reverse Engineering - Disassembly ve Decompilation",
    "Reverse Engineering - Packer ve Unpacker",
    "Reverse Engineering - Anti-Debug ve Anti-VM Teknikleri",
    "Reverse Engineering - PE/ELF Dosya Analizi",
    "Reverse Engineering - Malware Analizi (Statik/Dinamik)",
    "Reverse Engineering - Api Hooking ve Detour",
    "Reverse Engineering - Shellcode Analizi",
    "Exploit Gelistirme - Buffer Overflow",
    "Exploit Gelistirme - ROP Zincirleri",
    "Exploit Gelistirme - Heap Exploitation",
    "Exploit Gelistirme - Format String Zafiyetleri",
    "Exploit Gelistirme - Integer Overflow",
    "Exploit Gelistirme - Use-After-Free",
    "Exploit Gelistirme - Race Condition ve TOCTOU",
    "Exploit Gelistirme - Fuzzing Teknikleri",
    "Kablosuz Ag Guvenligi - WPA/WPA2 Kirma",
    "Kablosuz Ag Guvenligi - Evil Twin ve Rogue AP",
    "Kablosuz Ag Guvenligi - WPS ve PIN Saldirilari",
    "Kablosuz Ag Guvenligi - Deauth Saldirilari",
    "Kablosuz Ag Guvenligi - Bluetooth Guvenligi",
    "Python ile Ag Arac Gelistirme - Socket Programlama",
    "Python ile Ag Arac Gelistirme - HTTP Istemci/Sunucu",
    "Python ile Ag Arac Gelistirme - Proxy ve Tnel",
    "Python ile Ag Arac Gelistirme - Port Scanner",
    "Python ile Ag Arac Gelistirme - Paket Yakalama (Scapy)",
    "Python ile Ag Arac Gelistirme - Brute Force Araclari",
    "Python ile Ag Arac Gelistirme - Keylogger",
    "Python ile Ag Arac Gelistirme - Reverse Shell",
    "Python ile Ag Arac Gelistirme - Bind Shell",
    "Python ile Ag Arac Gelistirme - Web Scraper ve Crawler",
    "Python ile Ag Arac Gelistirme - API Entegrasyonlari",
    "Python ile Ag Arac Gelistirme - Payload Olusturma",
    "Python ile Ag Arac Gelistirme - Encoder/Decoder",
    "Python ile Ag Arac Gelistirme - Steganography",
    "Python ile Ag Arac Gelistirme - ZIP/PDF Sifre Kirma",
    "Python ile Ag Arac Gelistirme - Network Monitor",
    "Iz Birakmama (OpSec) - Proxy Zincirleri ve Tor",
    "Iz Birakmama (OpSec) - VPN ve Trafik Sifreleme",
    "Iz Birakmama (OpSec) - Log Silme ve Manipulasyonu",
    "Iz Birakmama (OpSec) - Windows Event Log Temizligi",
    "Iz Birakmama (OpSec) - Linux Log Temizligi (~/.bash_history, syslog)",
    "Iz Birakmama (OpSec) - Timestomping (Dosya Zaman Damgasi)",
    "Iz Birakmama (OpSec) - Anti-Forensics Teknikleri",
    "Iz Birakmama (OpSec) - Memory Forensics'ten Kacis",
    "Iz Birakmama (OpSec) - Disk Sifreleme ve Veri Gizleme",
    "Iz Birakmama (OpSec) - Digital Signature Spoofing",
    "Iz Birakmama (OpSec) - MAC Adres Spoofing",
    "Iz Birakmama (OpSec) - User-Agent ve Parmakizi Manipulasyonu",
    "Iz Birakmama (OpSec) - C2 Haberlesme ve Komuta Merkezleri",
    "Iz Birakmama (OpSec) - DNS-over-HTTPS ve Egres Filtreleme",
    "Iz Birakmama (OpSec) - Tor Hidden Services (.onion)",
    "Iz Birakmama (OpSec) - I2P ve Darknet Aglari",
    "Kali Linux Araclari - Metasploit Framework",
    "Kali Linux Araclari - Burp Suite",
    "Kali Linux Araclari - Hydra ve John the Ripper",
    "Kali Linux Araclari - Aircrack-ng Suite",
    "Kali Linux Araclari - Hashcat ve GPU Kirma",
    "Kali Linux Araclari - sqlmap",
    "Kali Linux Araclari - Nikto ve Dirb",
    "Kali Linux Araclari - Netcat ve Socat",
    "Kali Linux Araclari - Responder ve Impacket",
    "Kali Linux Araclari - BloodHound ve SharpHound",
    "Kali Linux Araclari - Empire ve Covenant",
    "Kali Linux Araclari - Bettercap",
    "Guvenli Kodlama - Input Dogrulama",
    "Guvenli Kodlama - Output Encoding ve Escape",
    "Guvenli Kodlama - Kimlik Dogrulama ve Session Yonetimi",
    "Guvenli Kodlama - Yetkilendirme ve ACL",
    "Guvenli Kodlama - Guvenli Veri Depolama",
    "Guvenli Kodlama - Hata Yonetimi ve Loglama",
    "Guvenli Kodlama - Guvenli Konfigurasyon",
    "Guvenli Kodlama - Guvenli API Tasarimi",
    "Guvenli Kodlama - Dependency ve Supply Chain Guvenligi",
    "Guvenli Kodlama - OWASP ASVS (Application Security Verification Standard)",
    "Saldiri Testi Metodolojisi - Penetration Testing Lifecycle",
    "Saldiri Testi Metodolojisi - Bilgi Toplama (Reconnaissance)",
    "Saldiri Testi Metodolojisi - Zafiyet Analizi",
    "Saldiri Testi Metodolojisi - Exploitasyon",
    "Saldiri Testi Metodolojisi - Post-Exploitasyon",
    "Saldiri Testi Metodolojisi - Raporlama",
    "Saldiri Testi Metodolojisi - Red Team vs Blue Team",
    "Saldiri Testi Metodolojisi - Purple Team Yaklasimi",
    "Savunma Mekanizmalari - WAF ve Web Application Firewall",
    "Savunma Mekanizmalari - SIEM ve Log Yonetimi",
    "Savunma Mekanizmalari - EDR ve XDR Cozumleri",
    "Savunma Mekanizmalari - SOAR ve Otomasyon",
    "Savunma Mekanizmalari - Honeypot ve Tuzak Sistemleri",
    "Savunma Mekanizmalari - Threat Intelligence",
    "Savunma Mekanizmalari - Incident Response Plan",
    "Savunma Mekanizmalari - Disaster Recovery",
    "Savunma Mekanizmalari - Network Segmentation",
    "Savunma Mekanizmalari - Zero Trust Mimarisi",
    "Savunma Mekanizmalari - Endpoint Security",
    "Savunma Mekanizmalari - Application Whitelisting",
    "Savunma Mekanizmalari - Application Sandboxing",
    "Savunma Mekanizmalari - Container Guvenligi (Docker/K8s)",
    "Savunma Mekanizmalari - Cloud Guvenligi (AWS/Azure/GCP)",
    "Savunma Mekanizmalari - IoT Guvenligi",
    "Savunma Mekanizmalari - Mobile App Guvenligi (Android/iOS)",
    "Savunma Mekanizmalari - Database Guvenligi"
]

recent_topics = []
turn = 1
consecutive_fails = 0
pool_index = 0

while True:
    try:
        # Check stop
        if os.path.expanduser("~/.hermes/STOP_SIBER_LOOP") and os.path.exists(os.path.expanduser("~/.hermes/STOP_SIBER_LOOP")):
            os.remove(os.path.expanduser("~/.hermes/STOP_SIBER_LOOP"))
            log("DURDURMA SINYALI ALINDI.")
            break

        # Pick topic from pool
        specific_topic = TOPICS_POOL[pool_index % len(TOPICS_POOL)]
        pool_index += 1
        
        log(f"{'='*65}")
        log(f"TUR {turn}")
        log(f"KONU: {specific_topic}")
        log(f"{'='*65}")

        prompt = (
            f"Sen bir siber guvenlik uzmani ve ogretmen AI'sin. Hermes AI asistanina siber guvenlik ogretiyorsun.\n"
            f"Tur {turn}. Konu: {specific_topic}\n\n"
            f"SU KURALLARA UY:\n"
            f"1. Kisa, oz, anlasilir anlat (5-10 cumle)\n"
            f"2. Pratik Python kodu ekle (```python ile)\n"
            f"3. Geride iz birakmamak icin nelere dikkat edilmeli belirt\n"
            f"4. Saldiri ve savunma yonlerini birlikte anlat\n"
            f"5. Test yontemini de belirt\n\n"
            f"Su formatta cevap ver:\n"
            f"KONU: {specific_topic}\n"
            f"OGRET: [ders icerigi - pratik Python kodu ile birlikte]\n"
            f"TEST: [nasil test edilir]\n"
            f"KORUNMA: [iz birakmamak icin yapilmasi gerekenler]"
        )

        resp = talk(prompt)
        log(f"OLLAMA CEVAP VERDI ({len(resp)} karakter)")
        
        path, sname = save_skill(specific_topic, resp, turn)
        is_new = sname not in existing
        existing.add(sname)
        
        total = len([f for f in os.listdir(SKILLS_DIR) if f.startswith("ollama-guvenlik-")])

        if is_new:
            log(f"✓ YENI SKILL KAYDEDILDI!")
        else:
            log(f"~ SKILL GUNCELLENDI (tekrar)")
        
        log(f"  Konu: {specific_topic}")
        log(f"  Dosya: {path}")
        log(f"  Toplam guvenlik skill: {total}")
        log(f"{'─'*65}")
        log("")

        time.sleep(2)
        turn += 1

    except KeyboardInterrupt:
        log("Klavye ile durduruldu.")
        break
    except Exception as e:
        log(f"HATA (tur {turn}): {e}")
        import traceback
        traceback.print_exc()
        time.sleep(10)
        turn += 1
        continue
