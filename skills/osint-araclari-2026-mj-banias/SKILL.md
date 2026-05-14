---
name: osint-araclari-2026-mj-banias
description: "MJ Banias'ın 2026 OSINT araçları rehberi — What's My Name, Google Dork GPT, OD Crawler, OSINT Industries, DarkSide breach data, Newspapers.com ve gerçek hayat önlemleri"
version: 1.0
category: security
source: "https://youtu.be/WHOgdsEiyew"
tags: [osint, open-source-intelligence, investigation, dorking, breach-data, username-search, newspaper-archives, court-records, osint-industries, darkside]
platforms: [linux, macos, windows]
---

# 🕵️ OSINT Araçları 2026 — MJ Banias Rehberi

**Kaynak:** [YouTube — David Bombal ft. MJ Banias](https://youtu.be/WHOgdsEiyew) | **Kanal:** David Bombal

## 🧠 OSINT Felsefesi (Mindset > Tools)

OSINT araçlarla değil, **zihniyetle** başlar. Araçlar sadece işini kolaylaştırır.
- "Gum chewing ability" — meraklı, ısrarcı, puzzle çözmeyi seven kişi olmak
- Araçlar seni daha verimli yapar, ama işi sen yaparsın
- [bullshithunting.com](https://bullshithunting.com) — MJ ve ekibinin yazdığı, soruşturma zihniyeti üzerine ücretsiz kaynak

---

## 🔧 ARAÇ #1: What's My Name (Web/App)

**URL:** https://whatsmyname.app
**Fiyat:** Ücretsiz (kalıcı)
**Yapan:** OSINT Combine

**Ne işe yarar:** Kullanıcı adı (username) arama motoru. Bir kullanıcı adını girersin, internetin her yerinde o ismin kullanıldığı platformları tarar.

**Kullanım:**
1. `whatsmyname.app` adresine git
2. Hedef kullanıcı adını gir (ör: `jamesbond007`)
3. NSFW filtresini aç/kapa
4. Search'e bas → bulut taraması başlar
5. Sonuçlar: sosyal medya, forumlar, bloglar, Google cache

**Gerçek hayat örneği:**
CBC belgeseli için hedefin 1 username'inden → 20+ farklı platform hesabı, forum katılımları, ilgi alanları tespit edildi.

**⚠️ Önlem:** NSWF filtresini kapatınca hedefin illegal ilgi alanları da ortaya çıkabilir — profesyonel kullanımda dikkatli ol.

---

## 🔧 ARAÇ #2: Google Dorking Araçları

### 2a. Dork GPT
**URL:** https://dorkgpt.com (veya benzeri)
**Fiyat:** Ücretsiz

Google dork'larını otomatik oluşturur. Doğal dilde yaz → dork üretsin.

**Örnek:**
```
"Bana nasa.gov'daki tüm PDF belgelerini bul"
→ site:nasa.gov filetype:pdf
```

### 2b. Dork Search Pro
**URL:** https://dorksearchpro.com (veya benzeri)
**Fiyat:** Ücretsiz (çok reklam var — **AdBlock kullan!**)

**Özellikler:**
- Hedef siteye tam sistem taraması
- Admin panelleri, indeks sayfaları, açık kameralar
- Wayback Machine taraması
- Dosya türü filtreleri: PDF, XLS, DOC, TXT, PPT, ZIP

**⚠️ Güvenlik:** Reklamlar kumar/gambling sitelerine yönlendirir. AdBlock zorunlu.

---

## 🔧 ARAÇ #3: OD Crawler (Open Directory Crawler)

**URL:** https://odcrawler.xyz (veya benzeri)
**Fiyat:** Ücretsiz

Açık dizinleri (open directories) tarar — internette halka açık duran dosya depoları.

**Kullanım:**
- Bir hedef/şirket/kelime gir (ör: `Elon Musk`)
- MP4, PDF, ZIP, ISO vb. dosyaları bulur
- Filmler, belgeseller, kitaplar, download linkleri

**Önemi:** Şirketlerin farkında olmadan halka açık bıraktığı dosyaları keşfetmek için kullanılır.

---

## 🔧 ARAÇ #4: OSINT Industries

**URL:** https://osint.industries
**Fiyat:** ~$20/ay

**Süper güç:** Email → her şey. Bir email girince:
- Hangi sitelere kayıtlı olduğu (tüm hesaplar)
- Hangi veri ihlallerinde (breach) göründüğü
- Fotoğraflar (Gravatar, Wix, eski profiller)
- Timeline (hesap ne zaman oluşturulmuş, en son ne zaman kullanılmış)
- İlişki grafiği (birbirine bağlı hesaplar)
- Şifre hash'leri (gösterilir, içerik gizlenir)

**Desteklenen aramalar:** Email, telefon, kullanıcı adı, domain

**Gerçek hayat örneği:** Videoda MJ kendi email'ini arattı — 2012'den Plex hesabı, Etsy, Bitmoji, Bethesda, eski fotoğraflar, Wix siteleri çıktı.

---

## 🔧 ARAÇ #5: DarkSide (Breach Data)

**URL:** https://darkside.com (veya benzeri)
**Fiyat:** Kurumsal abonelik

**Veri ihlali arama motoru.** Milyarlarca sızdırılmış kaydı tarar.

**Aranabilir seçiciler:**
- ✅ Email adresi
- ✅ Kullanıcı adı / alias
- ✅ Telefon numarası
- ✅ Adres
- ✅ IP adresi
- ✅ Şifre (hash)
- ✅ Kripto cüzdan adresi
- ✅ Domain
- ✅ Şirket adı
- ✅ Kullanıcı ID

**Sonuçta gelenler:**
- Email + şifre hash'i
- Doğum tarihi
- Kayıtlı IP
- Posta kodu / şehir
- Site adı (hangi breach'ten geldiği)

**⚠️ YASAL UYARI (ÇOK ÖNEMLİ):**
1. Her yargı bölgesinde breach data kullanımı yasal değildir
2. Mahkemede delil olarak kullanılacaksa **önceden hukuk danışmanlığı al**
3. Bir breach datadan elde edilen delil, diğer tüm delilleri zehirleyebilir (fruit of the poisonous tree)
4. Bazı işverenler breach data kullanımını tamamen yasaklar
5. **Asla** kişisel amaçla / eski partner sorgulamak için kullanma!

**Özel önlem:** Eğer bir ekip yönetiyorsan, breach data erişimini **sadece güvendiğin kişilere** ver. Analistlerin eski sevgili/eski arkadaş sorgulaması yapmasını engelle.

---

## 🔧 ARAÇ #6: Newspapers.com

**URL:** https://newspapers.com
**Fiyat:** ~$10-20/ay (abonelik)

**Ne işe yarar:** Taranmış eski gazete arşivleri (1800'lerden günümüze).

**Neden önemli:**
- Google'da indekslenmemiş eski haberler
- Yerel gazetelerdeki suç haberleri
- Evlilik/doğum/ölüm ilanları
- Lise mezuniyet listeleri (hedefin sınıf arkadaşlarını bul)
- Eski dolandırıcılık/hukuki ihtilaf haberleri

**Gerçek hayat örneği:** Hedef şirket 2014'te dolandırıcılıktan tutuklanmış — ama Google'da hiçbir kayıt yok. Sadece küçük bir yerel gazetede 1 satırlık haber.

**Alternatif taktik:** Küçük kasaba arşivindeki yaşlı görevliyi ara. Telefonla konuşmak, dijitalde bulamayacağın bilgileri getirir.

---

## 🔧 ARAÇ #7: Judy Records / CanLII

**Judy Records** (ABD): https://judyrecords.com — **760 milyon** mahkeme kaydı, ücretsiz
**CanLII** (Kanada): https://canlii.org
**Diğer ülkeler:** Her ülkenin kendi kamu mahkeme kayıt sistemi var (Fransa, İngiltere, Güney Afrika vb.)

**Ne işe yarar:**
- Eski dava kayıtları
- İflas, dava, boşanma, sözleşme ihlalleri
- Hedef şirketin/a kişinin geçmiş hukuki sorunları

**Gerçek hayat örneği:**
MJ bir inşaat firmasını araştırırken → firmanın bir iç mimar tarafından dava edildiğini buldu → iç mimarı aradı → tüm belgeleri, telefon numaralarını, çalışan listesini verdi → firmanın 3 yıl önceki yapısı ortaya çıktı.

---

## 🛡️ Gerçek Hayat İçin Önlemler (Kendini Koru)

### 1. Dijital Ayak İzini Küçült
| Ne Yapmalısın | Nasıl |
|--------------|-------|
| Eski hesapları sil | [justdelete.me](https://justdelete.me) — hesap silme rehberi |
| E-posta hijyeni | Her site için ayrı email (SimpleLogin, Firefox Relay) |
| Kullanıcı adı çeşitliliği | Her platformda farklı username kullan |
| Sosyal medya gizliliği | Profilleri gizle, eski gönderileri arşivle |

### 2. Breach Data'dan Korunma
- **Have I Been Pwned:** https://haveibeenpwned.com — email'ini kontrol et
- **Firefox Monitor:** Otomatik breach bildirimi
- Her site için **benzersiz şifre** (bitwarden/keepass)
- 2FA zorunlu (tercihen hardware key: YubiKey)

### 3. OSINT Profesyoneli Olarak Etik Kurallar
| Kural | Açıklama |
|-------|----------|
| 📜 Yasal sınırlar | Araştırdığın ülkenin yasalarını bil |
| ⚖️ Mahkeme standardı | Delil toplarken mahkemede kullanılabileceğini varsay |
| 🔒 Müşteri sözleşmesi | Breach data kullanım iznini yazılı al |
| 👥 Ekip yönetimi | Hassas veriye erişimi sınırla, log tut |
| 🚫 Kişisel kullanım yasak | Asla eski sevgili/arkadaş/ünlü sorgulama |
| 📋 Belgeli çalış | Her adımı kaydet, neyi nereden aldığını belgele |

### 4. Kendi Verini Temizleme
```
Adım 1: haveibeenpwned.com'da email'lerini kontrol et
Adım 2: justdelete.me ile eski hesapları sil
Adım 3: Google'da kendi adını ara (site:linkedin.com/in "Adın Soyadın")
Adım 4: OSINT Industries'e email'ini gir — ne kadar profil çıkıyor?
Adım 5: Newspapers.com'da kendi adını ara
Adım 6: Judy Records'ta kendi adını ara
Adım 7: What's My Name'de kullanıcı adlarını kontrol et
```

---

## 🎯 Hızlı Başlangıç Komutları

```bash
# OSINT Industries API (eğer hesabın varsa)
curl -H "Authorization: Bearer API_KEY" "https://api.osint.industries/search?email=hedef@email.com"

# Google Dork (manuel örnek)
site:example.com filetype:pdf OR filetype:xlsx -www -blog

# Have I Been Pwned (API)
curl "https://haveibeenpwned.com/api/v3/breachedaccount/hedef@email.com"
```

---

## 📚 Ek Kaynaklar

- [bullshithunting.com](https://bullshithunting.com) — Soruşturma zihniyeti
- [OSINT Combine](https://osintcombine.com) — What's My Name geliştiricisi
- [Trace Labs](https://tracelabs.org) — Kayıp kişi bulma CTF'leri
- [Bellingcat](https://bellingcat.com) — Açık kaynak araştırmacı gazetecilik
- [Sector 035](https://sector035.nl) — Haftalık OSINT link koleksiyonu
