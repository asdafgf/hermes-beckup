---
name: claude-ai-cheat-codes-levels
description: "Claude AI kullanımında 3 seviye cheat code: Beginner (screenshot + prompt engineering), Intermediate (Projects/KB + Excel/PPT/Word entegrasyonu), Advanced (Artifacts + public sharing + interactive tools). Her seviyede AI'dan maksimum verim almak için somut teknikler."
version: 1.0
author: hermes
source: "https://youtu.be/ZRb7D6R64hM — Claude AI Cheat Codes"
category: ai-productivity
tags: [claude, ai, cheat-code, productivity, prompt-engineering, artifacts]
---

# Claude AI Cheat Codes — 3 Seviye

## 🎯 Ne Zaman Kullanılır

- Kullanıcı "AI'dan daha verimli nasıl yararlanırım?" diye sorduğunda
- Claude, ChatGPT veya benzeri bir AI aracını daha etkili kullanma ipuçları istendiğinde
- Prompt mühendisliği, knowledge base, artifacts gibi konular açıldığında
- "AI cheat code", "AI level up", "AI productivity" gibi kavramlar geçtiğinde

---

## 📋 Seviye 1 — Beginner (Başlangıç)

### Screenshot Kullanımı
Metin kopyalayıp yapıştırmak yerine **ekran görüntüsü at**. AI görselleri okuyabilir — bu, yazıyı elle aktarmaktan çok daha hızlı.

```
❌: "şu hatayı alıyorum: [metni elle yaz]"
✅: Ekran görüntüsü at → AI'ya yapıştır → "Bu hatayı nasıl çözerim?"
```

### Prompt'u Search Bar Değil, Asistan Gibi Kullan
Çoğu kişi AI'yı Google gibi kullanıyor — tek cümlelik sorgu atıp cevap bekliyor. Oysa AI bir **asistan**, bir arama motoru değil.

| Yanlış | Doğru |
|--------|-------|
| "Python decorator nedir" | "Python decorator'ları anlat. Önce basit örnek, sonra real-world kullanım. Kodları da göster." |
| "şu kodu düzelt" | "Şu kodda hata var: [kod]. Hatayı bul, nedenini açıkla ve düzeltilmiş halini göster." |

**Kural:** Prompt ne kadar spesifik ve bağlamlı olursa, AI o kadar iyi cevap verir.

---

## 📋 Seviye 2 — Intermediate (Orta)

### Projects / Knowledge Base Kullanımı
AI sohbetlerine **proje bağlamı** ekle. Proje bilgilerini (kod tabanı, dokümantasyon, notlar) AI'nın hafızasına yükle ki her soruda yeniden anlatmak zorunda kalma.

```
📁 projects/my-app/
   ├── README.md
   ├── requirements.txt
   └── docs/
       └── api.md

→ AI bu dosyaları okuyup proje hakkında bağlam sahibi olur.
→ "users endpoint'ine nasıl istek atarım?" gibi soruları bağlamdan cevaplar.
```

### Excel Entegrasyonu
AI'ya Excel dosyası ver, şunları yapmasını iste:
- Mevcut formülleri analiz et ve açıkla
- PowerQuery sorguları yaz
- Yeni formüller oluştur (VLOOKUP, INDEX/MATCH, XLOOKUP, SUMIFS, vb.)
- Çoklu sekme workbook'larını oku ve raporla

```
💡 Kullanım: "Şu Excel'deki satış verilerini analiz et, hangi aylar en yüksek,
   hangi ürün kategorisi önde, ve bana bir özet tablo yap."
```

### PowerPoint Entegrasyonu
AI'ya slide master dosyasını ver:
- **Brand colors** ve **slide layouts**'u korur
- Mevcut şablonla uyumlu yeni slaytlar oluşturur
- Tutarlı tasarım dili sağlar

```
💡 Kullanım: "Şirket sunum şablonumu yüklüyorum. Bana Q2 roadmap için
   5 slaytlık bir sunum hazırla: hedefler, timeline, bütçe, riskler, sonuç."
```

### Word Entegrasyonu
Doküman analizi ve düzenleme:
- Uzun dokümanları özetleme
- Dilbilgisi/tarz kontrolü
- Format koruyarak düzenleme

---

## 📋 Seviye 3 — Advanced (İleri)

### Artifacts Kullanımı
AI'nın ürettiği **interaktif içerikleri** kullan:

**Nedir:** AI'nın oluşturduğu HTML/CSS/JS, SVG, React component, Mermaid diagram gibi görsel/interaktif çıktılar.

**Kullanım alanları:**
- Hızlı prototip: "Bana bir todo app yap" → hemen çalışan versiyon
- Diagram: "Şu API akışını mermaid ile çiz" → görsel olarak gör
- Dashboard: "Satış verilerimi gösteren bir dashboard yap"
- Oyun/demo: Hızlı interaktif bir şey

### Public Link ile Paylaşım
Kod bilmeyen kişiler bile AI'nın oluşturduğu artifact'leri **public link** ile paylaşabilir:
- Non-coder'lar için devrim: "şu dashboard'ı arkadaşımla paylaş"
- Herkes görebilir, etkileşime girebilir
- Güncelleme gerektiğinde AI'ya söyle, link güncellenir

```
💡 Örnek: Bir marketing uzmanı AI'ya "bana satış funnel'ını gösteren
   interaktif bir chart yap" der, AI yapar, public link ile ekip paylaşır.
```

### Chart/Diyagram Değiştirme
AI'nın oluşturduğu chart'ları canlı değiştir:
- "X eksenini aylara göre değil, çeyreklere göre yap"
- "Bar chart yerine line chart kullan"
- Renk paletini değiştir
- Yeni veri ekle

---

## ⚡ Productivity Shortcuts (Hepsinde Geçerli)

| Kural | Açıklama |
|-------|----------|
| **Spesifik ol** | "Şunu yap" değil, "Şu formatta, şu uzunlukta, şu açıdan yap" |
| **Bağlam ver** | Her soruda projeni, kodunu, dosyanı yeniden anlatma — Projects/KB kullan |
| **Görsel kullan** | Metin yerine screenshot, dosya, ekran kaydı at |
| **Artifact'leri keşfet** | Sadece metin değil, interaktif içerik iste |
| **Iterate et** | İlk cevap mükemmel olmayabilir — "şunu değiştir", "şurayı geliştir" de |

---

## 🔄 Kendi Kendine Öğrenme

AI'yı kullandıkça şunları öğrenir:
- **Keyword store:** "word", "powerpoint", "cheat code", "code level" gibi terimler otomatik öğrenilir
- **TF-IDF self-learning:** Her kullanımda hangi terimlerin önemli olduğu analiz edilir
- **Gelecek seanslarda:** Daha önce öğrenilen terimlere göre daha akıllı timestamp seçimi

---

## 📚 İlgili Skill'ler

- `watch-youtube` — YouTube videolarını analiz etme pipeline'ı
- `wiki-schema` — Obsidian wiki yönetimi ve knowledge graph
