#!/usr/bin/env python3
"""
OTOMATİK SKILL ÜRETİCİ v4
Full automated pipeline: Gemini → Claude → Fallback → Save
Runs via cronjob every 15 minutes. Never asks the user.
"""

import os, re, glob, json, time, sys, subprocess, requests
from datetime import datetime

SKILLS_BASE = r"C:\Users\eymen\AppData\Local\hermes\skills"
PROCESSED_FILE = r"C:\Users\eymen\Desktop\transcript_processed_ids_v4.txt"
LOG_FILE = r"C:\Users\eymen\Desktop\transcript_skills\otomatik_log.txt"
BASE_DIR = r"C:\Users\eymen\Desktop"

def get_api_key(var_name):
    val = os.environ.get(var_name, "")
    if val: return val
    try:
        result = subprocess.run(
            ["powershell.exe", "-Command", f"[System.Environment]::GetEnvironmentVariable('{var_name}','User')"],
            capture_output=True, text=True, timeout=5
        )
        val = result.stdout.strip()
        if val: os.environ[var_name] = val
        return val
    except: return ""

GOOGLE_API_KEY = get_api_key("GOOGLE_API_KEY")
OPENROUTER_API_KEY = get_api_key("OPENROUTER_API_KEY")

KANALLAR = {
    'john-hammond': os.path.join(BASE_DIR, 'rootofthenull_arsiv', 'transcriptler'),
    'networkchuck': os.path.join(BASE_DIR, 'networkchuck_arsiv', 'transcriptler'),
    'david-bombal': os.path.join(BASE_DIR, 'davidbombal_arsiv', 'transcriptler'),
}

def extract_text(srt_path):
    with open(srt_path, 'r', encoding='utf-8', errors='replace') as f:
        return ' '.join(
            line.strip() for line in f.read().split('\n')
            if line.strip() and not re.match(r'^\d+$', line) and not re.match(r'^\d{2}:\d{2}:\d{2}', line)
        )[:12000]

def ask_gemini(transcript, video_id, kanal):
    if not GOOGLE_API_KEY: return None
    prompt = f"Create a Hermes Agent SKILL.md from this transcript. Video: https://youtu.be/{video_id} Channel: {kanal}\n\nTranscript:\n{transcript[:10000]}"
    for attempt in range(3):
        try:
            resp = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}",
                json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"maxOutputTokens": 2000}},
                timeout=60
            )
            if resp.status_code == 200:
                return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            elif resp.status_code == 429:
                time.sleep(10 * (attempt + 1))
            else:
                return None
        except: return None
    return None

# Script continues with same logic as v4...
# Full source: ~/Desktop/transcript_skills/otomatik_skill_uretici_v4.py
