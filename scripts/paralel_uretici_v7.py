#!/usr/bin/env python3
"""
PARALEL SKILL ÜRETİCİ v7 - SÜPER HIZLI (FIXED: timeouts, batch scheduling)
Aynı anda 3 video işler, 3 farklı API kullanır
Sırayla dene: Gemini, OpenRouter GPT-4o-mini, Ollama qwen2.5-coder
"""
import os, re, glob, json, time, sys, subprocess, requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

SKILLS_BASE = r"C:\Users\eymen\AppData\Local\hermes\skills"
PROCESSED_FILE = r"C:\Users\eymen\Desktop\transcript_processed_ids_v5.txt"
LOG_FILE = r"C:\Users\eymen\Desktop\transcript_skills\paralel_log.txt"
BASE_DIR = r"C:\Users\eymen\Desktop"
CACHE_FILE = r"C:\Users\eymen\Desktop\transcript_skills\skill_cache.json"
MAX_WORKERS = 3

lock = Lock()

def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    print(f"[{t}] {msg}")
    with lock:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{t}] {msg}\n")

def get_api_key(name):
    v = os.environ.get(name, "")
    if v: return v
    try:
        r = subprocess.run(["powershell.exe","-Command",f"[System.Environment]::GetEnvironmentVariable('{name}','User')"],
                          capture_output=True, text=True, timeout=5)
        v = r.stdout.strip()
        if v: os.environ[name] = v
        return v
    except: return ""

GOOGLE_API_KEY = get_api_key("GOOGLE_API_KEY")
OPENROUTER_API_KEY = get_api_key("OPENROUTER_API_KEY")

# Cache
cache = {}
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, encoding='utf-8') as f: cache = json.load(f)
    except: cache = {}

def save_cache():
    with lock:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(dict(cache), f, ensure_ascii=False, indent=2)

