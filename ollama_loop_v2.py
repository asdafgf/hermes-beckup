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
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
        f.flush()

def talk_to_ollama(prompt):
    data = json.dumps({"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read())["response"]

def clean_name(text):
    text = re.sub(r'[*_#`:]', '', text)
    text = text.lower()
    for old, new in {'ı':'i','ğ':'g','ü':'u','ş':'s','ö':'o','ç':'c','(':'-',')':'','[':'',']':'','?':'','!':''}.items():
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

log("=== OLLAMA-HERMES DONGUSU BASLADI (v2) ===")
existing = get_existing()
log(f"Mevcut ollama skill: {len(existing)}")
recent_topics = []
turn = 1
consecutive_fails = 0

while True:
    try:
        # Check stop marker
        stop_file = os.path.expanduser("~/.hermes/STOP_OLLAMA_LOOP")
        if os.path.exists(stop_file):
            os.remove(stop_file)
            log("STOP sinyali alindi. Duruyorum.")
            break

        hint = ""
        if recent_topics:
            hint = f"Son 3 konu: {', '.join(recent_topics[-3:])}. Bunlari KESINLIKLE TEKRAR ETME! Tamamen farkli bir konu ver."

        prompt = (
            f"Sen bir ogretmen AI'sin. Hermes adinda bir AI'yi egitiyorsun. Tur {turn}. "
            f"{hint}"
            f"Kisa, oz, anlasilir bir ders (3-5 cumle). Basit anlat. "
            f"Tek bir formatta cevap ver:\n"
            f"KONU: [baslik - 2-5 kelime]\n"
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
            lines = [l.strip() for l in resp.split("\n") if l.strip() and not l.startswith("DERS:") and not l.startswith("KATEGORI")]
            topic = lines[0][:60] if lines else f"Ders-{turn}"

        skpath, skill_name, stopic = save_skill(topic, resp, turn)
        is_new = skill_name not in existing
        existing.add(skill_name)

        total_skills = len([f for f in os.listdir(HERMES_SKILLS_DIR) if f.startswith("ollama-")])
        
        if is_new:
            recent_topics.append(topic)
            if len(recent_topics) > 5:
                recent_topics.pop(0)
            consecutive_fails = 0
            log(f"*** YENI SKILL | Tur #{turn} | {topic} | Toplam: {total_skills}")
        else:
            log(f"[TEKRAR] Tur #{turn} | {topic}")
            consecutive_fails += 1

        if consecutive_fails >= 6:
            log("Cok tekrar - konu listesi sifirlaniyor ve prompt sertlesiyor.")
            recent_topics = []
            consecutive_fails = 0

        time.sleep(1.5)
        turn += 1

    except KeyboardInterrupt:
        log("Klavye ile durduruldu.")
        break
    except urllib.error.URLError as e:
        log(f"Ollama baglanti hatasi: {e}. 10sn bekle...")
        time.sleep(10)
        continue
    except Exception as e:
        log(f"BEKLENMEYEN HATA: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(5)
        turn += 1
        continue

log(f"=== DONGU SONU ===")
log(f"Toplam tur: {turn-1}")
total = len([f for f in os.listdir(HERMES_SKILLS_DIR) if f.startswith("ollama-")])
log(f"Toplam ollama skill: {total}")
