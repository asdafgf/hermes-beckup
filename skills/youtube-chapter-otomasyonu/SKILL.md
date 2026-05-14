---
name: youtube-chapter-otomasyonu
description: "Python + OpenAI ile YouTube videolarına otomatik bölüm (chapter) oluşturma — youtube-transcript-api ile transcript çek, GPT-4o-mini'ye bölümlere ayırttır, Streamlit UI ile kullan"
version: 1.0
category: software-development
source: "https://youtu.be/AmIL_TpsXjo"
tags: [youtube, chapters, transcript, openai, gpt, automation, streamlit, python]
platforms: [linux, macos, windows]
---

# 🎬 YouTube Chapter Otomasyonu

**Kaynak:** [YouTube](https://youtu.be/AmIL_TpsXjo)

Python + OpenAI ile YouTube videolarına otomatik olarak zaman damgalı bölüm başlıkları (chapters) oluştur.

---

## 📦 Kurulum

```bash
pip install youtube-transcript-api openai streamlit python-dotenv
```

## 🔑 API Anahtarı

`.env` dosyası oluştur:

```env
OPENAI_API_KEY=sk-...
```

## 🐍 Tam Python Kodu

```python
import os
import re
from dotenv import load_dotenv
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_video_id(url):
    patterns = [
        r'(?:v=|youtu\.be/|shorts/|embed/|live/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return url

def extract_transcript(video_id, language='en'):
    api = YouTubeTranscriptApi()
    segments = list(api.fetch(video_id, languages=[language]))
    result = []
    for seg in segments:
        minutes = int(seg.start // 60)
        seconds = int(seg.start % 60)
        result.append(f"{minutes}:{seconds:02d} {seg.text}")
    return "\n".join(result)

def sanitize_text(text):
    return text.replace('"', "'").replace('"', "'")

def generate_chapters(transcript, num_chapters=5):
    sanitized = sanitize_text(transcript)

    prompt = f"""You are a YouTube chapter generator. Given the following transcript, divide it into exactly {num_chapters} logical chapters.

For each chapter, provide:
- The start timestamp (MM:SS)
- A concise, descriptive title (max 60 chars)

Rules:
- Chapters must cover the entire video sequentially
- Start each chapter on a new line
- Format: MM:SS Title
- Use the actual transcript timestamps

Transcript:
{sanitized}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate YouTube chapter markers. Always start each chapter on a new line with format MM:SS Title."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

def format_chapters(raw_text):
    lines = raw_text.strip().split("\n")
    formatted = []
    for line in lines:
        line = line.strip()
        if re.match(r'^(\d+:)?\d{1,2}:\d{2}', line):
            formatted.append(line)
    return "\n".join(formatted)

def process_youtube_video(video_url, chapters=5):
    vid = extract_video_id(video_url)
    print(f"📹 Video ID: {vid}")
    
    transcript = extract_transcript(vid)
    print(f"📝 Transcript: {len(transcript)} chars")
    
    raw = generate_chapters(transcript, chapters)
    formatted = format_chapters(raw)
    
    print("\n" + "=" * 50)
    print("📋 CHAPTERS (paste into YouTube description):")
    print("=" * 50)
    print(formatted)
    return formatted

# === KULLANIM ===
# process_youtube_video("https://youtu.be/VIDEO_ID", chapters=5)
```

## 🖥️ Streamlit UI

```python
# interface.py
import streamlit as st
from chapter_generator import process_youtube_video

st.set_page_config(page_title="YouTube Chapter Generator", page_icon="🎬")
st.title("🎬 YouTube Chapter Generator")
st.markdown("Automatically generate timestamped chapters for any YouTube video.")

video_url = st.text_input("YouTube Video URL")
num_chapters = st.slider("Number of chapters", min_value=3, max_value=15, value=5)

if st.button("Generate Chapters") and video_url:
    with st.spinner("Processing..."):
        try:
            chapters = process_youtube_video(video_url, num_chapters)
            st.success("Chapters generated!")
            st.text_area("Result", chapters, height=300)
            st.code(chapters, language="text")
        except Exception as e:
            st.error(f"Error: {str(e)}")
```

Çalıştır: `streamlit run interface.py`

---

## 🧪 Kullanım

```python
from chapter_generator import process_youtube_video

# 5 bölümlü chapter oluştur
process_youtube_video("https://youtu.be/VIDEO_ID")

# 10 bölümlü
process_youtube_video("https://youtu.be/VIDEO_ID", chapters=10)
```

## ⚠️ Hata Yönetimi

| Sorun | Çözüm |
|-------|-------|
| Transcript yok | Farklı dil dene veya video altyazıları kapalı |
| Encoding hatası | `sanitize_text()` ile tek tırnak standardize et |
| Token limit | Uzun transcript'lerde chapters sayısını düşür |
| API timeout | `timeout` parametresi ekle (örn. `timeout=30`) |
