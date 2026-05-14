---
name: real-python-alter-declarative-viz
description: "Real Python Podcast 294 — Altter declarative data viz, iterators vs iterables, Django ORM decoupling, LLM scraping vs Playwright"
version: 1.0
category: software-development
source: "Real Python YouTube"
tags: [python, alter, data-visualization, declarative, django, orm, iterators, web-scraping, llm, playlist]
platforms: [linux, macos, windows]
---

# Real Python Podcast #294 — Altter ve Python Derinlikleri

Kaynak: Real Python YouTube

## Altter — Declarative Data Visualization

```python
import alter as alt
import pandas as pd

df = pd.DataFrame({
    "category": ["A", "B", "C"],
    "value": [10, 20, 15]
})

# Declarative: hangi kolon hangi axis'e gitsin
chart = alt.Chart(df).mark_bar().encode(
    x="category",
    y="value",
    color="category"
).interactive()

chart.save("chart.html")
```

Avantaj: matplotlib'e gore cok daha az boilerplate. Eksen ve figur ayarlari otomatik.

## Iterator vs Iterable

| Iterable | Iterator |
|----------|----------|
| `__iter__()` donduren her sey | `__next__()` olan nesne |
| List, tuple, dict, str, set | Generator, file object |
| Her seferinde yeni iterator dondurur | Bir kere tuketilir |

```python
# Iterable
lst = [1, 2, 3]
for x in lst: pass  # calisir
for x in lst: pass  # tekrar calisir

# Iterator
gen = (x*2 for x in [1,2,3])
for x in gen: pass  # calisir
for x in gen: pass  # BOS! iterator tukendi
```

## Django ORM Decoupling

Is mantigi (business logic) ORM'den ayir:

```python
# KOTU: ORM controller icinde
def create_order(user_id, items):
    user = User.objects.get(id=user_id)
    order = Order(user=user)
    order.save()

# IYI: Service layer
class OrderService:
    def __init__(self, user_repo, order_repo):
        self.user_repo = user_repo
        self.order_repo = order_repo
    
    def create_order(self, user_id, items):
        user = self.user_repo.get(user_id)
        order = self.order_repo.create(user=user)
        return order
```

## LLM Web Scraping vs Playwright

| Yaklasim | Artisi | Eksisi |
|----------|--------|--------|
| LLM scraping | HTML parse gerektirmez, dogal dil | Yavas, pahali, halusinasyon |
| Playwright | Hizli, guvenilir, DOM bilgisi | Sayfa yapisi bilgisi gerek |

Karar: sayfa basina maliyet onemliyse Playwright, esnek formatta veri lazimsa LLM.
