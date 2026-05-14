#!/usr/bin/env python3
"""
SÜPER YÖNETİCİ v1.1 — 5 DAKİKADA BİR ÇALIŞIR
HEDEF: 120s cronjob limitine sığ. 90-110s içinde bitir.
  1. Transcript çekme (yt-dlp ile — max 1 kanal, 5 video)
  2. Skill üretme (paralel, 3 thread — max 3 video, her API 10s timeout)
  3. Klasör temizliği (anlamsız skill'leri sil)
  4. Rapor hazırlama

Her şey otomatik, kullanıcıya sormaz.
"""

import os, re, glob, json, time, subprocess, requests, shutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# === YAPILANDIRMA ===
HOME = r"C:\Users\eymen"
DESKTOP = os.path.join(HOME, "Desktop")
SKILLS_BASE = os.path.join(HOME, "AppData", "Local", "hermes", "skills")
SCRIPTS_DIR = os.path.join(HOME, "AppData", "Local", "hermes", "scripts")
YTDLP = os.path.join(HOME, "temp-watch-youtube", "Watch_Youtube_Skill", ".venv", "Scripts", "yt-dlp")
LOG_DIR = os.path.join(DESKTOP, "super_yonetici_loglari")
CACHE_FILE = os.path.join(DESKTOP, "transcript_skills", "skill_cache.json")
PROCESSED_V5 = os.path.join(DESKTOP, "transcript_processed_ids_v5.txt")
PENDING_FILE = os.path.join(DESKTOP, "transcript_pending.txt")

# HEDEF: 120s limiti. Her şey buna sığmalı.
# Transcript: ~20-40s/kanal (5 video)
# Skill: ~30-45s (3 video paralel, her API 10s timeout)
# Temizlik: <5s
# Payda: ~55-90s
YTDLP_TIMEOUT = 60       # yt-dlp max 60s
API_TIMEOUT = 10         # her API çağrısı max 10s
MAX_TRANSCRIPT_PER_KANAL = 5  # max 5 video/kanal/run
MAX_VIDEO_PER_RUN = 3         # max 3 video skill üretimi/run

os.makedirs(LOG_DIR, exist_ok=True)
lock = Lock()

# === KANAL YAPILANDIRMASI ===
KANALLAR = {
    'john-hammond': {
        'url': 'https://www.youtube.com/@_JohnHammond/videos',
        'arsiv': os.path.join(DESKTOP, 'rootofthenull_arsiv', 'transcriptler'),
        'toplam': 1602
    },
    'networkchuck': {
        'url': 'https://www.youtube.com/@NetworkChuck/videos',
        'arsiv': os.path.join(DESKTOP, 'networkchuck_arsiv', 'transcriptler'),
        'toplam': 372
    },
    'david-bombal': {
        'url': 'https://www.youtube.com/@DavidBombal/videos',
        'arsiv': os.path.join(DESKTOP, 'davidbombal_arsiv', 'transcriptler'),
        'toplam': 1483
    }
}

# === LOGLAMA ===
def log(msg, dosya="ana"):
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{t}] {msg}"
    print(line)
    with lock:
        log_path = os.path.join(LOG_DIR, f"{dosya}.log")
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(line + "\n")

# === API KEY AL ===
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

GOOGLE_KEY = get_api_key("GOOGLE_API_KEY")
OPENROUTER_KEY = get_api_key("OPENROUTER_API_KEY")

