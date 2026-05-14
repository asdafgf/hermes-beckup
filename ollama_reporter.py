import time
import os
import re
from datetime import datetime

SKILLS_DIR = os.path.expanduser("~/.hermes/skills")
LOG_FILE = os.path.expanduser("~/.hermes/logs/ollama-loop-log.txt")
KNOWN_SKILLS_FILE = os.path.expanduser("~/.hermes/logs/ollama-reported-skills.txt")
LAST_MARKER = os.path.expanduser("~/.hermes/logs/ollama-last-total.txt")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def get_ollama_skills():
    files = [f for f in os.listdir(SKILLS_DIR) if f.startswith("ollama-") and f.endswith(".md")]
    return set(files)

def get_new_skills(known):
    current = get_ollama_skills()
    new_skills = current - known
    return new_skills, current

def read_new_log_lines(last_pos):
    if not os.path.exists(LOG_FILE):
        return "", 0
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        f.seek(last_pos)
        new_data = f.read()
        new_pos = f.tell()
    return new_data, new_pos

# Load known skills
known = get_ollama_skills()
reported_file = KNOWN_SKILLS_FILE
reported = set()
if os.path.exists(reported_file):
    with open(reported_file, "r") as f:
        reported = set(line.strip() for line in f if line.strip())

# Track last turn reported
last_turn = 0
last_log_pos = 0
if os.path.exists(LOG_FILE):
    last_log_pos = os.path.getsize(LOG_FILE)

print("HERMES | Canlı rapor başladı — yeni skill'ler anında bildirilecek.")
print("HERMES | Durdurmak için CTRL+C\n")

try:
    while True:
        time.sleep(8)  # Check every 8 seconds
        
        new_skills, known = get_new_skills(known)
        
        # Also check log for new turns
        new_log, last_log_pos = read_new_log_lines(last_log_pos)
        
        if new_skills:
            for skill in new_skills:
                if skill in reported:
                    continue
                
                # Read the skill file for details
                skpath = os.path.join(SKILLS_DIR, skill)
                topic = skill.replace("ollama-", "").replace(".md", "").replace("-", " ").title()
                turn_info = ""
                desc = ""
                cat = ""
                
                try:
                    with open(skpath, "r", encoding="utf-8") as f:
                        content = f.read()
                    # Extract turn number from description
                    m = re.search(r'Tur (\d+)', content)
                    if m:
                        turn_info = f"Tur #{m.group(1)}"
                    # Extract description
                    m2 = re.search(r'description: "([^"]+)"', content)
                    if m2:
                        desc = m2.group(1)
                except:
                    pass
                
                reported.add(skill)
                
                # MARKDOWN FREE - terminal friendly
                print(f"═══════════════════════════════════════════")
                print(f" YENI SKILL KAYDEDILDI! {turn_info}")
                print(f"═══════════════════════════════════════════")
                print(f" Konu: {topic}")
                if desc:
                    print(f" Açıklama: {desc}")
                print(f" Dosya: {skpath}")
                print(f" Toplam ollama-skill: {len(known)}")
                print(f"{'─'*47}")
        
        # Also report progress every ~10 turns from log
        if new_log:
            for line in new_log.split("\n"):
                m = re.search(r'TUR (\d+)', line)
                if m:
                    t = int(m.group(1))
                    if t > last_turn and t % 10 == 0:
                        last_turn = t
                        print(f"  [İlerleme] Tur {t} | Toplam skill: {len(known)}")
                
except KeyboardInterrupt:
    print("\n\nHERMES | Canlı rapor durduruldu. Döngü arka planda devam ediyor.")
