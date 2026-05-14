import urllib.request
import json
import os
import re
import time
from datetime import datetime

HERMES_SKILLS_DIR = os.path.expanduser("~/.hermes/skills")
LOG_FILE = os.path.expanduser("~/.hermes/logs/ollama-loop-log.txt")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
OLLAMA_MODEL = "gemma3:4b"

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def talk_to_ollama(prompt):
    data = json.dumps({"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read())["response"]

def clean_name(text):
    text = re.sub(r'[*_#`:]', '', text)
    text = text.lower()
    for old, new in {'ı':'i','ğ':'g','ü':'u','ş':'s','ö':'o','ç':'c'}.items():
        text = text.replace(old, new)
    text = re.sub(r'[^a-z0-9-]', '-', text.strip())
    text = re.sub(r'-+', '-', text)
    return text.strip('-')[:50]

def save_skill(topic, content, turn_num):
    clean = clean_name(topic)
    if not clean: clean = f"ders-{turn_num}"
    name = f"ollama-{clean}"
    skpath = os.path.join(HERMES_SKILLS_DIR, f"{name}.md")
    skill_md = f"""---
name: {name}
description: "Ollama tarafından öğretildi (Tur {turn_num}): {topic}"
created_by: agent
turn: {turn_num}
created_at: {datetime.now().isoformat()}
---

# {topic}

**Ollama'nın öğrettiği bilgi (Tur {turn_num}):**

{content}

---

## Kullanım

Bu skill, Ollama'nın Hermes'e öğrettiği bir konuyu içerir.
"""
    with open(skpath, "w", encoding="utf-8") as f:
        f.write(skill_md)
    return skpath, name, topic

def get_existing():
    return set(f.replace(".md","") for f in os.listdir(HERMES_SKILLS_DIR) if f.startswith("ollama-") and f.endswith(".md"))

log("=== OLLAMA-HERMES EGITIM DONGUSU (RAPORLU) BASLADI ===")
existing = get_existing()
consecutive_fails = 0
turn = 67  # kaldigin yerden devam

# Bir onceki turdan kalan konulari hatirlama
recent_topics = []

while True:
    try:
        stop_file = os.path.expanduser("~/.hermes/STOP_OLLAMA_LOOP")
        if os.path.exists(stop_file):
            os.remove(stop_file)
            log("Durduruldu.")
            break

        hint = ""
        if recent_topics:
            hint = f"Son konular: {', '.join(recent_topics[-3:])}. BUNLARI TEKRAR ETME! Tamamen farkli bir konu sec."

        prompt = (
            f"Sen bir ogretmen AI'sin. Hermes AI asistanini egitiyorsun. Tur {turn}. "
            f"{hint}"
            f"Kisa, oz bir ders ver (3-5 cumle). KARMASIK TERIMLER KULLANMA. "
            f"Sadece su formatta cevap ver:\n"
            f"KONU: [konu basligi - 2-5 kelime]\n"
            f"DERS: [3-5 cumle]\n"
            f"KATEGORI: [programlama|sistem|veri|guvenlik|ai|donanim|ag|genel]"
        )
        
        resp = talk_to_ollama(prompt)
        topic = ""
        for line in resp.split("\n"):
            if line.startswith("KONU:"):
                topic = re.sub(r'[*#]', '', line.replace("KONU:", "")).strip()
                break
        if not topic:
            topic = resp.strip().split("\n")[0][:50]

        skpath, skill_name, safe_topic = save_skill(topic, resp, turn)
        is_new = skill_name not in existing
        existing.add(skill_name)

        if is_new:
            recent_topics.append(topic)
            if len(recent_topics) > 5: recent_topics.pop(0)
            consecutive_fails = 0
            log(f"*** YENI SKILL | Tur #{turn} | {topic} | {skpath}")
        else:
            log(f"[TEKRAR] Tur #{turn} | {topic}")
            consecutive_fails += 1

        if consecutive_fails >= 5:
            log("Cok tekrar, konu havuzu sifirlaniyor...")
            recent_topics = []
            consecutive_fails = 0

        time.sleep(1.5)
        turn += 1

    except KeyboardInterrupt:
        log("DURDURULDU")
        break
    except Exception as e:
        log(f"HATA: {e}")
        time.sleep(5)
        consecutive_fails += 1
        turn += 1
        continue