# ============================================================
# GÖREV 1: TRANSCRIPT ÇEKME — MAX 1 KANAL, 5 VİDEO
# ============================================================
def gorev_transcript_cek():
    """En çok ihtiyacı olan 1 kanaldan 5 video çek. 60s içinde biter."""
    log("📥 Transcript çekme başladı...", "transcript")
    islenen = 0

    # En düşük yüzdelik kanalı bul
    en_kotu = None
    en_kotu_yuzde = 100
    for kanal, bilgi in KANALLAR.items():
        arsiv = bilgi['arsiv']
        mevcut = len(glob.glob(os.path.join(arsiv, '*.srt'))) if os.path.exists(arsiv) else 0
        hedef = bilgi['toplam']
        yuzde = mevcut * 100 // hedef if hedef else 0
        
        if mevcut < hedef and yuzde < en_kotu_yuzde:
            en_kotu = kanal
            en_kotu_yuzde = yuzde
            en_kotu_mevcut = mevcut

    if en_kotu is None:
        log("   ✅ Tüm kanallar tam", "transcript")
        return 0

    bilgi = KANALLAR[en_kotu]
    arsiv = bilgi['arsiv']
    mevcut = en_kotu_mevcut
    hedef = bilgi['toplam']
    kalan = hedef - mevcut
    cekilecek = min(MAX_TRANSCRIPT_PER_KANAL, kalan)

    log(f"   ⏳ {en_kotu}: {mevcut}/{hedef} ({en_kotu_yuzde}%) — +{cekilecek} video", "transcript")

    # John-Hammond %27 tıkanıklığı fix: her 15 turda bir --dateafter ile eski videolara zorla
    extra_args = []
    if en_kotu == 'john-hammond':
        if not hasattr(gorev_transcript_cek, 'jh_tur'):
            gorev_transcript_cek.jh_tur = 0
        gorev_transcript_cek.jh_tur += 1
        if gorev_transcript_cek.jh_tur % 15 == 0:
            extra_args = ["--dateafter", "20200101"]
            log(f"   🔄 {en_kotu}: --dateafter 20200101 ile eski videolara zorla", "transcript")

    try:
        cmd = [
            YTDLP, "--write-auto-sub", "--sub-lang", "en", 
            "--skip-download", "--convert-subs", "srt",
            "-o", os.path.join(arsiv, "%(id)s"),
            "--playlist-start", str(mevcut + 1),
            "--playlist-end", str(mevcut + cekilecek),
            "--sleep-requests", "1.5", "--min-sleep-interval", "2",
            "--max-sleep-interval", "4",
        ] + extra_args + [bilgi['url']]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=YTDLP_TIMEOUT)

        yeni = len(glob.glob(os.path.join(arsiv, '*.srt'))) - mevcut
        log(f"   ✅ {en_kotu}: +{yeni} yeni transcript", "transcript")
        islenen = yeni
    except subprocess.TimeoutExpired:
        log(f"   ⚠️ {en_kotu} timeout ({YTDLP_TIMEOUT}s)", "transcript")
    except Exception as e:
        log(f"   ❌ {en_kotu} hata: {str(e)[:80]}", "transcript")

    log(f"📥 Transcript: {islenen} yeni", "transcript")
    return islenen

