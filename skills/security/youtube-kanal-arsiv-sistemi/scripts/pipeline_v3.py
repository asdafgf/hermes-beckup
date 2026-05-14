#!/usr/bin/env python3
"""
TRANSCRIPT → CLAUDE/GEMINI → SKILL PIPELINE v3
Her yeni transcript için:
1. Claude API'ye sor (skill oluştur)
2. OpenAI/Gemini API'ye sor (skill oluştur)
3. İkisini karşılaştır, en iyisini seç
4. Security kategorisine SKILL.md olarak kaydet

API KEY'LER YOKSA → sadece transcript özeti + keyword bazlı skill oluşturur.
API KEY'LER VARSA → Claude/Gemini'ye de gönderir, daha kaliteli skill üretir.
"""

import os, re, glob, json, time, requests
from datetime import datetime

BASE = r"C:\Users\eymen\Desktop\transcript_skills"
PROCESSED_FILE = r"C:\Users\eymen\Desktop\transcript_processed_ids_v3.txt"
SKILLS_BASE = r"C:\Users\eymen\AppData\Local\hermes\skills"
LOG_FILE = os.path.join(BASE, "pipeline_v3_log.txt")
CLAUDE_OUT = os.path.join(BASE, "claude_skills")
GEMINI_OUT = os.path.join(BASE, "gemini_skills")
os.makedirs(CLAUDE_OUT, exist_ok=True)
os.makedirs(GEMINI_OUT, exist_ok=True)

CLAUDE_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    print(f"[{t}] {msg}")
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{t}] {msg}\n")

processed = set()
if os.path.exists(PROCESSED_FILE):
    with open(PROCESSED_FILE) as f:
        processed = set(line.strip() for line in f if line.strip())

