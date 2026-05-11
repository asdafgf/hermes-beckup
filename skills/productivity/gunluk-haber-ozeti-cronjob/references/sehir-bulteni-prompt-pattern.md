# Şehir Bülteni Prompt Pattern

Bu pattern, belirli bir şehir için günlük bülten oluşturan cronjob'larda kullanılır. `gunluk-haber-ozeti-cronjob` skill'inin alt türüdür.

## Ne Zaman Kullanılır

- Kullanıcı belirli bir şehir için günlük bülten istediğinde (İstanbul, Kayseri vb.)
- Şehre özgü kaynaklardan haber toplamak gerektiğinde (valilik, emniyet, belediye, metro, savcılık)
- Kapsam: fuar/etkinlik, trafik/kaza, toplu taşıma, resmi duyurular, ilginç olaylar

## Ayarlar

- **Zamanlama:** Genel özetten sonra (08:30 İstanbul, 09:00 Kayseri gibi)
- **Teslimat:** `all` (hem kullanıcı sohbetine hem Telegram Home kanalına)
- **Tools:** `["web"]` (sadece web_search)
- **Süre:** Son 24 saat

## Şehir Bülteni İçin Prompt Şablonu

```markdown
{ŞEHİR} SABAH BÜLTENİ — Son 24 saatte {ŞEHİR}'de olan her şeyi kapsamlı şekilde özetle.

web_search ile aşağıdaki her bir kaynak için AYRI arama yap. Toplam 8-10 farklı arama yapılacak.

---

## ARANACAK KAYNAKLAR:

### 1. Fuarlar & Etkinlikler & Eğlence
- "{ŞEHİR} fuar takvimi"
- "{ŞEHİR} etkinlikler bugün"
- "{ŞEHİR} konser sergi tiyatro"

### 2. Kaza & Trafik
- "{ŞEHİR} trafik kaza son dakika bugün"
- "{ŞEHİR} trafik haberleri"

### 3. Toplu Taşıma Duyuruları
- "{ŞEHİR} metro sefer duraklama aksama bugün"
- "{ŞEHİR} otobüs hat değişikliği"
- Varsa resmi site: metro.{sehir}.istanbul, {sehir}.bel.tr

### 4. İlçe Belediye Duyuruları — "Duyurular" sayfası
- "{ŞEHİR} ilçe belediye duyuru" site:turkiye.gov.tr VEYA site:{sehir}.bel.tr
- Önemli ilçeler için ayrı ayrı ara: Kadıköy, Şişli, Beşiktaş vb. (İstanbul için)
  VEYA şehrin ana ilçeleri (Kayseri için: Melikgazi, Kocasinan, Talas, Hacılar, İncesu)

### 5. Valilik Duyurusu
- "{ŞEHİR} valiliği duyuru" site:{sehir}.gov.tr
- "{ŞEHİR} valiliği basın açıklaması"

### 6. Emniyet Duyurusu
- "{ŞEHİR} emniyet müdürlüğü duyuru"
- "{ŞEHİR} emniyet basın açıklaması"
- "{ŞEHİR} polis trafik uygulama duyuru"

### 7. Cumhuriyet Savcılığı Duyurusu (büyükşehirler için)
- "{ŞEHİR} cumhuriyet savcılığı duyuru" site:adalet.gov.tr
- "{ŞEHİR} başsavcılık basın açıklaması"

---

## ÇIKTI FORMATI

🏙️ **{ŞEHİR} BÜLTENİ** — {günün tarihi} (Saat XX:XX)

**🎪 Fuarlar, Etkinlikler & Eğlence**
• ...
• ...

**🚗 Trafik & Kaza Haberleri**
• ...
• ...

**🚇 Toplu Taşıma Duyuruları**
• ...
• ...

**🏛️ Belediye Duyuruları**
• ...
• ...

**🏢 Valilik Duyurusu**
• ...
• ...

**👮 Emniyet Duyurusu**
• ...
• ...

**⚖️ Cumhuriyet Savcılığı Duyurusu** (varsa)
• ...
• ...

---

Kurallar:
- Sadece {ŞEHİR} ile ilgili haberler
- Sadece son 24 saat
- Her madde MAX 1 cümle
- Kaynak belirt (site adı)
- O kategoride haber yoksa "Son 24 saatte kayda değer bir gelişme yok." yaz
- Başta "Eymen, günaydın! ☀️" yaz (Eymen için sabit)
```

## Canlı Cronjob Referansları (Eymen)

Bu kullanıcı için aşağıdaki şehir bültenleri aktiftir:

| Şehir | Job ID | Schedule | Saat |
|---|---|---|---|
| İstanbul | `c86d4f2d0b76` | `30 8 * * *` | 08:30 |
| Kayseri | `c2a380d4e818` | `0 9 * * *` | 09:00 |

Her ikisi de `deliver: all` ile hem bu sohbete hem Telegram Home kanalına gönderir.

## Genel Özet Cronjob Referansı

| Özellik | Değer |
|---|---|
| Job ID | `30ad69089a2b` |
| Schedule | `15 8 * * *` (08:15) |
| Deliver | `origin,all` |
| Tools | `web` |

Birlikte çalışma sırası: 08:15 genel özet → 08:30 İstanbul → 09:00 Kayseri

## İstanbul — Özel Prompt

(Canlı cronjob prompt'u `sabah-ozeti-0800` ile karışmasın diye ayrıca saklanmaz. 
Yeniden oluşturmak için yukarıdaki şablonda `{ŞEHİR}` = "İstanbul" yap, 
İstanbul'a özgü ilçeleri ekle (Kadıköy, Şişli, Beşiktaş, Üsküdar, Maltepe, 
Ataşehir, Kartal, Pendik, Fatih, Esenler, Bağcılar, Küçükçekmece) 
ve toplu taşıma için metro.istanbul + iett.istanbul sitelerini ara.)

## Kayseri — Özel Prompt

(Canlı cronjob prompt'u `kayseri-sabah-bulteni`'dir. 
Yeniden oluşturmak için yukarıdaki şablonda `{ŞEHİR}` = "Kayseri" yap,
Kayseri ilçelerini kullan (Melikgazi, Kocasinan, Talas, Hacılar, İncesu, Develi, Yahyalı)
ve etkinlikler için Kayseri Büyükşehir Belediyesi sitesine öncelik ver.)

## Kullanıcı Tercihleri (Eymen için sabit)

- Türkçe cevap
- Her haber MAX 1 cümle
- Kaynak belirt (site adı parantez içinde)
- "Eymen, günaydın! ☀️" ile başlasın
- Yoksa "Kayda değer bir gelişme yok." yazsın
- İstanbul 08:30, Kayseri 09:00 (genel özet 08:00'den sonra sıralı)
