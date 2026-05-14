---
name: corey-schafer-fastapi-docker-cloudrun
description: "Corey Schafer — FastAPI uygulamasini Docker + Google Cloud Run + Neon Postgres ile deploy etme"
version: 1.0
category: software-development
source: "Corey Schafer YouTube"
tags: [fastapi, docker, cloud-run, google-cloud, postgres, neon, deployment]
platforms: [linux, macos, windows]
---

# FastAPI Docker + Google Cloud Run

Kaynak: Corey Schafer YouTube

## Genel Bakis

FastAPI uygulamasini Docker + Cloud Run + Neon Postgres'e deploy et. Auto-scaling, managed SSL, scale to zero.

## Dockerfile

```
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## main.py

```python
from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os

app = FastAPI()
engine = create_engine(os.getenv("DATABASE_URL"))

@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "healthy"}
```

## Deploy

```bash
gcloud builds submit --tag gcr.io/PROJECT/app
gcloud run deploy app --image gcr.io/PROJECT/app \
  --platform managed --allow-unauthenticated \
  --set-env-vars "DATABASE_URL=postgresql://..."
```

## Avantaj

VPS'te Nginx + systemd elle yonetilir. Cloud Run'da her sey otomatik.
