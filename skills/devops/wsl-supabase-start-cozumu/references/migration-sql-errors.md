# SQL Migration Errors Encountered with `npx supabase start`

## Hata: `current_date` PostgreSQL Keyword Çakışması

```
ERROR: syntax error at or near "current_date" (SQLSTATE 42601)
At statement: 2
CREATE OR REPLACE FUNCTION add_business_days(start_date DATE, num_days INT)
...
  current_date DATE := start_date;
```

### Sebep
`current_date` PostgreSQL'de **reserved keyword**'dür (built-in fonksiyon). Değişken adı olarak kullanılamaz.

### Çözüm
Değişken adını `cur_date` veya `current_day` olarak değiştir:

```sql
-- ❌ HATALI
DECLARE
  current_date DATE := start_date;
BEGIN
  WHILE days_added < num_days LOOP
    current_date := current_date + INTERVAL '1 day';
  END LOOP;
  RETURN current_date;
END;

-- ✅ DÜZELTİLMİŞ
DECLARE
  cur_date DATE := start_date;
BEGIN
  WHILE days_added < num_days LOOP
    cur_date := cur_date + INTERVAL '1 day';
  END LOOP;
  RETURN cur_date;
END;
```

## Diğer Olası PostgreSQL Keyword Çakışmaları

| Değişken Adı | PostgreSQL Keyword | Önerilen Alternatif |
|-------------|-------------------|-------------------|
| `current_date` | ✅ built-in | `cur_date`, `today` |
| `current_time` | ✅ built-in | `cur_time` |
| `current_timestamp` | ✅ built-in | `cur_ts` |
| `user` | ✅ built-in | `current_user_id` |
| `end` | ✅ reserved | `end_val`, `end_date` |
| `start` | ✅ reserved | `start_val`, `start_date` |
| `status` | ✅ reserved (SQL:2008) | `status_val` |
| `type` | ✅ reserved | `type_val`, `item_type` |
| `level` | ✅ reserved | `lvl`, `severity` |
| `group` | ✅ reserved | `group_name`, `grp` |

## Genel Çözüm: Tüm Migration'ları Kontrol Et

```bash
# WSL içinde tüm migration'larda reserved keyword ara
wsl -d Ubuntu -u root -- bash -c "
  cd /root/kiralog
  for f in supabase/migrations/*.sql; do
    echo \"=== \$f ===\"
    grep -ni 'current_date\|current_time\|current_timestamp\|declare.*user\|declare.*end\|declare.*start\|declare.*status\|declare.*type\|declare.*level\|declare.*group' \$f || true
  done
"
```

## npx supabase start Akışı

`npx supabase start` şu adımları çalıştırır:

1. **Docker imajlarını indir** (first run only — 7+ imaj, ~200 MB toplam)
2. **PostgreSQL container'ını başlat**
3. **Schema'yı initialse et** (supabase/templates/ içinden)
4. **Migration'ları sırayla uygula** (supabase/migrations/001, 002, 003...)
5. **Seed data** (supabase/seed.sql varsa)
6. **Tüm servisleri başlat** (Kong, GoTrue, Realtime, Storage, PostgREST, Studio)

Herhangi bir adımda hata alınırsa `--debug` ile yeniden çalıştır:
```bash
npx supabase start --debug
```
