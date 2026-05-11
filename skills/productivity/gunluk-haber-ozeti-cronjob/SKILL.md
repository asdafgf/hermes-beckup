---
name: gunluk-haber-ozeti-cronjob
description: >-
  Her sabah belirlenen saatte (örn. 08:00) cronjob ile otomatik haber özeti
  hazırlama — web_search ile Türkiye ve dünya gündemini topla, kategorilere
  ayır (finans/eğitim/sağlık/teknoloji/diğer), yabancı kaynakları Türkçe'ye
  çevir, Telegram'a teslim et.
---

# Günlük Haber Özeti Cronjob

## Ne Zaman Kullanılır

- Kullanıcı her sabah belirli bir saatte **otomatik haber özeti** istediğinde
- Türkiye gündemi + Dünya haberlerini **kategorize edilmiş** şekilde toplamak
- Yabancı kaynakları (Reuters, Bloomberg, BBC, Science Daily vb.) **Türkçe'ye çevirerek** sunmak
- Telegram üzerinden teslim almak

## Cronjob Yapılandırması

```bash
# Her sabah 08:00'de çalışan cronjob
hermes cron create \
  --name "sabah-ozeti-0800" \
  --schedule "0 8 * * *" \
  --deliver telegram \
  --toolset web \
  --prompt "..."

# Şimdi çalıştır (test)
hermes cron run --name "sabah-ozeti-0800"
```

**Kritik ayarlar:**
- `--deliver telegram` — sonuç Telegram'a gelsin
- `--toolset web` — sadece web_search aracı yeterli
- `--schedule "0 8 * * *"` — her gün 08:00 (crontab formatı)

## Prompt Tasarımı

### 5 Kritik Prompt Kuralı

1. **web_search çağrıları eksiksiz olmalı:** Her kategori için 4-5 ayrı arama yönergesi ver. Farklı kaynaklar görmek için aynı konuyu farklı İngilizce/Türkçe sorgularla ara. Özellikle finans verisi (gram altın) için site-specific arama yap: `site:bigpara.hurriyet.com.tr` veya `site:altin.in`.

2. **Kategori + haber sayısı net belirtilmeli:** "20 Türkiye + 25 Dünya haberi", her alt kategoride "4-5 haber" gibi somut sayılar ver. Sayılar paylaştırılmış olmalı (ör: 5 finans + 5 eğitim + 5 sağlık + 4 teknoloji + 4 diğer = 20).

3. **Yabancı kaynak → Türkçe çeviri kuralı prompt'a yazılmalı:** `**ÖNEMLİ:** Yabancı kaynaklardan (İngilizce siteler) aldığın haberleri **Türkçe'ye çevirerek** ver.`

4. **Güncellik filtresi MUTLAKA eklenmeli:** Her arama sorgusunda "today", "bugün", "son dakika", "May 2026", günün tarihi gibi güncellik anahtar kelimeleri kullan. Prompt'a `**KRİTİK:** Tüm haberler son 24-36 saat içinde yayınlanmış olmalı. Tarihe göre filtrele. Eski haberleri (2+ gün önce) dahil etme.` yaz.

5. **X/Twitter gündemi ayrı kategori olarak eklenmeli:** 3 kategorili yapı (X + Türkiye + Dünya). X verisi için `trending topics trending24.in` veya benzeri ikincil kaynaklar kullan (doğrudan X API'si gerekmez).

### Örnek Prompt (full)

Aşağıdaki prompt yapısını kullan — her yeni cronjob için sadece kategori sayısını ve haber adetlerini güncelle:

```
BUGÜNÜN SABAH ÖZETİNİ HAZIRLA — 2 ana kategorili, kapsamlı, özlü.

Şu an saat yaklaşık 08:00. web_search kullanarak bilgi topla.
Her kategori için 3-4 ayrı arama yap (farklı kaynakları görmek için).

**ÖNEMLİ:** Yabancı kaynaklardan aldığın haberleri Türkçe'ye çevirerek ver.

## KATEGORİ 1 — TÜRKİYE GÜNDEMİ (N haber)