def extract_text(srt_path):
    try:
        with open(srt_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        lines = content.split('\n')
        text = [l.strip() for l in lines if l.strip() and not re.match(r'^\d+$',l) and not re.match(r'^\d{2}:\d{2}:\d{2}',l)]
        result = ' '.join(text)
        result = re.sub(r'(\b\w+\b)( \1\b){2,}', r'\1', result)
        return result[:12000]
    except Exception as e:
        return ""

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

def process_one_video(video_info):
    """Single video processing - run in parallel"""
    vid_id, srt_path, kanal = video_info
    result = {"vid_id": vid_id, "success": False, "name": "", "source": ""}
    
    log(f"  🔄 [{kanal}] {vid_id} başladı")
    text = extract_text(srt_path)
    if len(text) < 100:
        log(f"  ⚠️ {vid_id} çok kısa ({len(text)} chars)")
        return result
    
    # Cache check
    cache_key = f"{kanal}:{vid_id}"
    if cache_key in cache:
        content = cache[cache_key]
        name = save_skill(content, vid_id, kanal, "cached")
        log(f"  ✅ [{kanal}] {vid_id} → {name} (önbellek)")
        return {"vid_id": vid_id, "success": True, "name": name, "source": "cached"}
    
    content = None; source = "fallback"
    
    # 1. Gemini
    if GOOGLE_API_KEY and not content:
        try:
            prompt = f"Create Hermes Agent SKILL.md from this cybersecurity video transcript. Format: YAML frontmatter with 'name' (short kebab-case), 'description' (summary), 'version: 1.0', 'category: security', 'source: https://youtu.be/{vid_id}', 'tags: [relevant-words]'. Then body content with step-by-step guide.\n\nTranscript:\n{text[:10000]}"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"
            r = requests.post(url,
                json={"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"maxOutputTokens":2000,"temperature":0.3}},
                timeout=45)
            if r.status_code == 200:
                t = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                t = re.sub(r'^```(yaml)?\n?|\n?```$', '', t)
                if len(t) > 100: content, source = t, "gemini"
        except Exception as e:
            log(f"  ⚠️ Gemini {vid_id}: {str(e)[:60]}")
    
    # 2. OpenRouter
    if not content and OPENROUTER_API_KEY:
        try:
            prompt2 = f"Create Hermes Agent SKILL.md from this cybersecurity video transcript. Format: YAML frontmatter with 'name' (short kebab-case), 'description' (1-2 lines), 'version: 1.0', 'category: security', 'source: https://youtu.be/{vid_id}', 'tags: [relevant-words]'. Then body with step-by-step guide.\n\nTranscript:\n{text[:10000]}"
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization":f"Bearer {OPENROUTER_API_KEY}","Content-Type":"application/json"},
                json={"model":"openai/gpt-4o-mini","messages":[{"role":"user","content":prompt2}],"max_tokens":2000},
                timeout=60)
            if r.status_code == 200:
                t = r.json()["choices"][0]["message"]["content"]
                t = re.sub(r'^```(yaml)?\n?|\n?```$', '', t)
                if len(t) > 100: content, source = t, "openrouter"
        except Exception as e:
            log(f"  ⚠️ OpenRouter {vid_id}: {str(e)[:60]}")
    
    # 3. Ollama
    if not content:
        try:
            prompt3 = f"Create Hermes Agent SKILL.md from this cybersecurity transcript. YAML frontmatter with name=kebab-case, description, version=1.0, category=security, source=https://youtu.be/{vid_id}, tags=[relevant]. Body=guide.\n\nTranscript:\n{text[:10000]}"
            payload = json.dumps({"model":"qwen2.5-coder:7b","prompt":prompt3,"stream":False,"options":{"num_predict":2000,"temperature":0.3}})
            r = requests.post("http://localhost:11434/api/generate", data=payload, headers={"Content-Type":"application/json"}, timeout=90)
            if r.status_code == 200:
                t = r.json().get("response","")
                if len(t) > 100:
                    t = re.sub(r'^```(yaml)?\n?|\n?```$', '', t)
                    content, source = t, "ollama"
        except Exception as e:
            log(f"  ⚠️ Ollama {vid_id}: {str(e)[:60]}")
    
    # Fallback (AI-generated summary)
    if not content:
        title = text.split('.')[0].strip()[:80]
        words = title.lower().split()[:8]
        name = '-'.join([re.sub(r'[^a-z0-9]','',w) for w in words if len(w)>2])[:60]
        kw = [w for w in ['hack','malware','phish','exploit','windows','linux','python','network','cloud','ai','android','root','ctf','password','security','docker','ransomware','powershell'] if w in text[:3000].lower()] or ['siber-guvenlik']
        content = f"""---
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

## 📝 Transcript Özeti

{text[:2000]}

---

## 🔑 Anahtar Kelimeler
{', '.join(kw)}

---

"""
    
    # Save & cache
    name = save_skill(content, vid_id, kanal, source)
    cache[cache_key] = content
    save_cache()
    
    log(f"  ✅ [{source}] {vid_id} → {name}")
    return {"vid_id": vid_id, "success": True, "name": name, "source": source}


# === MAIN LOOP ===
log("=" * 50)
log("PARALEL SKILL ÜRETİCİ v7 BAŞLADI")
log(f"API: Gemini={'✅' if GOOGLE_API_KEY else '❌'} OpenRouter={'✅' if OPENROUTER_API_KEY else '❌'} Ollama=✅")
log(f"⚠️ Aynı anda {MAX_WORKERS} video işlenecek!")
log(f"Önbellek: {len(cache)} kayıt")

# Processed IDs
processed = set()
if os.path.exists(PROCESSED_FILE):
    with open(PROCESSED_FILE) as f:
        processed = set(line.strip() for line in f if line.strip())

# Collect unprocessed videos
pending = []
KANALLAR = {
    'john-hammond': os.path.join(BASE_DIR, 'rootofthenull_arsiv', 'transcriptler'),
    'networkchuck': os.path.join(BASE_DIR, 'networkchuck_arsiv', 'transcriptler'),
    'david-bombal': os.path.join(BASE_DIR, 'davidbombal_arsiv', 'transcriptler'),
}

for kanal, trans_dir in KANALLAR.items():
    if not os.path.exists(trans_dir): continue
    for srt_path in sorted(glob.glob(os.path.join(trans_dir, '*.srt')), key=os.path.getsize, reverse=True):
        base = os.path.basename(srt_path)
        if base.endswith('.en.srt'):
            vid_id = base[:-7]
        elif base.endswith('.srt'):
            vid_id = base[:-4]
        else:
            continue
        if vid_id not in processed:
            pending.append((vid_id, srt_path, kanal))

log(f"📹 Bekleyen video: {len(pending)}")
log(f"🧠 Önbellekte: {len(cache)}")

# Process in parallel batches
baslangic = time.time()
success_count = 0
fallback_count = 0
gemini_count = 0
openrouter_count = 0
ollama_count = 0
cache_count = 0

for batch_start in range(0, min(len(pending), 120), MAX_WORKERS):  # Max 120 videos per run
    batch = pending[batch_start:batch_start + MAX_WORKERS]
    
    log(f"\n📦 Batch {batch_start//MAX_WORKERS + 1}/{(min(len(pending),120)-1)//MAX_WORKERS + 1}")
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_one_video, v): v for v in batch}
        for future in as_completed(futures):
            r = future.result()
            vid_id = r["vid_id"]
            processed.add(vid_id)
            with open(PROCESSED_FILE, 'a') as f:
                f.write(f"{vid_id}\n")
            if r["success"]:
                success_count += 1
                src = r["source"]
                if src == "gemini": gemini_count += 1
                elif src == "openrouter": openrouter_count += 1
                elif src == "ollama": ollama_count += 1
                elif src == "cached": cache_count += 1
                else: fallback_count += 1
    
    # Brief pause between batches
    time.sleep(1)

gecen = time.time() - baslangic
videos_processed = min(len(pending), 120)
rate = videos_processed / gecen * 60 if gecen > 0 else 0
log(f"\n📊 TAMAM: {videos_processed} video işlendi, {gecen:.0f}s, {rate:.1f} video/dk")
log(f"   Kaynaklar: Gemini={gemini_count} OpenRouter={openrouter_count} Ollama={ollama_count} Önbellek={cache_count} Fallback={fallback_count}")
log(f"🧠 Önbellek: {len(cache)} kayıt")
log(f"📹 Kalan: {len(pending) - videos_processed}")
log("=" * 50)
