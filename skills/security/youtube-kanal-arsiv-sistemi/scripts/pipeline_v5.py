#!/usr/bin/env python3
"""
OTOMATIK SKILL URETICI v5
Her yeni transcript icin sirayla dener:
1. Gemini API
2. OpenRouter (GPT-4o-mini)
3. Ollama qwen2.5-coder (sinirsiz, yerel)
4. Ollama gemma4:latest (alternatif)
5. Fallback (transcript ozeti)
Asla kullaniciya sormaz. Otomatik kaydeder.
Calisma: Her 15 dk'da bir cronjob ile tetiklenir.
"""

import os, re, glob, json, time, sys, subprocess, requests
from datetime import datetime

SKILLS_BASE = r"C:\Users\eymen\AppData\Local\hermes\skills"
PROCESSED_FILE = r"C:\Users\eymen\Desktop\transcript_processed_ids_v4.txt"
LOG_FILE = r"C:\Users\eymen\Desktop\transcript_skills\otomatik_log.txt"
BASE_DIR = r"C:\Users\eymen\Desktop"

def get_api_key(name):
    v = os.environ.get(name, "")
    if v: return v
    try:
        r = subprocess.run(["powershell.exe", "-Command",
            f"[System.Environment]::GetEnvironmentVariable('{name}','User')"],
            capture_output=True, text=True, timeout=5)
        v = r.stdout.strip()
        if v: os.environ[name] = v
        return v
    except: return ""

GOOGLE_API_KEY = get_api_key("GOOGLE_API_KEY")
OPENROUTER_API_KEY = get_api_key("OPENROUTER_API_KEY")

def log(msg):
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{t}] {msg}")
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{t}] {msg}\n")

processed = set()
if os.path.exists(PROCESSED_FILE):
    with open(PROCESSED_FILE) as f:
        processed = set(line.strip() for line in f if line.strip())

KANALLAR = {
    'john-hammond': os.path.join(BASE_DIR, 'rootofthenull_arsiv', 'transcriptler'),
    'networkchuck': os.path.join(BASE_DIR, 'networkchuck_arsiv', 'transcriptler'),
    'david-bombal': os.path.join(BASE_DIR, 'davidbombal_arsiv', 'transcriptler'),
}

