---
name: patrick-loeber-gemini-python-sdk
description: "Patrick Loeber (DeepMind) — Gemini Python SDK ile baslangic. AI Studio, multimodal (gorsel/video/ses), Gemini 2.5 thinking, chat, API key"
version: 1.0
category: software-development
source: "Patrick Loeber YouTube"
tags: [python, gemini, google-ai, sdk, multimodal, thinking-model, ai-studio]
platforms: [linux, macos, windows]
---

# Gemini Python SDK Baslangic

Kaynak: Patrick Loeber (Google DeepMind Developer)

## AI Studio

https://aistudio.google.com

- Tum Gemini modellerini dene (2.5 Flash, 2.0, Chemma)
- Prompt playground
- API key olustur
- Baslangic kodu uret

## Python SDK Kurulum

```bash
pip install google-genai
```

## Temel Kullanim

```python
from google import genai

client = genai.Client(api_key="YOUR_KEY")

# Basit chat
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is the capital of France?"
)
print(response.text)
```

## Chat

```python
chat = client.chats.create(model="gemini-2.5-flash")
response = chat.send_message("Tell me a joke")
print(response.text)
```

## Multimodal (Gorsel + Metin)

```python
import PIL.Image

image = PIL.Image.open("photo.jpg")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=["Describe this image", image]
)
print(response.text)
```

## Video / Ses Anlama

```python
# Video dosyasi
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=["What happens in this video?", "gs://bucket/video.mp4"]
)
```

## Thinking Model (Gemini 2.5)

```python
# Gemini 2.5 thinking modu
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents="Solve this complex math problem step by step"
)
```

## Ayar Parametreleri

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Write a poem",
    config={
        "temperature": 0.7,
        "max_output_tokens": 500,
        "top_p": 0.9,
    }
)
```

## Notlar

- AI Studio en iyi baslangic noktasi
- API key ucretsiz (kota limitli)
- Gemini 2.5 Flash hizli ve ucuz
- Multimodal Gemini'nin en guclu yonu
