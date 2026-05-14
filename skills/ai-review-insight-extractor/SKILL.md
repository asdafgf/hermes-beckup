---
name: ai-review-insight-extractor
description: "Gemini 2.5 Flash + LangChain ile ürün yorumlarından pros/cons/kilit temalar çıkarma — yapılandırılmış çıktı (Pydantic), toplu analiz, CSV çıktısı"
version: 1.0
category: data-science
source: https://youtu.be/szAZwt4V1X8
tags: [gemini, langchain, review-analysis, nlp, structured-output, pydantic, csv]
platforms: [linux, macos, windows]
---

# AI Review Insight Extractor

Kaynak: https://youtu.be/szAZwt4V1X8

Gemini 2.5 Flash ile yapılandırılmış çıktı kullanarak ürün yorumlarından pros, cons, kilit temalar ve özet çıkarma.

## Kurulum

pip install pandas python-dotenv langchain-google-genai

## API Anahtari

.env dosyasina GOOGLE_API_KEY ekle. API key: https://aistudio.google.com

## CSV Formati

gadget_reviews.csv:
```
review
"Amazing sound quality, deep bass, very comfortable"
"Battery life is poor, charges slowly, sound is good"
```

## Tam Kod

```python
import pandas as pd
from dotenv import load_dotenv
from typing import Annotated, Optional
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class ReviewSchema:
    key_themes: Annotated[list[str], "Extract key ideas or themes present in the review"]
    summary: Annotated[str, "Summarize in 2-3 sentences"]
    pros: Annotated[Optional[list[str]], "Positive aspects"]
    cons: Annotated[Optional[list[str]], "Negative aspects"]

structured_model = model.with_structured_output(ReviewSchema)

df = pd.read_csv("gadget_reviews.csv")
reviews = df["review"].dropna().tolist()
print(f"Toplam {len(reviews)} yorum")

processed = []
for idx, text in enumerate(reviews, 1):
    print(f"İşleniyor: {idx}/{len(reviews)}")
    r = structured_model.invoke(text)
    processed.append({"key_themes": r.key_themes, "summary": r.summary,
                       "pros": r.pros or [], "cons": r.cons or []})

all_themes = [t for r in processed for t in r["key_themes"]]
all_pros = [p for r in processed for p in r["pros"]]
all_cons = [c for r in processed for c in r["cons"]]

agg_prompt = f"""Themes: {all_themes}
Pros: {all_pros}
Cons: {all_cons}
Generate: 1) global summary, 2) collective pros, 3) collective cons, 4) final conclusion"""

final = model.invoke(agg_prompt)
print("\nFINAL SUMMARY:")
print(final.content)

pd.DataFrame(processed).to_csv("processed_reviews.csv", index=False)
print("processed_reviews.csv kaydedildi.")
```

## Output CSV

key_themes, summary, pros, cons sutunlarindan olusur. Optional alanlar bossa [] gelir.

## Ipuclari

- Dropna() ile bos satirlari temizle
- Gemini 2.5 Flash 1M token limiti var
- Model adini degistirerek GPT-4o-mini de kullanilabilir
