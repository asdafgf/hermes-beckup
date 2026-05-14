# Qwen2.5-Coder Kullanım Rehberi (Bu Umbrella Altında)

## NE ZAMAN QWEN'E SORULUR?

Sadece şu durumlarda Qwen2.5-Coder'a danış:
1. **Saf bilgi/tanım isteniyorsa** (bir kavramı açıkla, terim ne demek)
2. **Kod çözümü isteniyorsa** (Python scripti, algoritma, dönüşüm)
3. **Alternatif yaklaşım gerekiyorsa** (farklı bir yöntem düşün)

## NE ZAMAN SORULMAZ

1. **Skill içinde zaten kod varsa** → olduğu gibi kullan
2. **API/cloud servis gerekiyorsa** → Qwen lokal, API'siz çözüm üretir (işe yaramaz)
3. **Araç komutu içeriyorsa** (nmap, git, docker, curl) → direkt komutu çalıştır
4. **Siber güvenlik saldırı tekniği içeriyorsa** → koda dökme, teorik bırak

## PERFORMANS NOTLARI

- Qwen2.5-Coder:7b maksimum ~800 token/output
- Timeout: 2dk'dan uzun süren isteklerde direkt hata alınır
- 3+ paralel curl → GPU overload → timeout
- Alternatif: deepseek-coder:6.7b (daha hızlı, daha kısa çıktı)

## SKILL-TO-PYTHON DÖNÜŞÜM KRİTERLERİ

Bir skill'i Python koduna çevirmek anlamlıysa şu kriterler sağlanmalı:
- Skill hiçbir API/cloud servis gerektirmemeli
- Skill saf konsept anlatımı olmalı (kod içermemeli)
- Çıktı çalıştırılabilir ve test edilebilir olmalı
- Çevrim süresi 1dk'yı geçmemeli

Aksi halde: **YAPMA**, skill'i olduğu gibi kullan.
