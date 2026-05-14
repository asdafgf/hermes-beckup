---
name: hermes-agent-comparison-guide
description: "Hermes Agent vs Claude Code vs OpenClaw vs Codex — AI coding agent karşılaştırma rehberi. Hermes Agent'ın skills sistemi, voice/text çıktı, Excalidraw diyagram, komut modları, otonom yetenekler. Hangi aracın hangi senaryoda kullanılacağı."
version: 1.0
author: hermes
source: "https://youtu.be/gb5TlGw6Uks — Hermes Agent Deep Dive"
category: autonomous-ai-agents
tags: [hermes, claude-code, openclaw, codex, ai-agent, comparison, skills]
---

# Hermes Agent vs Diğer AI Kodlama Araçları

## 🎯 Ne Zaman Kullanılır

- Kullanıcı "Hermes mi, Claude Code mu, OpenClaw mu?" diye sorduğunda
- AI coding agent karşılaştırması istendiğinde
- Hermes Agent'ın özellikleri, skills sistemi, voice modu hakkında soru geldiğinde
- "Hangi aracı hangi iş için kullanmalıyım?" sorusu

---

## 🧠 Hermes Agent — Genel Bakış

Hermes Agent, terminal üzerinden çalışan, çok platformlu (Telegram, Discord, CLI) bir AI asistandır.

### Temel Özellikler

| Özellik | Açıklama |
|---------|----------|
| Skills Sistemi | SKILL.md formatında yapılandırılmış görev talimatları. Kullanıcı bir şey istediğinde ilgili skill otomatik yüklenir |
| Multi-Platform | Telegram, Discord, CLI — aynı anda tüm kanallarda çalışabilir |
| Voice Çıktı | Metin yanında ses notu döndürebilir |
| Excalidraw Diyagram | El çizimi görünümlü JSON diyagramlar oluşturabilir |
| Skills Library | ~70+ hazır skill (PDF, Excel, siber güvenlik, Expo, Cloudflare, vb.) |
| GitHub Entegrasyonu | GitHub'dan skill import edilebilir |
| Otonom Mod | Background'da çalışabilir, cronjob ile zamanlanabilir |

### Güçlü Yönleri

- Skills sistemi rakiplerinde olmayan en büyük fark
- Multi-platform olması Telegram/Discord'dan komut verme imkanı
- Türkçe tam destek
- Voice + diyagram gibi zengin çıktı formatları
- Otonom çalışma (gece boyunca eğitim, cronjob)

---

## ⚔️ Karşılaştırma

### Claude Code (Anthropic)
- En derin kod anlama, uzun context, Agentic mode
- Zorlu kodlama görevleri, refactoring, büyük projeler
- Sadece CLI (terminal)
- Skills yok (CLAUDE.md ile sınırlı)
- İdeal: Karmaşık yazılım geliştirme

### OpenClaw (Açık Kaynak)
- Açık kaynak, özelleştirilebilir, topluluk desteği
- Her seviye kodlama
- CLI
- Skills kısmen var
- İdeal: Açık kaynak sevenler, özelleştirme isteyenler

### Codex (OpenAI)
- En hızlı büyüyen araç
- **Süper uygulama (super app)** — her şeyi tek yerden yapma iddiası
- **ChatGPT tarzı sohbet arayüzü** (sol: projeler, sağ üst: sohbet, sağ alt: kod/preview)
- Kurulum: `npm install -g @openai/codex`
- Web sitesi, uygulama, API — hepsi tek arayüzden
- Dahili proje sistemi (her proje kendi chat geçmişini tutar)
- Web preview desteği
- Düşük öğrenme eğrisi (ChatGPT kullanan herkes)
- İdeal: Hızlı prototip, web/app geliştirme, MVP çıkarma

### Hermes Agent
- Skills sistemi en büyük fark
- Kodlama + doküman + araştırma + otomasyon
- Telegram, Discord, CLI — hepsi birden
- 70+ hazır skill + GitHub'dan import
- İdeal: Çok yönlü asistana ihtiyaç, multi-platform

---

## 🎯 Senaryo Bazlı Seçim

| Görev | Önerilen Araç |
|-------|--------------|
| Karmaşık kodlama / refactoring | Claude Code |
| Hızlı prototip / basit işler | Codex |
| Açık kaynak / özelleştirme | OpenClaw |
| Çok yönlü / multi-platform / otonom | Hermes Agent |

**Not:** Bunlar alternatif değil, tamamlayıcı. Claude Code kod yazar, Hermes Agent her şeyi yönetir ve gerektiğinde Claude Code'u çağırır.

---

## 🔧 Hermes Özel Yetenekler (Rakiplerde Olmayan)

### 1. Skills Sistemi
- SKILL.md formatı → yapılandırılmış görev talimatları
- Otomatik skill yükleme
- GitHub'dan import: trailofbits, getsentry, expo, cloudflare, stripe, anthropic
- Kendi skill'ini yazma (skill_manage)

### 2. Voice Çıktı
Metin + sesli yanıt — uzun raporları dinleme, multitasking.

### 3. Excalidraw Diyagram
El çizimi görünümlü diyagramlar (mimari, akış, network topolojisi).

### 4. Otonom / Background Çalışma
Gece eğitimi, saat başı raporlama, cronjob, notify_on_complete.

### 5. Multi-Platform Aynı Anda
Telegram + Discord + CLI + webhook — hepsi aynı oturum.

---

## 💡 Kullanım Stratejisi

1. Günlük işler: Hermes Agent (multi-platform, skills)
2. Zorlu kod: Hermes içinden Claude Code'u çağır (delegate_task ile)
3. Hızlı prototip: Codex (delegate_task ile)
4. Otomasyon: Hermes cronjob + background
5. Doküman: Hermes (PDF, Excel, PPTX, DOCX skill'leri)
6. Araştırma: Hermes web_search + Ollama + wiki

---

## 📚 İlgili Skill'ler

- claude-ai-cheat-codes-levels — AI kullanım seviyeleri
- watch-youtube — YouTube video analizi
- hermes-agent — Hermes Agent yapılandırma ve kullanım
- skill-import — GitHub'dan skill import etme
