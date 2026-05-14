---
name: arjancodes-dry-antipattern
description: "ArjanCodes — DRY prensibinin yanlış kullanımı: kod tekrarını azaltırken okunabilirliği kaybetme. Boolean flag antipattern ve doğru çözüm: Strategy/Policy pattern"
version: 1.0
category: software-development
source: "ArjanCodes YouTube"
tags: [python, dry, clean-code, design-patterns, antipattern, boolean-flag, strategy-pattern]
platforms: [linux, macos, windows]
---

# DRY Often Makes Your Code Worse — Doğru Kullanım

Kaynak: ArjanCodes (YouTube)

## Problem

DRY (Don't Repeat Yourself) prensibini uygularken kod tekrarını azaltmak için **boolean flag**'lerle dolu generic bir fonksiyon yazmak, kodu daha **kötü** hale getirebilir.

### Yanlış Yaklaşım

```python
def normalize_strings(items, strip_whitespace=True, lowercase=True,
                       require_at=False, split_at=False,
                       min_length=None, remove_prefix=None):
    result = []
    for item in items:
        if strip_whitespace:
            item = item.strip()
        if lowercase:
            item = item.lower()
        if require_at and '@' not in item:
            continue
        if split_at and '@' in item:
            item = item.split('@')[1]
        if min_length and len(item) < min_length:
            continue
        if remove_prefix and item.startswith(remove_prefix):
            item = item[len(remove_prefix):]
        result.append(item)
    return result
```

Sorunlar:
- 6 boolean flag → test edilecek 64 kombinasyon
- Flag'lerin etkileşimi belirsiz (ör: `require_at=False` ama `split_at=True` → hata)
- Yeni gereksinim = yeni parametre
- Okunamaz, debug'ı imkansız

### Doğru Çözüm: Policy Pattern

```python
from dataclasses import dataclass
from typing import Callable, List

@dataclass
class NormalizationPolicy:
    """Her policy tek bir sorumluluğa sahip"""
    transform: Callable[[str], str]
    validate: Callable[[str], bool] = lambda x: True

# Policy'leri tanımla
STRIP = NormalizationPolicy(transform=lambda s: s.strip())
LOWERCASE = NormalizationPolicy(transform=lambda s: s.lower())
EXTRACT_USERNAME = NormalizationPolicy(
    transform=lambda s: s.split('@')[1] if '@' in s else s,
    validate=lambda s: '@' in s
)
MIN_LENGTH_3 = NormalizationPolicy(
    transform=lambda s: s,
    validate=lambda s: len(s) >= 3
)
REMOVE_MAILTO = NormalizationPolicy(
    transform=lambda s: s.removeprefix('mailto:') if s.startswith('mailto:') else s
)

def normalize(items: List[str], policies: List[NormalizationPolicy]) -> List[str]:
    result = []
    for item in items:
        for policy in policies:
            if not policy.validate(item):
                break
            item = policy.transform(item)
        else:
            result.append(item)
    return result

# Kullanım
emails = ["  USER@EXAMPLE.COM  ", "admin@site.com"]
result = normalize(emails, [STRIP, LOWERCASE, EXTRACT_USERNAME])
# → ["user@example.com", "admin@site.com"]
```

## Avantajlar

| DRY Flag Yaklaşımı | Policy Pattern |
|-------------------|----------------|
| 6 flag = 64 olasılık | Her policy bağımsız test edilir |
| Yeni özellik = yeni parametre | Yeni özellik = yeni policy sınıfı |
| Flag interaction'ları belirsiz | Policy'ler birbirinden bağımsız |
| Tek dosya, tek fonksiyon | Modüler, genişletilebilir |

## Ne Zaman DRY Uygulanmamalı

1. Boolean flag sayısı 2'yi geçiyorsa
2. Fonksiyon parametreleri 5'i geçiyorsa
3. Flag'ler birbirini etkiliyorsa
4. Kod tekrarı < okunabilirlik kaybı
5. Farklı çağrı sitelerinde farklı flag kombinasyonları gerekiyorsa

## Özet

> DRY iyi bir prensiptir, ama **yanlış uygulandığında** kodu daha kötü yapar.
> Boolean flag'leri Policy/Strategy pattern ile değiştir.
> Kod tekrarını azaltırken **okunabilirliği koru**.