# ============================================================
# GÖREV 2: SKILL ÜRETME (PARALEL) — MAX 3 VİDEO
# ============================================================
def extract_text(srt_path):
    try:
        with open(srt_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        # Hem .srt hem .vtt formatını destekle
        lines = content.split('\n')
        text = [l.strip() for l in lines if l.strip() and not re.match(r'^\d+$',l) and not re.match(r'^\d{2}:\d{2}:\d{2}',l) and not re.match(r'^WEBVTT',l) and not l.strip().startswith('NOTE') and not '-->' in l]
        result = ' '.join(text)
        result = re.sub(r'(\b\w+\b)( \1\b){2,}', r'\1', result)
        return result[:12000]
    except: return ""

def extract_name(content):
    m = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
    if m:
        n = m.group(1).strip().strip("\"'")
        n = re.sub(r'[^a-z0-9-]', '', n.lower())
        if n and len(n) >= 3: return n
    return None

def save_skill(content, video_id, kanal, source):
    name = extract_name(content) or f"{kanal}-{video_id[:8]}"
    sdir = os.path.join(SKILLS_BASE, "security", name)
    os.makedirs(sdir, exist_ok=True)
    with open(os.path.join(sdir, "SKILL.md"), 'w', encoding='utf-8') as f:
        f.write(content)
    return name

def process_one_video(vid_id, srt_path, kanal, cache):
    """Tek videoyu işle - paralel thread'de çalışır. Her API 10s timeout."""
    cache_key = f"{kanal}:{vid_id}"
    if cache_key in cache:
        return {"vid_id": vid_id, "status": "cached", "name": cache.get(cache_key, {}).get("name", "")}
    
    text = extract_text(srt_path)
    if len(text) < 100:
        return {"vid_id": vid_id, "status": "short"}
    
    content = None; source = "fallback"
    
    # 1. Gemini (10s timeout)
    if GOOGLE_KEY:
        try:
            prompt = f"Create Hermes Agent SKILL.md from this transcript. name=short kebab-case, description=summary, body=step-by-step, category=security\nVideo: {vid_id}\n{text[:10000]}"
            r = requests.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GOOGLE_KEY,
                json={"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"maxOutputTokens":2000,"temperature":0.3}}, timeout=API_TIMEOUT)
            if r.status_code == 200:
                t = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                t = re.sub(r'^```(yaml)?\n?|\n?```$', '', t)
                if len(t) > 50: content, source = t, "gemini"
        except: pass
    
    # 2. OpenRouter (10s timeout)
    if not content and OPENROUTER_KEY:
        try:
            prompt2 = f"Create SKILL.md for Hermes Agent. name=kebab-case, description, body=guide, category=security\nVideo: {vid_id}\n{text[:10000]}"
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization":f"Bearer {OPENROUTER_KEY}","Content-Type":"application/json"},
                json={"model":"openai/gpt-4o-mini","messages":[{"role":"user","content":prompt2}],"max_tokens":2000}, timeout=API_TIMEOUT)
            if r.status_code == 200:
                t = r.json()["choices"][0]["message"]["content"]
                t = re.sub(r'^```(yaml)?\n?|\n?```$', '', t)
                if len(t) > 50: content, source = t, "openrouter"
        except: pass
    
    # 3. Ollama (10s timeout)
    if not content:
        try:
            prompt3 = f"Create SKILL.md. name=kebab-case. Video: {vid_id}\n{text[:10000]}"
            payload = json.dumps({"model":"qwen2.5-coder:7b","prompt":prompt3,"stream":False,"options":{"num_predict":2000,"temperature":0.3}})
            r = requests.post("http://localhost:11434/api/generate", data=payload, headers={"Content-Type":"application/json"}, timeout=API_TIMEOUT)
            if r.status_code == 200:
                t = r.json().get("response","")
                if len(t) > 50:
                    t = re.sub(r'^```(yaml)?\n?|\n?```$', '', t)
                    content, source = t, "ollama"
        except: pass
    
    # Fallback
    if not content:
        title = text.split('.')[0].strip()[:80]
        words = title.lower().split()[:8]
        name = '-'.join([re.sub(r'[^a-z0-9]','',w) for w in words if len(w)>2])[:60]
        kw = [w for w in ['hack','malware','phish','exploit','windows','linux','python','network','cloud','ai','android','root','ctf','password'] if w in text[:3000].lower()] or ['siber-guvenlik']
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
    
    sname = save_skill(content, vid_id, kanal, source)
    cache[cache_key] = {"name": sname, "source": source}
    return {"vid_id": vid_id, "status": "ok", "name": sname, "source": source}

def gorev_skill_uret():
    """Bekleyen transcript'lerden max 3 video işle. Paralel: 3 thread. 60s içinde biter."""
    log("🧠 Skill üretme başladı...", "skill")
    
    # Önbellek yükle
    cache = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE) as f: cache = json.load(f)
        except: cache = {}
    
    # İşlenmiş ID'ler
    processed = set()
    if os.path.exists(PROCESSED_V5):
        with open(PROCESSED_V5) as f:
            processed = set(line.strip() for line in f if line.strip())
    
    # Bekleyen videoları bul - hem .srt hem .vtt (büyükten küçüğe)
    pending = []
    # Ana kanallardan
    for kanal, bilgi in KANALLAR.items():
        arsiv = bilgi['arsiv']
        if not os.path.exists(arsiv): continue
        for dosya in sorted(glob.glob(os.path.join(arsiv, '*.srt')) + glob.glob(os.path.join(arsiv, '*.vtt')), key=os.path.getsize, reverse=True)[:10]:
            vid = os.path.basename(dosya).split('.')[0]
            if vid not in processed:
                pending.append((vid, dosya, kanal))
    # Ayrıca pending_transcriptler klasöründen
    pending_dir = os.path.join(DESKTOP, "pending_transcriptler")
    if os.path.exists(pending_dir):
        for dosya in sorted(glob.glob(os.path.join(pending_dir, '*.srt')) + glob.glob(os.path.join(pending_dir, '*.vtt')), key=os.path.getsize, reverse=True)[:5]:
            vid = os.path.basename(dosya).split('.')[0]
            ck = re.sub(r'\.(en|tr)$', '', vid)
            if ck not in processed:
                pending.append((ck, dosya, 'pending'))
    
    if not pending:
        log("   ✅ Bekleyen video yok", "skill")
        return 0
    
    # Max 3 video işle
    hedef_videolar = pending[:MAX_VIDEO_PER_RUN]
    log(f"   📹 {len(pending)} video bekliyor, {len(hedef_videolar)} işlenecek...", "skill")
    
    baslangic = time.time()
    ok = 0
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(process_one_video, v, s, k, cache): (v, k) for v, s, k in hedef_videolar}
        for future in as_completed(futures):
            r = future.result()
            vid_id = r["vid_id"]
            processed.add(vid_id)
            with open(PROCESSED_V5, 'a') as f:
                f.write(f"{vid_id}\n")
            if r["status"] == "ok": ok += 1
    
    # Önbellek kaydet
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    
    gecen = time.time() - baslangic
    log(f"🧠 Skill: {ok} yeni, {gecen:.0f}s", "skill")
    return ok

