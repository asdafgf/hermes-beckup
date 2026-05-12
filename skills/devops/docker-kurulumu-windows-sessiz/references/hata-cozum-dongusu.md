# Hata Çözüm Döngüsü — Windows Python Script Kurulum/Onarım

Bu referans, Claude.ai'dan Python scripti alıp Windows'ta çalıştırma döngüsünü belgeler.

## Standart Akış

1. **Sorunu tespit et** — hangi hata, hangi bağlam (OS, Python versiyon, yetki seviyesi)
2. **Claude.ai'a anlat** — aşağıdaki şablonu kullan
3. **Python script'ini kaydet** → `C:\Users\eymen\kiralog\<isim>.py`
4. **Çalıştır** — önce otomatik dene, olmazsa elle admin PowerShell
5. **Hata varsa** → çıktıyı Claude'a yapıştır → düzeltilmiş script al → tekrar dene
6. **Başarılı olunca** → skill olarak kaydet

## Claude.ai Şablonu

```
Windows 11'de [SORUN] için Python scripti yaz.

Durum:
- Windows 11, Python [versiyon]
- [Mevcut durum 1]
- [Mevcut durum 2]

Script gereksinimleri:
1. Admin kontrolü (değilse hata verip çıksın, UAC yükseltme DENEMESİN)
2. [Adım 2]
3. [Adım 3]
...
N. Hata yakalama + özet + exit code
N+1. input() veya bekleme OLMASIN
N+2. ANSI renk KULLANMA
N+3. Her adım [1/5] formatında olsun
```

## Bilinen Windows Kısıtları

| Sorun | Çözüm |
|-------|-------|
| `ShellExecuteW runas` kod 5 | Hermes venv'inden UAC yükseltme reddedilir |
| `Start-Process -Verb RunAs` iptal | Aynı venv kısıtı |
| `schtasks /rl HIGHEST` | Admin olmadan çalışmaz |
| foreground timeout 600s | background + notify kullan |
| ANSI renk bozuk | `colorama` veya düz print kullan |
| `input()` takılma | background process output alamaz |