**Finans** (N/5 haber) — Borsa İstanbul, döviz, faiz, enflasyon
**Eğitim** (N/5 haber) — MEB, üniversite sınavları, eğitim politikaları
**Sağlık** (N/5 haber) — Sağlık Bakanlığı, hastaneler, aşı, ilaç
**Teknoloji** (N/5 haber) — Yerli teknoloji, girişim, siber güvenlik
**Diğer** (kalan) — Siyaset, spor, kültür-sanat, ulaşım

Aramalar: "Türkiye gündemi bugün", "Türkiye ekonomi haberleri", ...

## KATEGORİ 2 — DÜNYADAN HABERLER (M haber, TÜRKÇE ÇEVİRİ)

**Finans** (M/5 haber) — Petrol, altın, küresel borsalar, Fed
**Eğitim** (M/5 haber) — Küresel eğitim, üniversite sıralamaları
**Sağlık** (M/5 haber) — Yeni ilaçlar, DSÖ, tıbbi araştırmalar
**Teknoloji** (M/5 haber) — Yapay zeka, uzay, Apple/Google/MS
**Diğer** (kalan) — Jeopolitik, iklim, spor, doğal afet

Aramalar: "latest global finance news today", "technology breakthrough", ...

## ÇIKTI FORMATI

🇹🇷 **TÜRKİYE GÜNDEMİ — N Haber**

**Finans**
1. ... (kaynak)

...

🌍 **DÜNYADAN HABERLER — M Haber (Türkçe çeviri)**

**Finans**
1. ... (kaynak)

...

ÖNEMLİ KURALLAR:
- TÜM yabancı kaynak haberleri TÜRKÇE'ye çevrilmiş olmalı
- Her haber MAX 1 cümle, öz ve bilgilendirici
- Kaynak belirt (site adı parantez içinde)
- Toplam okuma süresi ~2-3 dakika olacak şekilde düzenle
- Başta "Eymen, günaydın! ☀️" yaz
```

## Kategori Standartları

Her zaman aynı 5 alt kategori kullan:

| Alt Kategori | Türkiye İçin | Dünya İçin |
|---|---|---|
| **Finans** | BIST, döviz, faiz, enflasyon, bütçe | Petrol, altın, küresel borsalar, Fed/MB |
| **Eğitim** | MEB, üniversite sınavları, eğitim politikası | Küresel eğitim, üniversite sıralamaları, değişim |
| **Sağlık** | Sağlık Bakanlığı, hastaneler, aşı/ilaç | Yeni ilaçlar, DSÖ, tıbbi araştırmalar |
| **Teknoloji** | Yerli teknoloji, girişim, siber güvenlik | Yapay zeka, uzay, Apple/Google/Microsoft |
| **Diğer** | Siyaset, spor, kültür-sanat, ulaşım | Jeopolitik, iklim, spor, doğal afet |

## Başarısızlık Senaryoları

- **web_search boş dönerse:** Prompt'ta arama sorgularını Türkçe + İngilizce çeşitlendir. "son dakika", "latest", "breaking" gibi anahtar kelimeler ekle.
- **Cronjob "ok" döndü ama mesaj gelmedi:** `last_delivery_error` alanını kontrol et. Genelde Telegram token sorunu veya çok uzun mesaj (Telegram 4096 karakter limiti).
- **Çok kısa/az haber geliyorsa:** Prompt'taki "N haber" sayısını ve her kategori için arama adedini artır.
- **Kullanıcı "mesaj gelmedi" diyorsa:** `deliver` parametresini kontrol et. `telegram` sadece Home kanalına gider. Kullanıcıyla aynı sohbette görmek için `deliver: origin,all` veya `deliver: origin` kullan.  
- **Haberler güncel değilse (eski tarih):** Prompt'a güncellik filtresi ekle ("Tüm haberler son 24-36 saat içinde yayınlanmış olmalı") ve arama sorgularına "today", "May 2026" gibi spesifik tarih anahtarları koy.
- **Gram altın fiyatı hatalıysa:** `site:bigpara.hurriyet.com.tr` veya `site:altin.in` gibi spesifik finans sitesi araması kullan. Genel arama eski/yanlış veri döndürebilir.
- **web_search güncel haber bulamazsa (eski tarihli sonuçlar):** Prompt'taki arama sorgularına günün spesifik tarihini ekle (ör: "May 12 2026" yerine "May 11 2026"). Tarih filtreleme web_search'in en zayıf noktasıdır — aynı sorguyu farklı İngilizce+Türkçe varyasyonlarla dene.
- **X/Twitter gündemi boş gelirse:** trends24.in sitesine alternatif olarak Google Trends veya "viral Turkey today" gibi genel aramalar dene. X API'sine erişim olmadan bu her zaman risklidir.

### Son Dakika Akışı Pattern (yüksek frekanslı cronjob) → Artık 08:15 bütünleşik

Bu skill'in önceki versiyonunda ayrı bir `*/5 * * * *` son-dakika-akisi cronjob'u vardı. Kullanıcı tercihiyle **kaldırıldı** ve sabah 08:15 özetinin **Kategori 1 (Son Dakika & Önemli Gelişmeler)** bölümüne entegre edildi.

**Sebep:** Günde 1 kez, tek bir kapsamlı mesaj. Gün içinde tekrar bildirim yok.

**Prompt'ta son dakika kısmı şöyle yapılandırılır:**

```
## KATEGORİ 1 — SON DAKİKA & ÖNEMLİ GELİŞMELER

