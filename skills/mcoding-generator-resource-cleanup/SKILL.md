---
name: mcoding-generator-resource-cleanup
description: "mCoding — Python generator'larda kaynak temizleme (with, try/finally, async generator). GC close() otomatik çağrılması, break/exception durumunda cleanup garantisi"
version: 1.0
category: software-development
source: "mCoding YouTube"
tags: [python, generators, async, resource-management, try-finally, context-manager, garbage-collection]
platforms: [linux, macos, windows]
---

# Python Generator Resource Cleanup (mCoding)

Kaynak: mCoding (James Murphy)

## Problem

Generator'lar bir kaynağı (DB transaction, lock, file) yönettiğinde, generator **tamamlanmadan** durursa (break, exception) kaynak temizlenir mi?

### Doğru Cevap: EVET

```python
class Resource:
    def __init__(self, name):
        self.name = name
    def cleanup(self):
        print(f"Cleanup: {self.name}")

def managed_generator():
    resource = Resource("my-resource")
    try:
        with resource:  # veya try/finally
            yield 0
            yield 1
            yield 2
    finally:
        resource.cleanup()  # Her durumda çalışır

# Normal kullanım
for val in managed_generator():
    print(f"Got: {val}")
    if val == 1:
        break  # Generator yarıda kesildi!
# Output: 0, 1, Cleanup: my-resource  ← hala temizlenir!
```

## Neden Çalışır?

Generator **garbage collect** edildiğinde, Python otomatik olarak `.close()` metodunu çağırır.

`.close()` → GeneratorException fırlatır → Generator içindeki finally bloğu çalışır.

```python
gen = managed_generator()
print(next(gen))  # 0
print(next(gen))  # 1
# gen referansı silinir veya scope dışı
del gen  # → .close() çağrılır → cleanup mesajı gelir
```

## Async Generator

```python
import asyncio

async def async_managed():
    try:
        yield 0
        yield 1
    finally:
        await cleanup()  # asenkron temizlik

async def main():
    async for val in async_managed():
        print(f"Got: {val}")
        break  # async generator da temizlenir

asyncio.run(main())
```

## Önemli Noktalar

| Durum | Cleanup? |
|-------|----------|
| `for` döngüsü normal biter | ✅ |
| `break` ile çıkılır | ✅ (GC close ile) |
| Exception fırlatılır | ✅ |
| Generator manuel `del` edilir | ✅ (hemen) |
| Generator scope dışına çıkar | ✅ (GC toplarken) |
| `async for` break | ✅ |
| **CPython dışı implementasyonlar** | ⚠️ GC farklı çalışabilir |

## Best Practice

```python
# ✅ DOĞRU: context manager + try/finally
def get_data():
    conn = database.connect()
    try:
        for row in conn.query():
            yield row
    finally:
        conn.close()

# VEYA contextlib
from contextlib import contextmanager

@contextmanager
def managed_resource():
    res = acquire()
    try:
        yield res
    finally:
        release(res)

# Kullanım
with managed_resource() as res:
    res.do_work()
```

## Uyarı

```python
# ⚠️ DİKKAT: with inside generator
def risky():
    with open("file.txt") as f:
        yield from f
    # with bloğu yield'den sonra devam eder
    # break yapılırsa, with __exit__ hala çağrılır
```

> **Özet:** Python generator'ları için resource cleanup **garanti altındadır** — break, exception veya GC hepsi finally bloğunu tetikler. Async generator'lar da aynı garantiyi sağlar.