def extract_text(srt_path):
    try:
        with open(srt_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        lines = content.split('\n')
        text = [l.strip() for l in lines if l.strip()
                and not re.match(r'^\d+$', l)
                and not re.match(r'^\d{2}:\d{2}:\d{2}', l)]
        result = ' '.join(text)
        result = re.sub(r'(\b\w+\b)( \1\b){2,}', r'\1', result)
        return result[:12000]
    except: return ""

def extract_name(content):
    m = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
    if m:
        n = m.group(1).strip().strip('"\'')
        n = re.sub(r'[^a-z0-9-]', '', n.lower())
        if n and len(n) >= 3: return n
    return None

def save_skill(content, video_id, kanal, source):
    name = extract_name(content) or f"{kanal}-{video_id[:8]}"
    sdir = os.path.join(SKILLS_BASE, "security", name)
    os.makedirs(sdir, exist_ok=True)
    with open(os.path.join(sdir, "SKILL.md"), 'w', encoding='utf-8') as f:
        f.write(content)
    bdir = os.path.join(BASE_DIR, "transcript_skills", "kaydedilen")
    os.makedirs(bdir, exist_ok=True)
    with open(os.path.join(bdir, f"{name}.md"), 'w', encoding='utf-8') as f:
        f.write(content)
    return name

def ask_gemini(text, vid_id, kanal):
    if not GOOGLE_API_KEY: return None
    prompt = f"""Create a Hermes Agent SKILL.md file from this transcript.
Video: https://youtu.be/{vid_id} Channel: {kanal}
name=short kebab-case, description=one sentence, body=step-by-step, category=security
SKILL.md only:
{text[:10000]}"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"
    for a in range(3):
        try:
            r = requests.post(url, json={"contents":[{"parts":[{"text":prompt}]}],
                "generationConfig":{"maxOutputTokens":2000,"temperature":0.3}}, timeout=60)
            if r.status_code == 200:
                t = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                return re.sub(r'^```(yaml)?\n?|\n?```$', '', t)
            if r.status_code == 429:
                log(f" Gemini kota, {10*(a+1)}s bekle")
                time.sleep(10*(a+1))
            else: return None
        except: time.sleep(5)
    return None

def ask_openrouter(text, vid_id, kanal):
    if not OPENROUTER_API_KEY: return None
    prompt = f"""Create a Hermes Agent SKILL.md from this cybersecurity video.
Video: https://youtu.be/{vid_id} Channel: {kanal}
name=kebab-case, description=summary, body=guide, category=security
SKILL.md only:
{text[:10000]}"""
    for a in range(3):
        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization":f"Bearer {OPENROUTER_API_KEY}","Content-Type":"application/json"},
                json={"model":"openai/gpt-4o-mini","messages":[{"role":"user","content":prompt}],"max_tokens":2000}, timeout=90)
            if r.status_code == 200:
                t = r.json()["choices"][0]["message"]["content"]
                return re.sub(r'^```(yaml)?\n?|\n?```$', '', t)
            if r.status_code == 429: time.sleep(15)
            else: return None
        except: time.sleep(5)
    return None

def ask_ollama(text, vid_id, kanal, model="qwen2.5-coder:7b"):
    """Ollama - sinirsiz, ucretsiz, yerel."""
    prompt = f"""Create a Hermes Agent SKILL.md from this transcript.
name: short kebab-case, description: one sentence, body: step-by-step, category: security
Video: https://youtu.be/{vid_id} Channel: {kanal}
SKILL.md only:
{text[:10000]}"""
    payload = json.dumps({"model":model,"prompt":prompt,"stream":False,
        "options":{"num_predict":2000,"temperature":0.3}})
    for a in range(2):
        try:
            r = requests.post("http://localhost:11434/api/generate", data=payload,
                headers={"Content-Type":"application/json"}, timeout=180)
            if r.status_code == 200:
                t = r.json().get("response","")
                if len(t) > 50:
                    return re.sub(r'^```(yaml)?\n?|\n?```$', '', t)
        except requests.exceptions.Timeout: log(" Ollama timeout, retry...")
        except Exception as e:
            if "Connection refused" in str(e):
                log(" Ollama restart...")
                subprocess.run(["taskkill","//F","//IM","ollama.exe"], capture_output=True, timeout=5)
                time.sleep(3)
                subprocess.Popen(["ollama","serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(5)
        time.sleep(3)
    return None

def fallback(title, text, vid_id, kanal):
    words = title.lower().split()[:8]
    name = '-'.join([re.sub(r'[^a-z0-9]','',w) for w in words if len(w)>2])[:60]
    kw = [w for w in ['hack','malware','phish','exploit','windows','linux','python',
        'network','cloud','ai','android','root','ctf','password']
          if w in text[:3000].lower()] or ['siber-guvenlik']
    return f"""---
name: {name}
description: "{title[:100]}"
version: 1.0
category: security
source: "https://youtu.be/{vid_id}"
tags: [{', '.join(kw[:6])}, {kanal}]
---

# {title}

**Kaynak:** [YouTube](https://youtu.be/{vid_id}) | **Kanal:** {kanal}

---

## Transcript Ozeti

{text[:2000]}

---

## Anahtar Kelimeler
{', '.join(kw)}

---
"""

# === ANA DONGU ===
log("=" * 50)
log(f"API: Gemini={'OK' if GOOGLE_API_KEY else 'YOK'} OpenRouter={'OK' if OPENROUTER_API_KEY else 'YOK'} Ollama=HAZIR")
log(f"Onceden islenen: {len(processed)} video")

islenen = 0
for kanal, trans_dir in KANALLAR.items():
    if not os.path.exists(trans_dir): continue
    srts = sorted(glob.glob(os.path.join(trans_dir, '*.srt')), key=os.path.getsize, reverse=True)
    for srt_path in srts:
        vid_id = os.path.basename(srt_path).split('.')[0]
        if vid_id in processed: continue
        log(f"\n{kanal}/{vid_id}")
        text = extract_text(srt_path)
        if len(text) < 100: processed.add(vid_id); continue
        title = text.split('.')[0].strip()[:80]
        source, content = "fallback", None
        if GOOGLE_API_KEY:
            r = ask_gemini(text, vid_id, kanal)
            if r: content, source = r, "gemini"
        if not content and OPENROUTER_API_KEY:
            r = ask_openrouter(text, vid_id, kanal)
            if r: content, source = r, "openrouter"
        if not content:
            r = ask_ollama(text, vid_id, kanal, "qwen2.5-coder:7b")
            if r: content, source = r, "ollama-qwen"
        if not content:
            r = ask_ollama(text, vid_id, kanal, "gemma4:latest")
            if r: content, source = r, "ollama-gemma4"
        if not content: content = fallback(title, text, vid_id, kanal)
        name = save_skill(content, vid_id, kanal, source)
        processed.add(vid_id)
        with open(PROCESSED_FILE, 'a') as f: f.write(f"{vid_id}\n")
        log(f"[{source}] {name}")
        islenen += 1
        time.sleep(2)

log(f"\nBatch: {islenen} yeni skill | Toplam: {len(processed)} video")
