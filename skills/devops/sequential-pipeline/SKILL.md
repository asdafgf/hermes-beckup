---
name: sequential-pipeline
description: >-
  Sıralı veri işleme pipeline'ı. AST-Aktör-Eleştirmen mimarisi.
  Supabase kayıtları, JSONL dosyaları ve API çağrılarını sırayla işler.
  Lazy generator, weakref cache, exponential backoff ile yeniden deneme.
---

# Sequential Processing Pipeline

## Ne Zaman Kullanılır
- Supabase'den batch halinde veri çekip işlemen gerekiyor
- JSONL dosyasını satır satır işlemen gerekiyor
- API çağrılarını sırayla, hata yönetimiyle yapman gerekiyor
- Tüm adımları tek bir pipeline'da birleştirmen gerekiyor

## Kullanım

```bash
cd /c/Users/eymen/kiralog
python sequential_pipeline.py
```

## Mimari: AST-Aktör-Eleştirmen

- **AST (Abstract Syntax Tree):** Pipeline adımlarının sıralı yapısı
- **Aktör:** Her generator (supabase_records, file_records, api_records) bir aktör
- **Eleştirmen:** process_item fonksiyonu ile dönüşüm + GC notları

## 5 Bileşen

| # | Bileşen | Açıklama |
|---|---------|----------|
| 1 | `supabase_records()` | Lazy paginated generator, batch boyutu 100 |
| 2 | `file_records()` | JSONL dosyasını satır satır okur |
| 3 | `api_records()` | Sıralı API çağrısı, 3 retry, exponential backoff |
| 4 | `process_item()` | Kaynak etiketi + zaman damgası ekler, weakref cache |
| 5 | `run_pipeline()` | Tüm adımları sırayla çalıştırır |

## Özellikler
- Bellek dostu (lazy generator, tüm veriyi belleğe almaz)
- Bağımlılık yok (Supabase/httpx kurulu değilse mock mod)
- WeakValueDictionary ile otomatik GC
- Exponential backoff ile hata yönetimi