Sadece GERÇEKTEN önemli/ büyük gelişmeleri al:

**Türkiye:**
- "son dakika Türkiye bugün"
- "deprem son dakika Türkiye" (varsa)
- "ekonomi kriz son dakika Türkiye"

**Dünya:**
- "breaking news today world" site:bbc.com VEYA site:reuters.com
- "war conflict latest today" veya "earthquake today"
- "global crisis latest news"

Her madde MAX 1 cümle, kaynak belirt. Yoksa bu kategoriyi tamamen kaldır.
```

**Önemli:** Bu kategoride haber yoksa `"Son 24 saatte kayda değer bir son dakika gelişmesi yok."` yazdır, kategoriyi gösterme. Kullanıcı boş kategori görmek istemez.

### Kullanıcı Tercihi: Günde 1 Mesaj Kuralı

Eymen (bu kullanıcı) için **günde yalnızca 1 kez** kapsamlı özet gönderilir. Gün içinde tekrar mesaj gelmez.

Bu kuralı uygulamak için:

1. **Son dakika akışı gibi yüksek frekanslı cronjob'lar KULLANMA.** `*/5 * * * *` yerine her şeyi sabah 08:15'teki tek bir cronjob'da birleştir.
2. Eğer kullanıcı **son dakika akışı** (ör: 5 dk'da bir) isterse, bunu reddet ve alternatif olarak **sabah özetinin içinde son dakika kategorisi** öner:
   ```
   "Günde 1 kez, sabah 08:15'te kapsamlı özet geliyor.
    Gün içinde ayrıca bildirim gelmez. Son dakika gelişmeleri
    sabah özetinin ilk kategorisinde yer alır."
   ```
3. Cronjob'u güncellerken `--schedule`'ı tek bir günlük saat olarak ayarla (ör: `15 8 * * *`).

**Bu kural Eymen'e özgüdür.** Başka bir kullanıcı farklı tercih edebilir.

### Şehir Bülteni — Genel Özetle Birlikte Çalışma

Bu skill bazen aynı kullanıcı için **genel özet + şehir bültenleri** kombinasyonu olarak çalışır. Örnek:

| Saat | Bülten | Kapsam |
|---|---|---|
| 08:15 | 📬 Kapsamlı Sabah Özeti | Son Dakika + X (15) + Türkiye (20) + Dünya (25) |
| 08:30 | 🏙️ İstanbul Bülteni | Fuar, etkinlik, trafik, metro, belediye, valilik, emniyet, savcılık |
| 09:00 | ☀️ Kayseri Bülteni | Fuar, etkinlik, trafik, kaza, belediye, valilik, emniyet, ilginç olaylar |

Şehir bültenleri genel özetten **bağımsız cronjob'lardır** (farklı schedule, farklı prompt). `gunluk-haber-ozeti-cronjob` skill'i **genel özet için prompt şablonu** sağlar; şehir bültenleri `references/sehir-bulteni-prompt-pattern.md`'deki ayrı şablonu kullanır.

Şehir bülteni eklerken dikkat edilmesi gerekenler:
- Her şehir için **ayrı cronjob** (`hermes cron create --name "sehir-adi-sabah-bulteni"`)
- Schedule'lar çakışmayacak şekilde ayarlanmalı (genelden sonra, 30 dk ara ile)
- Teslimat hepsi `all` veya `origin,all` olmalı
- Şehre özgü kaynaklar prompt'a eklenmeli (valilik sitesi, belediye sitesi, ilçe listesi)
- Kaynak bulunamazsa sessiz kal (boş kategori gösterme)

### Cronjob Yönetimi (birden çok cronjob ile)

Bu skill genellikle birden çok cronjob'un aynı anda çalıştığı bir ortamda kullanılır. Örnek: genel özet (08:00) + İstanbul (08:30) + Kayseri (09:00) + son dakika akışı (her 5 dk).

| Komut | Açıklama |
|---|---|
| `hermes cron create --name "X" --schedule "..." --deliver all --toolset web --prompt "..."` | Yeni cronjob |
| `hermes cron run --name "X"` | Şimdi çalıştır (test) |
| `hermes cron list` | Tüm cronjob'ları gör |
| `hermes cron remove --name "X"` | Cronjob'u sil (last_status ok olsa bile) |

**Teslimat hedefleri:**
- `telegram` → sadece Telegram Home kanalına (ID: 6328823909)
- `all` → Telegram Home kanalı + cronjob'u tetikleyen sohbet
- `origin,all` → cronjob'u tetikleyen sohbet + Telegram Home kanalı
- Kullanıcıyla birebir sohbette görmek için `deliver: origin,all` kullan

**Önemli:** `deliver` parametresini değiştirmek cronjob'u silip yeniden oluşturmayı gerektirmez — `hermes cron update --name "X" --deliver "origin,all"` ile güncellenebilir.

**Windows'ta cronjob çalışması:** Bilgisayar kapalıyken cronjob çalışmaz. Bilgisayar açılınca kaçırılan çalıştırmalar otomatik atlanır, sonraki zamanlanmış çalışmaya geçer. Manuel çalıştırmak için `hermes cron run --name "X"` kullan.

## Kullanıcı Tercihleri (Eymen için sabit)

- Türkçe cevap, Türkçe çeviri
- 20 Türkiye + 25 Dünya haberi, artı X'te 15 başlık + son dakika
- 5 alt kategori: finans, eğitim, sağlık, teknoloji, diğer
- Kaynak belirtmeli (site adı parantez içinde)
- Her haber MAX 1 cümle
- Saat 08:15'te Telegram'a teslim (tek mesaj, günde 1 kez)
- Gün içinde tekrar mesaj gelmez
- "Eymen, günaydın! ☀️" ile başlasın

## Alt Tür: Şehir Bülteni

Bu skill ayrıca **şehir bazlı bülten** pattern'ini de kapsar. Şehir bültenleri genel özetten sonra (08:30-09:00 gibi) çalışır ve farklı kaynaklardan toplar:
- Valilik, emniyet, savcılık, belediye duyuruları
- Fuar/etkinlik takvimi
- Trafik/kaza haberleri
- Toplu taşıma (metro, otobüs) değişiklikleri
- İlginç olaylar

Şehir bülteni prompt şablonu için:
- `references/sehir-bulteni-prompt-pattern.md` — full şablon, kaynak listesi, format

## İlgili Skill'ler

- `python-mock-test-harness` — aynı anda kurulmuş diğer cronjob (test-harness periyodik kontrolü)

## Referanslar

- `references/eymen-sabah-ozeti-prompt-3-kategori.md` — Eymen için özelleştirilmiş 3 kategorili tam prompt metni (X gündemi + Türkiye + Dünya), canlı veri kaynakları, tarih filtreleri ve kullanıcı tercihleri
- `references/sehir-bulteni-prompt-pattern.md` — Şehir bazlı (İstanbul, Kayseri vb.) bülten prompt şablonu, kaynak listesi, çıktı formatı ve yaşayan cronjob referansları
