---
name: hata-cozum-dongusu
description: "Standart hata çözme döngüsü: sorunu Claude.ai'a sor, Python kodunu al, çalıştır, hata varsa Claude'a geri gönder, düzeltilmiş kodla değiştir, tekrar çalıştır. Her tür Windows/sistem sorunu için uygulanabilir."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [debugging, workflow, problem-solving, python]
    related_skills: [systematic-debugging, python-oto-debug-dongusu]
---

# Hata Çözüm Döngüsü (Claude.ai + Python)

## Genel Bakış

Windows'ta karşılaşılan herhangi bir sistem sorununu çözmek için standartlaştırılmış bir yöntem. Claude.ai'a sorunu anlat, aldığın Python kodunu çalıştır, hata alırsan hata çıktısını Claude'a yapıştır, düzeltilmiş kodu al, değiştir, tekrar çalıştır. Bu döngü sorun çözülene kadar devam eder.

## Ne Zaman Kullanılır

- Docker, WSL, Node.js, Python, Scoop, winget gibi araç kurulumlarında sorun çıkınca
- Windows sistem hatalarında (servis başlamıyor, path bulunamıyor, yetki hatası)
- Bilinmeyen bir hata ile karşılaşıldığında ve çözümü internette hemen bulunamadığında
- Manuel adımlar gerektiren karmaşık kurulumlar için otomatik script gerektiğinde
- **Kullanma:** Basit hatalar için (typo, yanlış dosya yolu) doğrudan düzelt, bu döngüye girme

## Adımlar

### 1. Sorunu Tanımla

Hata mesajını, beklentiyi ve ortamı (OS, versiyonlar) netleştir:
```
Hedef: Docker Desktop'ı sessiz kur
Ortam: Windows 11, Docker CLI yüklü (scoop), engine bağlanamıyor
Hata: "failed to connect to the docker API at npipe:////./pipe/docker_engine"
```

### 2. Sorunu Claude.ai'a Sor (markopasa_@hotmail.com)

Claude.ai sohbetinde şu kalıbı kullan:
```
[Hedef] yapmak istiyorum.
Ortam: Windows 11, [araçlar yüklü/değil]
Karşılaştığım hata: [hata mesajı]

Bana bu sorunu çözecek bir Python script'i yaz.
Script şunları yapmalı:
- [madde madde beklenen adımlar]
- Yönetici yetkisi gerekiyorsa kontrol etsin
- Her adımda [INFO]/[OK]/[HATA] çıktısı versin
- Hata durumunda script durmasın, devam etsin
```

### 3. Python Kodunu Al ve Kaydet

Claude.ai'ın verdiği Python kodunu al, proje klasörüne `.py` olarak kaydet:
```bash
cd /c/Users/eymen/kiralog/
# Kodu yapıştır: dosya_adi.py
python dosya_adi.py
```

### 4. Çalıştır ve Çıktıyı İzle

- Script çalışırken çıktıyı takip et
- Başarılı olursa ✅ işlem bitti
- Hata alırsan hata çıktısını kopyala

### 5. Hata Çıktısını Claude.ai'a Yapıştır

Claude.ai sohbetine hatayı yapıştır:
```
Script çalıştı ama şu hatayı aldım:

[hata çıktısı - tümü]

Bunu düzeltilmiş Python script'ini ver.
```

### 6. Düzeltilmiş Kod ile Değiştir ve Tekrar Çalıştır

Claude.ai'ın verdiği düzeltilmiş kod ile eski `.py` dosyasını değiştir:
```bash
# Eski dosyayı sil, yeni kodu yapıştır
python dosya_adi.py
```

### 7. Döngüyü Tekrarla

Hata kalmayana kadar 4-5-6 adımlarını tekrarla.

## Yaygın Pitfall'lar

1. **Claude.ai'a eksik bilgi vermek** — OS, versiyon, hata mesajının TAMAMI lazım
2. **Python script'i foreground'da timeout** — 600s üstü işlemlerde `background=True` + `notify_on_complete=True` kullan (Eymen ön planda beklemez)
3. **Yönetici yetkisi ([WinError 740])** — Docker, WSL, Hyper-V, servis kurulumları admin ister. Çözüm: script'in kendini UAC ile yükseltmesi (`ctypes.windll.shell32.ShellExecuteW(None, "runas", ...)`). Kullanıcıya "admin olarak çalıştır" deme — script kendisi halletsin.
4. **Birden çok kod almadan doğrudan çalıştırmamak** — İlk deneme genelde hatalı olur
5. **Hata çıktısını kısaltmak** — Claude'a tam çıktıyı yapıştır, özetleme
6. **Uzun süren işlemlerde notify_on_complete** — Kurulum >5 dk sürüyorsa background + notify kullan
7. **ANSI renk kodları Windows'ta bozuk çıktı** — Script'te `\033[` gibi ANSI escape kodları kullanma, düz metin çıktı (tag bazlı) tercih et
8. **capture_output=True iken kurulum output'u gecikebilir** — Uzun işlemlerde `stdout=subprocess.DEVNULL` ile detach et, progress'i print ile ayrıca raporla
9. **Background process'e UAC penceresi bağlanamaz** — UAC gereken script'leri background değil, direkt `terminal` ile admin olarak başlat

## Doğrulama Listesi

- [ ] Sorun net bir şekilde tanımlandı mı?
- [ ] Claude.ai'a eksiksiz bilgi verildi mi?
- [ ] Python script'i kaydedildi mi?
- [ ] Script çalıştırıldı ve çıktı alındı mı?
- [ ] Hata varsa çıktı Claude.ai'a yapıştırıldı mı?
- [ ] Düzeltilmiş kod ile script güncellendi mi?
- [ ] Sorun çözülene kadar döngü tekrarlandı mı?
- [ ] Çözüm skill olarak kaydedildi mi? (öğrenilen ders)

## Tek Seferlik Kullanım Kalıbı

Claude.ai'a şu şablonu yapıştır:

```
[HEDEF] yapmak istiyorum.
Windows 11 kullanıyorum.
Mevcut durum: [yüklü araçlar, versiyonlar]
Aldığım hata:
```
[hata çıktısı]
```
Bana bu sorunu çözecek bir Python script'i yaz.
Script:
1. Yönetici yetkisini kontrol etsin, yoksa uyarı versin
2. Her adımda [INFO], [OK], [HATA] etiketli çıktı versin
3. Hatalarda script durmasın, devam etsin (warn + geç)
4. timeout değerleri yeterince yüksek olsun
5. Renkli terminal çıktısı kullansın
```
