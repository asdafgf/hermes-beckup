# Eymen Sabah Özeti — 4 Kategorili Prompt (Güncel)

Bu prompt Eymen için özelleştirilmiştir. Her sabah 08:15'te çalışır. **Günde 1 kez** — gün içinde tekrar mesaj gelmez.

## Ayarlar

- **Zamanlama:** `15 8 * * *` (her gün 08:15 — 08:00'den 08:15'e çekildi, nedeni İstanbul 08:30 ve Kayseri 09:00 bültenleriyle çakışmayı önlemek)
- **Teslimat:** `origin,all` (Hem bu sohbete hem Telegram Home kanalına)
- **Tools:** `["web"]` (sadece web_search)
- **Kategoriler:** 4 (Son Dakika + X gündemi + Türkiye + Dünya)
- **Haber sayısı:** Son Dakika (değişken) + X (15) + Türkiye (20) + Dünya (25) = ~60 madde
- **Dil:** Türkçe (yabancı kaynaklar → Türkçe çeviri)
- **Gün içinde tekrar:** HAYIR — sadece sabah 08:15'te

## Kullanıcı Tercihleri

- "Eymen, günaydın! ☀️" ile başlasın
- Her haber MAX 1 cümle
- Kaynak belirt (site adı parantez içinde)
- 5 alt kategori: Finans, Eğitim, Sağlık, Teknoloji, Diğer
- Gram altın canlı fiyatı mutlaka olsun (bigpara/altin.in)
- Tüm haberler son 24-36 saat olmalı

## Prompt Metni (kopyala-yapıştır)

```markdown
BUGÜNÜN SABAH ÖZETİNİ HAZIRLA — 3 ana kategorili, kapsamlı, özlü.

Şu an saat yaklaşık 08:00. web_search kullanarak bilgi topla. Her kategori için 4-5 ayrı arama yap (farklı kaynakları görmek için).

**KRİTİK:** 
- Tüm aramalarda "today", "latest", "bugün", "son dakika" gibi güncellik anahtar kelimeleri KULLAN.
- Her haberin GÜNCEL olduğundan emin ol. Eski haberleri (2+ gün önce) dahil etme.
- Tarih, dünkü veya bugünkü tarih olmalı.

**ÖNEMLİ:** Yabancı kaynaklardan (İngilizce siteler) aldığın haberleri **Türkçe'ye çevirerek** ver.

---

## KATEGORİ 1 — X/TWITTER GÜNDEMİ (En çok konuşulan 15 başlık)

Şu aramaları yap:
- "X trending Turkey today May 2026" site:trends24.in
- "trending topics Turkey Twitter today"
- "viral tweet Turkey bugün"
- "Turkey most discussed Twitter today May"
- "X Turkey trends hot topics now"

Son 24 saatte X'te en çok konuşulan 15 konuyu/tweet başlığını listele. Her biri 1 cümle, öz.

---

## KATEGORİ 2 — TÜRKİYE GÜNDEMİ (20 haber, TAMAMI GÜNCEL)

Her başlık altında 4-5 haber olacak şekilde dağıt. Toplam 20 haber. **Tüm haberler son 24 saat içinde yayınlanmış olmalı.**

**📊 Finans (Gram Altın + Borsa + Döviz)** (4-5 haber)
• Gram altın fiyatı için şu aramaları yap:
  - "gram altın fiyatı canlı" site:bigpara.hurriyet.com.tr
  - "gram altın kaç TL bugün" site:altin.in
  - "canlı gram altın fiyatı Mayıs 2026"
  - "dolar TL kuru bugün" site:bigpara.hurriyet.com.tr
  - "Borsa İstanbul son durum bugün"
• Gram altın fiyatını mutlaka belirt (alış ve satış).

**📚 Eğitim** (4-5 haber)
• "MEB son dakika bugün", "YKS 2026 haberleri", "eğitim gündemi bugün"

**🏥 Sağlık** (4-5 haber)
• "sağlık bakanlığı son dakika bugün", "ilaç hastane haberleri"

**💻 Teknoloji** (3-4 haber)
• "yerli teknoloji güncel haber" site:webrazzi.com, "Türkiye teknoloji haberi bugün"

**📌 Diğer** (3-4 haber)
• Siyaset, spor, kültür-sanat, hava durumu, ulaşım

---

## KATEGORİ 3 — DÜNYADAN HABERLER (25 haber, TÜRKÇE ÇEVİRİ, GÜNCEL)

Her başlık altında 5-6 haber olacak şekilde dağıt. Toplam 25 haber. **Tüm haberler son 36 saat içinde yayınlanmış olmalı.**

**💰 Finans** (5-6 haber)
• "gold price today May 11 2026", "oil price latest today", "global stock market today"
• Gram altın ons fiyatını mutlaka kontrol et

**📚 Eğitim** (3-4 haber)
• "global education news May 2026 today"

**🏥 Sağlık** (4-5 haber)
• "new medicine breakthrough May 2026", "WHO latest news today", "global health today"

**💻 Teknoloji** (5-6 haber)
• "AI latest news today May 2026", "technology breakthrough today", "tech news today"

**📌 Diğer** (4-5 haber)
• "world news today May 2026", "geopolitics latest today", "Turkey international news today"

---

## ÇIKTI FORMATI

📱 **X'TE GÜNDEM — En Çok Konuşulan 15 Başlık**
1. 🔥 ...
2. ...
...
15. ...

---

🇹🇷 **TÜRKİYE GÜNDEMİ — 20 Haber**

**📊 Finans (Gram Altın + Borsa + Döviz)**
1. Gram altın alış: ... TL, satış: ... TL (kaynak)
2. ...
...

**📚 Eğitim**
...

**🏥 Sağlık**
...

**💻 Teknoloji**
...

**📌 Diğer**
...

---

🌍 **DÜNYADAN HABERLER — 25 Haber (Türkçe çeviri)**

**💰 Finans**
1. ...
...

**📚 Eğitim**
...

**🏥 Sağlık**
...

**💻 Teknoloji**
...

**📌 Diğer**
...

---

ÖNEMLİ KURALLAR:
- TÜM haberler GÜNCEL olmalı (son 24-36 saat)
- Gram altın fiyatı canlı veri kaynağından alınmalı
- TÜM yabancı kaynak haberleri TÜRKÇE'ye çevrilmiş olmalı
- Her haber MAX 1 cümle, öz ve bilgilendirici
- Kaynak belirt (site adı parantez içinde)
- Başta "Eymen, günaydın! ☀️" yaz
```

## Değişiklik Geçmişi

| Tarih | Değişiklik |
|---|---|
| 2026-05-11 | X platformu 3. kategori olarak eklendi |
| 2026-05-11 | Gram altın canlı veri kaynağı eklendi (bigpara/altin.in) |
| 2026-05-11 | Tarih/güncellik filtresi eklendi |
| 2026-05-11 | 20+25 haber formatına geçildi |
| 2026-05-11 | `deliver: origin,all` olarak değiştirildi (çift yönlü teslimat) |
| 2026-05-11 | Saat 08:00 → 08:15 olarak değişti |
| 2026-05-11 | 3 kategori → 4 kategori (Son Dakika eklendi) |
| 2026-05-11 | 5 dk'da bir son-dakika-akisi cronjob'u kaldırıldı, 08:15'e entegre edildi |