# === PENDING VIDEOLARI İŞLE ===
def isle_pending_videolar():
    """transcript_pending.txt'deki videoların transcript'lerini manuel çek"""
    if not os.path.exists(PENDING_FILE):
        return 0
    
    with open(PENDING_FILE, 'r') as f:
        ids = [line.strip() for line in f if line.strip()]
    
    if not ids:
        return 0
    
    # Max 3 pending video işle (120s limiti var)
    log(f"📋 {len(ids)} pending video bulundu, max 3 işleniyor...", "pending")
    islenen = 0
    
    for vid_id in ids[:3]:
        try:
            import subprocess
            arsiv = os.path.join(DESKTOP, "pending_transcriptler")
            os.makedirs(arsiv, exist_ok=True)
            
            result = subprocess.run([
                YTDLP, "--write-auto-sub", "--sub-lang", "en,tr",
                "--skip-download", "--convert-subs", "srt",
                "-o", os.path.join(arsiv, "%(id)s"),
                f"https://youtu.be/{vid_id}"
            ], capture_output=True, text=True, timeout=30)
            
            srt_dosyasi = os.path.join(arsiv, f"{vid_id}.en.srt")
            if os.path.exists(srt_dosyasi):
                islenen += 1
                log(f"   ✅ {vid_id} transcript çekildi", "pending")
            else:
                tr_srt = os.path.join(arsiv, f"{vid_id}.tr.srt")
                if os.path.exists(tr_srt):
                    islenen += 1
                    log(f"   ✅ {vid_id} Türkçe transcript çekildi", "pending")
                else:
                    log(f"   ⚠️ {vid_id} transcript bulunamadı", "pending")
        except Exception as e:
            log(f"   ❌ {vid_id} hata: {str(e)[:60]}", "pending")
    
    # Sadece işlenenleri temizle
    kalan_ids = ids[3:]
    if kalan_ids:
        with open(PENDING_FILE, 'w') as f:
            f.write('\n'.join(kalan_ids) + '\n')
        log(f"📋 Pending: {len(ids)-len(kalan_ids)}/{len(ids)} işlendi, {len(kalan_ids)} kaldı", "pending")
    else:
        open(PENDING_FILE, 'w').close()
        log(f"📋 Pending: {islenen} işlendi, kuyruk temizlendi", "pending")
    
    return islenen

# ============================================================
# GÖREV 3: TEMİZLİK — HIZLI (<5s)
# ============================================================
def gorev_temizlik():
    """Anlamsız/tekrarlı skill'leri temizle."""
    log("🧹 Temizlik başladı...", "temizlik")
    
    security_dir = os.path.join(SKILLS_BASE, "security")
    if not os.path.exists(security_dir): return 0
    
    garbage_patterns = [
        r'^music[\- ]', r'\-music', r'^hey[\- ]', r'^hello[\- ]',
        r'^alrighty', r'^all[\- ]?right', r'^well[\- ]hey',
        r'^thanks[\- ]', r'^welcome[\- ]back', r'^before[\- ]dive',
        r'^guys[\- ]', r'^everyone[\- ]', r'^everybody[\- ]',
        r'^whats[\- ]going', r'^hows[\- ]going', r'^righty[\- ]',
        r'^for[\- ]later', r'^this[\- ]video', r'^lets[\- ]',
        r'^gonna[\- ]', r'^okay[\- ]', r'^yeah[\- ]', r'^so[\- ]',
        r'^now[\- ]again', r'^short[\- ]video', r'^real[\- ]quick',
        r'^just[\- ]', r'^little[\- ]', r'^couple[\- ]', r'^lot[\- ]of',
        r'^applause', r'^alrighty$', r'^alright$', r'^all[\- ]right$',
        r'^and[\- ](then|two|mech|actually|welcome)',
        r'^im[\- ](sorry|going|gonna|taking|mall|pretty|running)',
        r'^so[\- ](this|i|if|5g|in|the|couple)',
        r'^this[\- ](is|was|strange|continuation|mp3|the|video|one|example|capture|code)',
    ]
    
    silinen = 0
    for name in os.listdir(security_dir):
        is_garbage = False
        for p in garbage_patterns:
            if re.search(p, name.lower()):
                is_garbage = True
                break
        if is_garbage and len(name) < 30:
            shutil.rmtree(os.path.join(security_dir, name))
            silinen += 1
    
    log(f"🧹 Temizlik: {silinen} anlamsız skill silindi", "temizlik")
    return silinen

