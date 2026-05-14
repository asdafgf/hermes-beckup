---
name: serpapi-youtube-transcript
description: "SerpAPI YouTube Transcript API ile video transkriptlerini çekme — Python requests ile API çağrısı, dil desteği, otomatik konuşma tanıma, chapter çekme"
version: 1.0
category: software-development
source: "https://youtu.be/wpSqsVHXGIA"
tags: [serpapi, youtube, transcript, api, scraping, python]
platforms: [linux, macos, windows]
---

# 🔍 SerpAPI YouTube Transcript API

**Kaynak:** [YouTube](https://youtu.be/wpSqsVHXGIA)

SerpAPI'nin YouTube Transcript API'si ile videolardan anında transkript çek.

---

## 📦 Kurulum

```bash
pip install requests python-dotenv
```

## 🔑 API Anahtarı

1. https://serpapi.com adresine kaydol
2. Dashboard'dan API key al
3. `.env` dosyasına ekle

## 🐍 Temel Kullanım

```python
import os, json, requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SERPAPI_API_KEY")

def get_youtube_transcript(video_id, language=None):
    params = {"api_key": API_KEY, "engine": "youtube_video_transcript", "video_id": video_id}
    if language:
        params["language_code"] = language
    else:
        params["type"] = "auto"
    return requests.get("https://serpapi.com/search", params=params).json()

video_id = "dQw4w9WgXcQ"
result = get_youtube_transcript(video_id)
print(json.dumps(result, indent=2, ensure_ascii=False))
```

## 📝 Transkripti Düzenli Göster

```python
def print_clean_transcript(video_id):
    data = get_youtube_transcript(video_id)
    if "transcripts" not in data:
        print("Transkript bulunamadı:", data.get("error"))
        return
    for item in data["transcripts"]:
        start_sec = item.get("start", 0) / 1000
        m, s = divmod(int(start_sec), 60)
        print(f"{m}:{s:02d}  {item.get('snippet','')}")
```

## 🌍 Dil Desteği

```python
# Almanca çeviri (type="auto" kullanma!)
result = get_youtube_transcript("video_id", language="de")
```

## 📋 Chapter Bilgisi

```python
def get_chapters(video_id):
    data = get_youtube_transcript(video_id)
    for ch in data.get("chapters", []):
        start_sec = ch.get("start", 0) / 1000
        m, s = divmod(int(start_sec), 60)
        print(f"{m}:{s:02d}  {ch.get('title','')}")
```

## ⚙️ Parametre Tablosu

Parametre: api_key → Zorunlu: ✅ → Açıklama: SerpAPI anahtarı
Parametre: engine → Zorunlu: ✅ → Açıklama: youtube_video_transcript
Parametre: video_id → Zorunlu: ✅ → Açıklama: 11 karakter video ID
Parametre: type → Zorunlu: ❌ → Açıklama: auto (otomatik konuşma)
Parametre: language_code → Zorunlu: ❌ → Açıklama: en, de, tr, fr...

> ⏱ Zaman değerleri **milisaniye** ! Saniyeye çevir: `/ 1000`
