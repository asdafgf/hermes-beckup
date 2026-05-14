#!/usr/bin/env python3
"""
TRANSCRIPT → SKILL PIPELINE v2
Bir kanal için ZIPLENEBİLİR versiyon. Kullanım:
  python3 pipeline_v2.py

Tüm 3 kanalı tarar, işlenmemiş transcript'leri skill'e çevirir.
processed_ids_v2.txt ile tekrar işlemeyi engeller.
"""

import os, re, glob, json, time, sys, requests
from datetime import datetime

BASE = r"C:\Users\eymen\Desktop\transcript_skills"
PROCESSED_FILE = r"C:\Users\eymen\Desktop\transcript_processed_ids_v2.txt"
SKILLS_BASE = r"C:\Users\eymen\AppData\Local\hermes\skills"
LOG_FILE = os.path.join(BASE, "pipeline_v2_log.txt")

os.makedirs(os.path.join(BASE, "kaydedilen"), exist_ok=True)

def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    line = f"[{t}] {msg}"
    print(line)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + "\n")

processed = set()
if os.path.exists(PROCESSED_FILE):
    with open(PROCESSED_FILE) as f:
        processed = set(line.strip() for line in f if line.strip())

TERMS = [
    r'\bmalware\b', r'\bransomware\b', r'\bphishing\b', r'\bexploit\b',
    r'\bpayload\b', r'\bbackdoor\b', r'\btrojan\b', r'\bkeylogger\b',
    r'\bc2\b', r'\bcommand.{0,20}control\b', r'\binfostealer\b', r'\bloader\b',
    r'\bdropper\b', r'\bpowershell\b', r'\bpython\b', r'\bbash\b',
    r'\blinux\b', r'\bwindows\b', r'\bactive directory\b', r'\bentra\b',
    r'\bazure\b', r'\baws\b', r'\bcloud\b', r'\bdocker\b', r'\bkubernetes\b',
    r'\bnmap\b', r'\bmetasploit\b', r'\bburp\b', r'\bsql injection\b',
    r'\bxss\b', r'\brce\b', r'\bprivilege escalation\b', r'\bpersistence\b',
    r'\bcredential\b', r'\bpassword\b', r'\bmfa\b', r'\b2fa\b',
    r'\bvpn\b', r'\btor\b', r'\bdark web\b', r'\bprivacy\b', r'\bencryption\b',
    r'\bsupply chain\b', r'\bnpm\b', r'\bdependency\b',
    r'\bai\b', r'\bgpt\b', r'\bllm\b', r'\bprompt injection\b', r'\bmcp\b',
    r'\bwireshark\b', r'\bfirewall\b', r'\bsiem\b', r'\bwazuh\b', r'\bedr\b',
    r'\bthreat hunting\b', r'\bforensic\b', r'\bdfir\b', r'\bincident response\b',
    r'\bctf\b', r'\bcapture the flag\b', r'\btryhackme\b',
    r'\bcertification\b', r'\bccna\b',
    r'\bwindows firewall\b', r'\blsass\b', r'\bmimikatz\b',
    r'\bntlm\b', r'\bkerberos\b', r'\bbloodhound\b', r'\bresponder\b',
    r'\bimpacket\b', r'\bgolang\b', r'\bcursor\b', r'\bcopilot\b', r'\bcodex\b',
]

SKIP_PATTERNS = [
    r'^hey\b', r'^all right', r'^alrighty', r'^hello\b',
    r'^well hey', r'^before dive', r'^what.s\b', r'^righty'
]

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
    return result

