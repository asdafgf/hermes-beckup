#!/usr/bin/env python3
"""SÜPER YÖNETİCİ v1.1 — Hızlı Raporlama
Cronjob'dan bağımsız çalışan durum raporu.
Transcript sayıları, skill durumu, temizlik logları.
Dosya sayımı .srt uzantısına göre yapılır."""
import os, json, glob, time, re
from datetime import datetime

HOME = os.path.expanduser('~')
DESKTOP = os.path.join(HOME, 'Desktop')
SKILLS_BASE = os.path.join(HOME, 'AppData', 'Local', 'hermes', 'skills')
CACHE_FILE = os.path.join(DESKTOP, 'transcript_skills', 'skill_cache.json')
LOG_DIR = os.path.join(DESKTOP, 'super_yonetici_loglari')

t_start = time.time()
print(f'[SUPER-YONETICI v1.1] Basladi: {datetime.now().strftime("%H:%M:%S")}')

# 1. Transcript sayilari (.srt uzantisi!)
jh = len(glob.glob(os.path.join(DESKTOP, 'rootofthenull_arsiv', 'transcriptler', '*.srt')))
nc = len(glob.glob(os.path.join(DESKTOP, 'networkchuck_arsiv', 'transcriptler', '*.srt')))
db = len(glob.glob(os.path.join(DESKTOP, 'davidbombal_arsiv', 'transcriptler', '*.srt')))
total_t = jh + nc + db
target_t = 1602 + 372 + 1483
pct = round(100 * total_t / target_t)

# 2. Skill sayilari
total_skills = 0
for cat in os.listdir(SKILLS_BASE):
    cat_path = os.path.join(SKILLS_BASE, cat)
    if os.path.isdir(cat_path) and not cat.endswith('.json'):
        total_skills += len(glob.glob(os.path.join(cat_path, '*', 'SKILL.md')))
skill_sec = len(glob.glob(os.path.join(SKILLS_BASE, 'security', '*', 'SKILL.md')))
skill_dev = len(glob.glob(os.path.join(SKILLS_BASE, 'devops', '*', 'SKILL.md')))

# 3. Cache
cache_size = os.path.getsize(CACHE_FILE) if os.path.exists(CACHE_FILE) else 0

# 4. Son temizlik
print('\n=== SON TEMIZLIK ===')
temiz_log = os.path.join(LOG_DIR, 'temizlik.log')
if os.path.exists(temiz_log):
    with open(temiz_log) as f:
        tlines = f.readlines()
    for l in [x.strip() for x in tlines[-10:] if x.strip()]:
        print(f'  {l}')

# 5. Son skill uretimi
print('\n=== SON SKILL URETIMI ===')
skill_log_file = os.path.join(LOG_DIR, 'skill.log')
if os.path.exists(skill_log_file):
    with open(skill_log_file) as f:
        slines = f.readlines()
    for l in [x.strip() for x in slines[-5:] if x.strip()]:
        print(f'  {l}')

# 6. Kronik sorun tespiti
print('\n=== KRONIK SORUNLAR ===')
ana_log = os.path.join(LOG_DIR, 'ana.log')
if os.path.exists(ana_log):
    with open(ana_log) as f:
        al = f.read()
    timeout_count = len(re.findall(r'timeout', al))
    v1_count = len(re.findall(r'v1 BASLADI', al)) - len(re.findall(r'v1\.1 BASLADI', al))
    v11_count = len(re.findall(r'v1\.1 BASLADI', al))
    print(f'  Timeout sayisi (bugun): {timeout_count}')
    print(f'  v1 (eski) calisma: {v1_count}')
    print(f'  v1.1 (yeni) calisma: {v11_count}')

tlog_file = os.path.join(LOG_DIR, 'transcript.log')
if os.path.exists(tlog_file):
    with open(tlog_file) as f:
        tlog = f.read()
    plus_total = sum(int(x) for x in re.findall(r'\+(\d+) yeni transcript', tlog))
    print(f'  Toplam yeni transcript bugun: +{plus_total}')

# 7. RAPOR
print()
print('='*55)
print(f'  📊 SÜPER YÖNETİCİ RAPORU')
print(f'  ⏰ {datetime.now().strftime("%H:%M:%S")}')
print('='*55)
print(f'  📹 Transcript: {total_t}/{target_t} (%{pct})')
print(f'     john-hammond:   {jh}/1602 (%{round(jh/1602*100)})')
print(f'     networkchuck:   {nc}/372  (%{round(nc/372*100)})')
print(f'     david-bombal:   {db}/1483 (%{round(db/1483*100)})')
print(f'  🧠 Security Skill: {skill_sec}')
print(f'  📦 Toplam Skill:   {total_skills}')
print(f'  💾 Cache:          {cache_size//1024}KB')
print(f'  ⏱ Sure:           {round(time.time()-t_start)}s')
print('='*55)

# 8. Kalan is
print(f'\n  KALAN IS: {target_t - total_t} transcript')
print(f'  Kanal bazinda kalan:')
print(f'     john-hammond:   {1602-jh} (en buyuk eksik)')
print(f'     david-bombal:   {1483-db}')
print(f'     networkchuck:   tamam')
print(f'\n[SUPER-YONETICI] Bitti: sured: {round(time.time()-t_start)}s')