# ============================================================
# GÖREV 4: RAPOR
# ============================================================
def gorev_rapor():
    """5 dk'lik rapor hazırla."""
    security_dir = os.path.join(SKILLS_BASE, "security")
    toplam_skill = len([d for d in os.listdir(security_dir) if os.path.isdir(os.path.join(security_dir, d))]) if os.path.exists(security_dir) else 0
    
    toplam_transcript = 0
    for kanal, bilgi in KANALLAR.items():
        arsiv = bilgi['arsiv']
        if os.path.exists(arsiv):
            toplam_transcript += len(glob.glob(os.path.join(arsiv, '*.srt')))
    
    toplam_hedef = sum(b['toplam'] for b in KANALLAR.values())
    yuzde = toplam_transcript * 100 // toplam_hedef if toplam_hedef else 0
    
    # Detaylı per-channel rapor
    detaylar = []
    for kanal, bilgi in KANALLAR.items():
        arsiv = bilgi['arsiv']
        m = len(glob.glob(os.path.join(arsiv, '*.srt'))) if os.path.exists(arsiv) else 0
        h = bilgi['toplam']
        pct = m * 100 // h
        detaylar.append(f"  {kanal}: {m}/{h} (%{pct})")
    
    rapor = f"""📊 SÜPER YÖNETİCİ RAPORU
⏰ {datetime.now().strftime('%H:%M:%S')}
{'='*40}
📹 Transcript: {toplam_transcript}/{toplam_hedef} (%{yuzde})
{'='*40}
""" + '\n'.join(detaylar) + f"""
{'='*40}
🧠 Security Skill: {toplam_skill}"""
    
    if os.path.exists(CACHE_FILE):
        try: rapor += f"\n💾 Önbellek: {os.path.getsize(CACHE_FILE)//1024}KB"
        except: pass
    
    log(rapor, "rapor")
    return rapor

# ============================================================
# ANA DÖNGÜ — TÜM GÖREVLERİ PARALEL ÇALIŞTIR
# ============================================================
def main():
    baslangic = time.time()
    
    log("=" * 50, "ana")
    log("🚀 SÜPER YÖNETİCİ v1.1 BAŞLADI", "ana")
    log(f"API: Gemini={'✅' if GOOGLE_KEY else '❌'} OpenRouter={'✅' if OPENROUTER_KEY else '❌'} Ollama=✅", "ana")
    log(f"Hedef: 120s içinde bitir (şu an: {datetime.now().strftime('%H:%M')})", "ana")
    
    sonuclar = {}
    
    # Pending videoları işle (önce, hızlı biten iş)
    try:
        p = isle_pending_videolar()
        sonuclar["pending"] = p
    except Exception as e:
        sonuclar["pending"] = f"HATA: {str(e)[:60]}"
    
    # Görevleri paralel çalıştır
    with ThreadPoolExecutor(max_workers=3) as executor:
        gorevler = {
            executor.submit(gorev_transcript_cek): "transcript",
            executor.submit(gorev_skill_uret): "skill",
            executor.submit(gorev_temizlik): "temizlik",
        }
        for future in as_completed(gorevler):
            gorev_adi = gorevler[future]
            try:
                sonuclar[gorev_adi] = future.result()
            except Exception as e:
                sonuclar[gorev_adi] = f"HATA: {str(e)[:80]}"
    
    # Rapor
    rapor = gorev_rapor()
    
    gecen = time.time() - baslangic
    log(f"⏱ Toplam: {gecen:.0f}s (limit: 120s)", "ana")
    log(f"📊 {sonuclar}", "ana")
    log("=" * 50, "ana")
    
    if gecen >= 110:
        log("⚠️ KRİTİK: 110s+ sürdü, daha agresif zamanlama gerekebilir!", "ana")
    
    return {
        "transcript": sonuclar.get("transcript", 0),
        "skill": sonuclar.get("skill", 0),
        "temizlik": sonuclar.get("temizlik", 0),
        "sure": f"{gecen:.0f}s",
        "rapor": rapor
    }

if __name__ == "__main__":
    main()
