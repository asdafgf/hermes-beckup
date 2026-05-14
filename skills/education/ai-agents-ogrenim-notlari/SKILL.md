---
name: ai-agents-ogrenim-notlari
description: "3 YouTube videosundan derlenmiş kapsamlı AI agent öğrenim notları: Claude AI cheat codes (3 seviye), Hermes/Claude Code/OpenClaw/Codex karşılaştırması, Codex CLI kılavuzu, watch-youtube pipeline'ı. Prompt mühendisliği, araç seçimi, skills sistemi, self-learning."
version: 1.0
author: hermes
source: "ZRb7D6R64hM + gb5TlGw6Uks + 3TdD8Qv5Tk8"
category: education
tags: [ai-agents, prompt-engineering, hermes, claude-code, codex, openclaw, comparison, learning-notes]
---

# AI Agent Öğrenim Notları

> Kaynak: 3 YouTube videosu, 5 skill, 1 pipeline

---

## 📚 1. CLAUDE AI CHEAT CODES — 3 Seviye

### 🟢 Seviye 1: Beginner
**Screenshot kullan:** Metin kopyalama yerine ekran görüntüsü at, AI okur.
**Prompt Search Bar değil, Asistan:** Detaylı talimat ver.

| Yanlış | Doğru |
|--------|-------|
| "Python decorator nedir" | "Decorator'ları anlat. Önce basit örnek, sonra real-world. Kod göster." |
| "şu kodu düzelt" | "Şu kodda hata var: [kod]. Hatayı bul, nedenini açıkla, düzelt." |

### 🟡 Seviye 2: Intermediate
- **Knowledge Base/Projects:** Proje dosyalarını AI hafızasına yükle
- **Excel:** Formül analizi, PowerQuery, VLOOKUP/XLOOKUP oluşturma
- **PowerPoint:** Slide master + brand colors koruyarak yeni slayt
- **Word:** Doküman özetleme, dilbilgisi kontrolü

### 🔴 Seviye 3: Advanced
- **Artifacts:** HTML/CSS/JS, SVG, React, Mermaid diagram çıktıları
- **Public Link:** Kod bilmeyenler bile paylaşabilir
- **Chart değiştirme:** Canlı düzenleme

### ⚡ Shortcuts
Spesifik ol → Bağlam ver → Görsel kullan → İterate et

---

## ⚔️ 2. AI CODING AGENT KARŞILAŞTIRMASI

| Araç | Güçlü Yön | Kurulum | İdeal |
|------|-----------|---------|-------|
| **Hermes Agent** | Skills + multi-platform + otonom | Hermes CLI | Çok yönlü asistanlık |
| **Claude Code** | En derin kod anlama | npm i -g @anthropic-ai/claude-code | Karmaşık refactoring |
| **OpenClaw** | Açık kaynak | CLI | Özelleştirme |
| **Codex** | ChatGPT tarzı + super app | npm i -g @openai/codex | Hızlı prototip |

**Kural:** Bunlar alternatif değil, tamamlayıcı. Hermes orkestra, diğerleri uzman işçi.

### Hermes Özel Güçler
- Skills sistemi (SKILL.md + auto-load + GitHub import)
- Multi-platform (Telegram + Discord + CLI)
- Voice çıktı + Excalidraw diyagram
- Otonom / background / cronjob
- 70+ hazır skill

---

## 🚀 3. CODEX CLI

**Kurulum:** `npm install -g @openai/codex`
**Başlat:** `codex`

**Arayüz:** ChatGPT tarzı — sol panel projeler, sağ üst sohbet, sağ alt kod/preview.

**Özellikler:**
- Proje tabanlı çalışma
- Web sitesi / uygulama / API geliştirme
- Web preview
- Düşük öğrenme eğrisi

---

## 🔧 4. WATCH-YOUTUBE PIPELINE

**Pipeline:** YouTube URL → yt-dlp → NLP timestamp (spaCy) → ffmpeg frame → Pillow storyboard → Vision LLM → Obsidian wiki

**Self-Learning:** TF-IDF ile her videodan yeni keyword → `data/keyword_store.json`

**Wiki Formatı:** Her sayfada Özet + Kütüphaneler + Bağlantılar + Kaynak Video zorunlu. PascalCase dosya adı. Obsidian [[link]].

---

## 💡 5. ANA ÇIKARIMLAR

1. **Prompt mühendisliği** = AI kullanımının temeli
2. **Knowledge base kullan** = her seferinde aynı şeyi anlatma
3. **Skills sistemi** = öğrenilen her şey tekrar kullanılabilir
4. **Hiçbir araç tek başına yeterli değil** = orkestra mantığı
5. **Self-learning** = AI kullandıkça daha akıllı hale gelir
6. **Video analiz** = transcript + NLP + frame extraction + storyboard

---

## 🔗 Bağlantılı Skill'ler

- claude-ai-cheat-codes-levels
- hermes-agent-comparison-guide
- codex-complete-guide
- watch-youtube
- wiki-schema
