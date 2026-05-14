---
name: structured-data-extraction-llm
description: "LangChain + Groq/Llama 3 ile yapılandırılmamış metinden JSON/Pydantic çıktı alma — 3 yaklaşım: Pydantic class, JSON mode, prompt-based"
version: 1.0
category: data-science
source: https://youtu.be/qW6liOeb340
tags: [langchain, groq, llama3, structured-output, pydantic, json, data-extraction]
platforms: [linux, macos, windows]
---

# Structured Data Extraction with LLMs

Kaynak: https://youtu.be/qW6liOeb340

LangChain + Groq/Llama 3 ile unstructured text'ten yapılandırılmış veri çıkarma. 3 farklı yaklaşım.

## Kurulum

```bash
pip install langchain langchain-openai pydantic python-dotenv
```

## API Anahtari

Groq API key: https://console.groq.com

.env dosyasina: GROQ_API_KEY=...

## LLM Baslatma

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    model="llama3-8b-8192"
)

# Test
resp = llm.invoke("How are you?")
print(resp.content)
```

## Schema Tanimi (Pydantic v1)

```python
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Optional

class Person(BaseModel):
    """Information about a person"""
    name: str = Field(description="Name of the person")
    age: int = Field(description="Age of the person")
    height: Optional[str] = Field(description="Height of the person")

class People(BaseModel):
    """List of people"""
    people: List[Person] = Field(description="List of people")
```

## Yaklasim 1: Pydantic Class Output

```python
structured_llm = llm.with_structured_output(Person)
result = structured_llm.invoke("Anna is 20 years old and 5'5\" tall")
print(result)  # Person(name='Anna', age=20, height="5'5\"")

# Coklu kisi
structured_llm_people = llm.with_structured_output(People)
result = structured_llm_people.invoke(
    "Anna is 20 years old and 5'5\" tall. Sam is 25 years old and 5'10\" tall."
)
print(result)  # People(people=[Person(...), Person(...)])
```

## Yaklasim 2: JSON Mode (Prompt-based)

```python
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import SimpleJsonOutputParser

prompt = PromptTemplate.from_template("""You are an expert data parser.
Parse data from user query. Use this schema: {schema}

Respond only as JSON based on the mentioned schema strictly.
Follow JSON schema. Do not add extra fields.
If you don't know any field, set it to null.

Query: {query}""")

chain = prompt | llm | SimpleJsonOutputParser()

# Tek kisi
result = chain.invoke({
    "schema": Person.schema_json(),
    "query": "Anna is 20 years old and 5'5\" tall"
})
print(result)  # {'name': 'Anna', 'age': 20, 'height': "5'5\""}

# Coklu kisi
result = chain.invoke({
    "schema": People.schema_json(),
    "query": "Anna is 20... Sam is 25..."
})
print(result)  # {'people': [{'name': 'Anna', ...}, {'name': 'Sam', ...}]}
```

## Yaklasim 3: Simple Prompt (Parser'siz)

```python
chain_no_parser = prompt | llm  # parser yok
result = chain_no_parser.invoke({
    "schema": People.schema_json(),
    "query": "Anna is 20... Sam is 25..."
})
# Output'ta extra alanlar olabilir (description, note vb.)
# SimpleJsonOutputParser bunlari temizler
```

## Karmasik Ornek (Uzun Metin)

```python
long_text = """Anna is 20 years old, 5'5\" tall. Lives in UK.
Sam is 25 years old, 5'10\" tall. Works as marketing manager.
Donna is 35 years old, 5'6\" tall.
Jack is 45 years old, 6' tall."""

result = chain.invoke({
    "schema": People.schema_json(),
    "query": long_text
})
# Sadece name, age, height cikar — extra bilgiler atlanir
```

## Onemli Noktalar

- `with_structured_output()` direk Pydantic objesi dondurur
- `SimpleJsonOutputParser` schemaya uymayan alanlari temizler
- `schema_json()` string formatinda schema dondurur
- Parser yoksa LLM extra alan ekleyebilir
- `Optional[str]` ile zorunlu olmayan alanlar tanimlanir
