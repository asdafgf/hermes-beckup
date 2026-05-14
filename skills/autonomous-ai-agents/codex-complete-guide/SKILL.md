---
name: codex-complete-guide
description: "OpenAI Codex CLI — tam kılavuz. Codex nedir, nasıl kurulur, temel özellikler: ChatGPT tarzı sohbet arayüzü, proje yönetimi, web/app geliştirme, Claude Code'dan farkları. Codex'i hızlı prototipleme ve günlük kodlama için kullanma."
version: 1.0
author: hermes
source: "https://youtu.be/3TdD8Qv5Tk8 — Codex Complete Guide"
category: autonomous-ai-agents
tags: [codex, openai, coding-agent, claude-code, comparison, ai-coding]
---

# Codex CLI — Tam Kılavuz

## 🎯 Ne Zaman Kullanılır

- Kullanıcı "Codex nedir?" diye sorduğunda
- Codex ile Claude Code karşılaştırması istendiğinde
- Hızlı prototip çıkarma veya basit-orta kodlama görevleri için Codex önerileceğinde
- AI coding agent seçimi yapılırken Codex seçeneği değerlendirildiğinde

---

## 🧠 Codex Nedir?

Codex, OpenAI tarafından geliştirilen bir **süper uygulama (super app)** — terminal üzerinden çalışan, sohbet edebilen, kod yazabilen, web sitesi ve uygulama geliştirebilen bir AI coding agent.

**Anahtar cümle:** "Codex, her şeyi yapabilen bir araç. Claude Code'u bıraktığım anlamına gelmez, ama Codex'in yeri ayrı."

---

## 🔧 Kurulum

### Npm ile
```bash
npm install -g @openai/codex
```

### Kullanıma başlama
```bash
codex     # CLI'ı başlatır
```

---

## 💬 Arayüz

Codex'in arayüzü **ChatGPT tarzı** bir sohbet penceresi olarak gelir:

```
┌─────────────────────────────────────────────┐
│  💬 Codex CLI                               │
├─────────────────────────────────────────────┤
│                                             │
│  Sol: Chat geçmişi (Projects)               │
│  Sağ üst: Sohbet alanı                      │
│  Sağ alt: Kod çıktısı / preview             │
│                                             │
│  ┌─────────────────────┐  ┌───────────────┐ │
│  │ Projeler            │  │ Sohbet        │ │
│  │ ├── my-app          │  │ "bana bir todo │ │
│  │ ├── blog-site       │  │  app yap"     │ │
│  │ └── api-server      │  │               │ │
│  └─────────────────────┘  │ [Yanıt...]    │ │
│                            └───────────────┘ │
└─────────────────────────────────────────────┘
```

- **Solda:** Proje listesi ve chat geçmişi
- **Sağ üst:** ChatGPT benzeri sohbet arayüzü
- **Sağ alt:** Kod çıktısı, web preview, görsel sonuçlar

---

## ⚡ Temel Özellikler

### 1. Proje Tabanlı Çalışma
Her proje kendi chat geçmişini ve dosyalarını tutar:
```
/my-app.codex/
  ├── chat_history.json
  ├── files/
  │   ├── index.html
  │   ├── style.css
  │   └── app.js
  └── preview/
```

### 2. Her Şeyi Yapabilme
Codex tek bir arayüzden şunları yapabilir:
- Web sitesi oluşturma
- Uygulama geliştirme
- API yazma
- Debugging
- Refactoring
- Dokümantasyon

### 3. ChatGPT Benzeri Deneyim
Natural language ile konuş, kod yazdır. Arayüz tanıdık geldiği için öğrenme eğrisi düşük.

### 4. Web Preview
Codex'te oluşturduğun web sayfalarını anında önizleyebilirsin.

---

## ⚔️ Codex vs Claude Code

| Yön | Codex | Claude Code |
|-----|-------|-------------|
| **Arayüz** | ChatGPT tarzı sohbet | Terminal CLI |
| **Kurulum** | `npm install -g @openai/codex` | `npm install -g @anthropic-ai/claude-code` |
| **Güçlü yön** | Hızlı prototip, her şeyi yapma iddiası | Derin kod anlama, büyük refactoring |
| **Öğrenme eğrisi** | Düşük (ChatGPT kullanan herkes) | Orta |
| **Proje yönetimi** | Dahili proje sistemi | Dosya sistemi tabanlı |
| **En iyi olduğu yer** | Web/app prototipleme, hızlı iterasyon | Karmaşık yazılım, büyük codebase |

---

## 💡 Kullanım Stratejisi

| Görev | Araç |
|-------|------|
| Hızlı prototip, web sitesi, MVP | **Codex** |
| Karmaşık refactoring, büyük proje | **Claude Code** |
| Çok yönlü asistanlık, multi-platform, otomasyon | **Hermes Agent** (orkestra) |
| Açık kaynak, özelleştirme | **OpenClaw** |

**Hermes Agent içinden Codex'i çağırma:**
```bash
# delegate_task ile Codex'e devret
task: "Codex'e şu web uygulamasını yaptır: [detay]"
```

---

## 📚 İlgili Skill'ler

- `hermes-agent-comparison-guide` — Hermes vs Claude Code vs OpenClaw vs Codex
- `claude-ai-cheat-codes-levels` — AI kullanım seviyeleri
