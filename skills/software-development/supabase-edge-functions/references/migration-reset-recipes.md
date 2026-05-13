# Migration Reset Debugging Recipes

## Scenario: npx supabase start → "relation X already exists"

### Symptom
```
ERROR: relation "users" already exists (SQLSTATE 42P07)
```
Supabase'in iç schema'sında `users` tablosu bulunamıyor ama migrasyon çalıştırılınca hata alınıyor.

### Root Cause
Volume'lar `supabase stop --no-backup` ile silinmiş olsa bile Docker Compose volume'ları `docker system prune --volumes` ile temizlenmiyor veya migration seed'den gelen bir tablo kolon çakışması yaşıyor. En yaygın sebep: migrasyon SQL'inde `IF NOT EXISTS` olmaması.

### Step-by-step Fix

**1. Stop + temizle**
```bash
npx supabase stop --no-backup
docker system prune --volumes -f
```

**2. Migrasyon SQL'inde IF NOT EXISTS kontrolü**
```bash
grep "^CREATE TABLE " supabase/migrations/*.sql
```
Çıktıdaki her satır `CREATE TABLE IF NOT EXISTS` ile başlamalı. Eksik varsa düzelt.

**3. Toplu düzeltme (dikkatli)**
```bash
sed -i 's/^CREATE TABLE /CREATE TABLE IF NOT EXISTS /g' supabase/migrations/*.sql
# Hemen kontrol et:
grep "IF NOT EXISTS IF NOT EXISTS" supabase/migrations/*.sql
# Varsa düzelt:
sed -i 's/IF NOT EXISTS IF NOT EXISTS/IF NOT EXISTS/g' supabase/migrations/*.sql
```

**4. Seed dosyasını da kontrol et**
```bash
grep "^CREATE TABLE " supabase/seed/*.sql 2>/dev/null
```
Seed'de zaten `IF NOT EXISTS` olmalı (genelde vardır, ama kontrol et).

**5. Temiz başlat**
```bash
npx supabase start
```

### Known Cases

| Proje | Hata | Çözüm |
|---|---|---|
| KiraLog 2026-05 | `relation "users" already exists` | 001_initial.sql'de 9 CREATE TABLE'ın hiçbirinde IF NOT EXISTS yoktu. `sed` ile toplu düzeltildi. İlk denemede `patch`+`sed` çakışmasıyla ikileme oluştu, ikinci denemede düzeldi. |
