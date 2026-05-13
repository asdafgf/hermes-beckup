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
| 4 | `process_item()` | Kaynak etiketi + zaman damgası ekler, normal dict cache |
| 5 | `run_pipeline()` | Tüm adımları sırayla çalıştırır |

## Özellikler
- Bellek dostu (lazy generator, tüm veriyi belleğe almaz)
- Bağımlılık yok (Supabase/httpx kurulu değilse mock mod)
- Normal dict ile basit cache (WeakValueDictionary dict/tuple objelerini weakref olarak tutamaz)
- Exponential backoff ile hata yönetimi

## Pitfall'lar

- **WeakValueDictionary dict/tuple kabul etmez** — `weakref.WeakValueDictionary` içinde saklanan `dict` veya `tuple` objeleri `TypeError: cannot create weak reference to 'dict' object` hatası verir. Kullanılacaksa `object` wrapper kullan veya normal `dict`'e düş.
- **process_item() return tipi dict olmalı** — tuple dönerse, tip uyuşmazlığı olur. `{"source", "timestamp", "payload"}` formatını koru.
- **Supabase bağlantısı kurulamazsa mock mod** — bu durumda 5 mock satır üretilir. Eğer mock yerine gerçek Supabase testi isteniyorsa `.env` dosyasındaki `SUPABASE_URL` ve `SUPABASE_KEY` kontrol edilmeli.