def extract_clean_text(srt_path):
    with open(srt_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    lines = content.split('\n')
    text = []
    for line in lines:
        line = line.strip()
        if re.match(r'^\d+$', line): continue
        if re.match(r'^\d{2}:\d{2}:\d{2}', line): continue
        if line == '': continue
        text.append(line)
    result = ' '.join(text)
    result = re.sub(r'(\b\w+\b)( \1\b){2,}', r'\1', result)
    return result[:12000]

def extract_keywords(text):
    terms = [
        r'\bmalware\b', r'\bransomware\b', r'\bphishing\b', r'\bexploit\b',
        r'\bpayload\b', r'\bbackdoor\b', r'\btrojan\b', r'\bkeylogger\b',
        r'\bc2\b', r'\binfostealer\b', r'\bdropper\b',
        r'\bpowershell\b', r'\bpython\b', r'\bbash\b', r'\bgolang\b',
        r'\blinux\b', r'\bwindows\b', r'\bactive directory\b', r'\bentra\b',
        r'\bazure\b', r'\baws\b', r'\bcloud\b', r'\bdocker\b', r'\bkubernetes\b',
        r'\bnmap\b', r'\bmetasploit\b', r'\bburp\b',
        r'\bsql injection\b', r'\bxss\b', r'\brce\b',
        r'\bprivilege escalation\b', r'\bpersistence\b',
        r'\bcredential\b', r'\bpassword\b', r'\bmfa\b', r'\b2fa\b',
        r'\bvpn\b', r'\btor\b', r'\bdark web\b', r'\bencryption\b',
        r'\bsupply chain\b', r'\bnpm\b', r'\bdependency\b',
        r'\bai\b', r'\bgpt\b', r'\bllm\b', r'\bprompt injection\b', r'\bmcp\b',
        r'\bwireshark\b', r'\bfirewall\b', r'\bsiem\b', r'\bwazuh\b',
        r'\bthreat hunting\b', r'\bforensic\b', r'\bdfir\b',
        r'\bctf\b', r'\bhackthebox\b', r'\btryhackme\b',
        r'\bntlm\b', r'\bkerberos\b', r'\bbloodhound\b',
        r'\bcursor\b', r'\bcopilot\b', r'\bcodex\b',
    ]
    found = []
    text_lower = text.lower()[:5000]
    for pattern in terms:
        m = re.search(pattern, text_lower)
        if m:
            found.append(m.group())
    return list(dict.fromkeys(found))[:5]

def generate_skill_name(keywords, text):
    if keywords:
        name = '-'.join(keywords[:3])
        name = re.sub(r'[^a-z0-9-]', '', name.lower())
        if len(name) > 5 and len(name) < 60:
            return name
    first_sentence = text.split('.')[0].strip()
    skip_patterns = [r'^hey\b', r'^all right', r'^alrighty', r'^hello\b',
                     r'^well hey', r'^before dive', r'^what.s\b', r'^righty']
    for sp in skip_patterns:
        if re.search(sp, first_sentence.lower()):
            parts = text.split('.')
            if len(parts) > 1:
                first_sentence = parts[1].strip()
            break
    words = first_sentence.split()[:6]
    name = '-'.join([w.lower().strip('.,!?\'"') for w in words if len(w) > 2])
    name = re.sub(r'[^a-z0-9-]', '', name)
    if len(name) < 5:
        return None
    return name[:60]

def determine_category(keywords, text):
    text_lower = text.lower()[:3000]
    kw_text = ' '.join(keywords).lower()
    if any(w in kw_text or w in text_lower for w in ['malware', 'ransomware', 'trojan', 'backdoor']):
        return 'malware-analysis'
    if any(w in kw_text or w in text_lower for w in ['phishing', 'scam', 'credential']):
        return 'phishing'
    if any(w in kw_text or w in text_lower for w in ['windows', 'active directory', 'entra', 'lsass']):
        return 'windows-security'
    if any(w in kw_text or w in text_lower for w in ['linux', 'bash', 'privilege escalation']):
        return 'linux-security'
    if any(w in kw_text or w in text_lower for w in ['python', 'coding', 'golang']):
        return 'programming'
    if any(w in kw_text or w in text_lower for w in ['network', 'wireshark', 'nmap', 'firewall', 'cisco']):
        return 'networking'
    if any(w in kw_text or w in text_lower for w in ['ai', 'gpt', 'llm', 'claude', 'mcp']):
        return 'ai-security'
    if any(w in kw_text or w in text_lower for w in ['cloud', 'aws', 'azure', 'docker']):
        return 'cloud-security'
    if any(w in kw_text or w in text_lower for w in ['supply chain', 'npm', 'dependency']):
        return 'supply-chain'
    if any(w in kw_text or w in text_lower for w in ['ctf', 'capture the flag', 'hack', 'pentest']):
        return 'pen-testing'
    if any(w in kw_text or w in text_lower for w in ['tor', 'dark web', 'privacy', 'encryption']):
        return 'privacy-tor'
    if any(w in kw_text or w in text_lower for w in ['forensic', 'incident response', 'wazuh', 'siem']):
        return 'incident-response'
    return 'general-security'

def ask_claude(transcript_text, video_id, kanal):
    if not CLAUDE_API_KEY:
        return None, "CLAUDE_API_KEY yok"
    prompt = f"""You are analyzing a cybersecurity video transcript. Create a Hermes Agent SKILL.md file.
Video source: https://youtu.be/{video_id}  Channel: {kanal}
Create a valid SKILL.md with YAML frontmatter (name, description, category: security, tags), description of technique, step-by-step guide. Respond ONLY with valid SKILL.md.
TRANSCRIPT: {transcript_text[:10000]}"""
    try:
        resp = requests.post("https://api.anthropic.com/v1/messages",
            headers={"x-api-key": CLAUDE_API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={"model": "claude-sonnet-4-20250514", "max_tokens": 2000, "messages": [{"role": "user", "content": prompt}]},
            timeout=60)
        if resp.status_code == 200:
            return resp.json()["content"][0]["text"], None
        else:
            return None, f"Claude hata {resp.status_code}"
    except Exception as e:
        return None, f"Claude exception: {str(e)[:80]}"

def ask_openai(transcript_text, video_id, kanal):
    if not OPENAI_API_KEY:
        return None, "OPENAI_API_KEY yok"
    prompt = f"""Create a Hermes Agent SKILL.md for this cybersecurity video transcript.\nVideo: https://youtu.be/{video_id}\nChannel: {kanal}\n\nTRANSCRIPT:\n{transcript_text[:10000]}"""
    try:
        resp = requests.post("https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "content-type": "application/json"},
            json={"model": "gpt-4o-mini", "max_tokens": 2000, "messages": [{"role": "user", "content": prompt}]},
            timeout=60)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"], None
        else:
            return None, f"OpenAI hata {resp.status_code}"
    except Exception as e:
        return None, f"OpenAI exception: {str(e)[:80]}"

def save_skill(content, video_id, kanal):
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            for line in parts[1].split('\n'):
                if line.strip().startswith('name:'):
                    name = line.split(':', 1)[1].strip().strip('"\'')
                    name = re.sub(r'[^a-z0-9-]', '', name.lower())
                    if name and len(name) >= 3:
                        break
            else:
                name = f"{kanal}-{video_id[:8]}"
        else:
            name = f"{kanal}-{video_id[:8]}"
    else:
        name = f"{kanal}-{video_id[:8]}"
    skill_dir = os.path.join(SKILLS_BASE, "security", name)
    os.makedirs(skill_dir, exist_ok=True)
    with open(os.path.join(skill_dir, "SKILL.md"), 'w', encoding='utf-8') as f:
        f.write(content)
    return name

# ============ ANA DÖNGÜ ============
kanallar = {
    'john-hammond': r"C:\Users\eymen\Desktop\rootofthenull_arsiv\transcriptler",
    'networkchuck': r"C:\Users\eymen\Desktop\networkchuck_arsiv\transcriptler",
    'david-bombal': r"C:\Users\eymen\Desktop\davidbombal_arsiv\transcriptler",
}

log("=== PIPELINE v3 BAŞLADI ===")
log(f"Claude API: {'VAR' if CLAUDE_API_KEY else 'YOK'} | OpenAI API: {'VAR' if OPENAI_API_KEY else 'YOK'}")

if not CLAUDE_API_KEY and not OPENAI_API_KEY:
    log("⚠️ API KEY'LER YOK — keyword-based modda çalışılıyor")
    log("   API key eklemek için: export ANTHROPIC_API_KEY=... export OPENAI_API_KEY=...")

islenen = 0
for kanal, trans_dir in kanallar.items():
    if not os.path.exists(trans_dir):
        continue
    srts = sorted(glob.glob(os.path.join(trans_dir, '*.srt')), key=os.path.getsize, reverse=True)
    for srt_path in srts:
        vid_id = os.path.basename(srt_path).split('.')[0]
        if vid_id in processed:
            continue
        log(f"\n>>> [{kanal}] {vid_id}")
        text = extract_clean_text(srt_path)
        if len(text) < 200:
            log("   ⚠️ Çok kısa, atlandı"); processed.add(vid_id); continue
        log(f"   Transcript: {len(text)} karakter")
        
        # API'ler varsa Claude/Gemini'ye sor
        claude_result = None
        openai_result = None
        
        if CLAUDE_API_KEY:
            log("   🤖 Claude'a soruluyor...")
            claude_result, err = ask_claude(text, vid_id, kanal)
            if claude_result:
                name = save_skill(claude_result, vid_id, kanal)
                with open(os.path.join(CLAUDE_OUT, f"{name}.md"), 'w', encoding='utf-8') as f:
                    f.write(claude_result)
                log(f"   ✅ Claude → {name}")
            else:
                log(f"   ⚠️ Claude: {err}")
        
        if OPENAI_API_KEY:
            log("   🤖 OpenAI'a soruluyor...")
            openai_result, err = ask_openai(text, vid_id, kanal)
            if openai_result:
                name = save_skill(openai_result, vid_id, kanal)
                with open(os.path.join(GEMINI_OUT, f"{name}.md"), 'w', encoding='utf-8') as f:
                    f.write(openai_result)
                log(f"   ✅ OpenAI → {name}")
            else:
                log(f"   ⚠️ OpenAI: {err}")
        
        # API'ler yoksa keyword-based skill oluştur
        if not claude_result and not openai_result:
            keywords = extract_keywords(text)
            skill_name = generate_skill_name(keywords, text)
            if not skill_name:
                skill_name = f"{kanal}-{vid_id[:8]}"
            category = determine_category(keywords, text)
            kw_str = ', '.join(keywords) if keywords else "siber güvenlik"
            
            skill_content = f"""---
name: {skill_name}
description: "{kanal} videosundan çıkarılan: {kw_str}"
version: 1.0
author: hermes
category: security
source: "https://youtu.be/{vid_id}"
tags: [{', '.join(keywords[:5])}, {kanal}, video-notu]
---
# {kw_str}
**Kaynak:** [YouTube](https://youtu.be/{vid_id}) | **Kanal:** {kanal}
**Kategori:** {category}
## 🎯 Konu
{kw_str}
## 📝 Transcript Özeti
{text[:2000]}
## 🔑 Anahtar Kelimeler
{kw_str}
## 📌 Nasıl Kullanılır
1. Videoyu izle: https://youtu.be/{vid_id}
2. Transcript özetini oku
3. Konuyu pratikte dene
"""
            name = save_skill(skill_content, vid_id, kanal)
            log(f"   ✅ Keyword skill → {skill_name}")
        
        processed.add(vid_id)
        with open(PROCESSED_FILE, 'a') as f:
            f.write(f"{vid_id}\n")
        islenen += 1
        time.sleep(1)

log(f"\n📊 BATCH TAMAM — {islenen} işlendi | Toplam: {len(processed)}")
log("=== PIPELINE v3 BİTTİ ===")