def extract_keywords(text):
    found = []
    text_lower = text.lower()[:5000]
    for pattern in TERMS:
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
    for sp in SKIP_PATTERNS:
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
    if any(w in kw_text or w in text_lower for w in ['malware', 'ransomware', 'trojan', 'backdoor', 'infostealer', 'keylogger']):
        return 'malware-analysis'
    if any(w in kw_text or w in text_lower for w in ['phishing', 'scam', 'social engineering', 'credential']):
        return 'phishing'
    if any(w in kw_text or w in text_lower for w in ['windows', 'active directory', 'entra', 'microsoft', 'lsass', 'mimikatz']):
        return 'windows-security'
    if any(w in kw_text or w in text_lower for w in ['linux', 'bash', 'shell', 'privilege escalation']):
        return 'linux-security'
    if any(w in kw_text or w in text_lower for w in ['python', 'coding', 'programming']):
        return 'programming'
    if any(w in kw_text or w in text_lower for w in ['network', 'wireshark', 'nmap', 'firewall']):
        return 'networking'
    if any(w in kw_text or w in text_lower for w in ['ai', 'gpt', 'llm', 'claude', 'chatgpt', 'prompt injection', 'mcp']):
        return 'ai-security'
    if any(w in kw_text or w in text_lower for w in ['cloud', 'aws', 'azure', 'docker', 'kubernetes']):
        return 'cloud-security'
    if any(w in kw_text or w in text_lower for w in ['supply chain', 'npm', 'dependency']):
        return 'supply-chain'
    if any(w in kw_text or w in text_lower for w in ['ctf', 'capture the flag', 'tryhackme', 'pentest']):
        return 'pen-testing'
    if any(w in kw_text or w in text_lower for w in ['tor', 'dark web', 'privacy', 'encryption', 'vpn']):
        return 'privacy-tor'
    if any(w in kw_text or w in text_lower for w in ['forensic', 'dfir', 'incident response', 'wazuh', 'siem']):
        return 'incident-response'
    return 'general-security'

def get_title(text):
    first = text.split('.')[0].strip()
    for sp in SKIP_PATTERNS:
        if re.search(sp, first.lower()):
            parts = text.split('.')
            if len(parts) > 1:
                first = parts[1].strip()
            break
    return first[:100]

kanallar = {
    'john-hammond': r"C:\Users\eymen\Desktop\rootofthenull_arsiv\transcriptler",
    'networkchuck': r"C:\Users\eymen\Desktop\networkchuck_arsiv\transcriptler",
    'david-bombal': r"C:\Users\eymen\Desktop\davidbombal_arsiv\transcriptler",
}

log("=== PIPELINE v2 BAŞLADI ===")
log(f"Önceden işlenen: {len(processed)}")

islenen = 0
for kanal, trans_dir in kanallar.items():
    if not os.path.exists(trans_dir):
        continue
    srts = sorted(glob.glob(os.path.join(trans_dir, '*.srt')), key=os.path.getsize, reverse=True)
    for srt_path in srts:
        vid_id = os.path.basename(srt_path).split('.')[0]
        if vid_id in processed:
            continue
        text = extract_clean_text(srt_path)
        if len(text) < 100:
            processed.add(vid_id); continue
        keywords = extract_keywords(text)
        skill_name = generate_skill_name(keywords, text)
        if not skill_name:
            skill_name = f"{kanal}-{vid_id[:8]}"
        category = determine_category(keywords, text)
        title = get_title(text)
        kw_str = ', '.join(keywords) if keywords else "siber güvenlik"

        content = f"""---
name: {skill_name}
description: "{title}"
version: 1.0
author: hermes
category: security
source: "https://youtu.be/{vid_id}"
tags: [{', '.join(keywords[:5])}, {kanal}, video-notu]
---

# {title}

**Kaynak:** [YouTube](https://youtu.be/{vid_id}) | **Kanal:** {kanal}
**Kategori:** {category}

---

## 🎯 Konu

{kw_str}

---

## 📝 Transcript Özeti

{text[:2000]}

---

## 🔑 Anahtar Kelimeler
{', '.join(keywords) if keywords else 'Siber güvenlik'}

---

## ▶️ Nasıl Kullanılır
1. Videoyu izle: https://youtu.be/{vid_id}
2. Transcript özetini oku
3. Güvenli ortamda dene

---

## 🔗 İlgili Skill'ler
- youtube-kanal-arsiv-sistemi
"""
        skill_dir = os.path.join(SKILLS_BASE, "security", skill_name)
        os.makedirs(skill_dir, exist_ok=True)
        with open(os.path.join(skill_dir, "SKILL.md"), 'w', encoding='utf-8') as f:
            f.write(content)
        with open(os.path.join(BASE, "kaydedilen", f"{skill_name}.md"), 'w', encoding='utf-8') as f:
            f.write(content)

        processed.add(vid_id)
        with open(PROCESSED_FILE, 'a') as f:
            f.write(f"{vid_id}\n")
        islenen += 1
        log(f"✅ {kanal}/{skill_name}")
        time.sleep(0.3)

log(f"\n📊 BATCH: {islenen} yeni | {len(processed)} toplam")
log("=== BİTTİ ===")
