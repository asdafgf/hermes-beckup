---
name: olasilik-oncelik-ilkesi
description: "Tüm işlemlerde temel düşünce: Her olasılık gerçekliğe dönüşme potansiyeli taşır. Hiçbir olasılık atlanmaz, test edilir. Karar verirken ilk sorgulanan olgu budur."
version: 1.0
author: q
category: decision-making
tags: [olasilik, priorite, test-et, dene, karar]
related_skills: [systematic-debugging, hata-cozum-dongusu, hata-cozum-ollama, nexus-core]
---

# Olasılık Öncelik İlkesi

## 🔑 Temel Kural

**Her olasılık, gerçekliğe dönüşme ihtimali taşır. Bu ihtimal asla göz ardı edilmez — her olasılık denenmelidir.**

Bu, tüm karar verme sürecinin **ilk düşünülen olgusu** olmalıdır. Bir karar verirken sırasıyla:

1. **Olasılıkları listele** — akla gelen tüm ihtimalleri yaz
2. **Hiçbirini eleme** — "bu çalışmaz", "bu saçma", "bu ihtimal düşük" diye atlama
3. **Dene** — her olasılığı sırayla test et
4. **Sonuç al** — çalışanı bul, çalışmayanı kaydet (gelecekte işe yarayabilir)

## 🧠 Zihinsel Model

```text
Başarı = (Düşük ihtimal) × (Denemeye devam etme) × (Çok sayıda olasılık)

Formül basit: Ne kadar çok olasılık denersen, gerçekliğe dönüşme şansı o kadar artar.
```

## ⚙️ Uygulama

### Hata Çözümünde
```python
# YANLIŞ — sadece en olası 1-2 sebebi kontrol etmek
sorun = "qwen cevap vermiyor"
cozum1 = "timeout"  # kontrol et, olmazsa pes et

# DOĞRU — tüm olasılıkları sırayla dene
sorun = "qwen cevap vermiyor"
olasiliklar = [
    "timeout",
    "model stuck/Stopping...",
    "ollama servisi çöktü",
    "port 11434 kapalı",
    "RAM yetmedi",
    "curl hatalı syntax",
    "json payload hatalı",
    "lock dosyası kilitli",
    "arkaplan process çakışması"
]
for olasilik in olasiliklar:
    test_et(olasilik)   # her birini dene, hiçbirini atlama
```

### Kod Yazarken
```python
# YANLIŞ: "En mantıklı yol bu, direkt uygula"
def coz():
    return en_mantikli_yol()

# DOĞRU: "3 farklı yaklaşım dene, hangisi çalışırsa"
def coz():
    yaklasimlar = [yol_A, yol_B, yol_C]
    for y in yaklasimlar:
        if y() == "basarili":
            return y
```

### Planlarken
```text
❌: "Bu yöntem en verimli, direkt bunu yap."
✅: "3 yöntem var. A en hızlı, B en güvenilir, C en esnek.
    Hangisi gerçekliğe dönüşecek bilmiyorum — hepsini dene."
```

## 💥 Kritik İstisna: Güvenlik ve Etik

- **Siber güvenlik öğrenimi:** Olasılıklar teorik olarak tartışılır, gerçek sistemlerde test edilmez. Kullanıcı aksini söylemedikçe sadece eğitim/simülasyon ortamında denenir.
- **Zarar verme potansiyeli olan olasılıklar:** Kullanıcıya danış, onay almadan deneme.
- **Yasal sınır:** "Denenebilir" olması "denenmeli" olduğu anlamına gelmez. Yasal ve etik çerçeveyi kullanıcı belirler.

## 📋 Örnek Vakalar

### Vaka 1: Qwen hata veriyor
- Olasılık A: Timeout → çözüm: timeout 120sn → **dene** ✅ çalıştı
- Olasılık B: Daha hızlı model kullan → **dene** ⚡ daha hızlı

### Vaka 2: Port çakışması
- Olasılık A: taskkill ile ollama'yı öldür → **dene**
- Olasılık B: Port 11435'te başka serve başlat → **dene**
- Olasılık C: Windows yeniden başlat → **dene**

### Vaka 3: Script syntax hatası
- Olasılık A: Parantezleri kontrol et → **dene**
- Olasılık B: $[] vs $() syntax'ı → **dene**
- Olasılık C: UTF-8 encoding sorunu → **dene**

## 🔄 Günlük Kullanım

Her karar anında kendine sor:
```
"Bu olasılığı denemeden geçersem, gerçekliğe dönüşme şansını yok mu ediyorum?"
```

Cevap "Evet" ise → **DENE.**
Cevap "Belki" ise → **YİNE DE DENE.**
Cevap "Hayır" (güvenlik/etik ihlali) ise → **kullanıcıya danış.**
