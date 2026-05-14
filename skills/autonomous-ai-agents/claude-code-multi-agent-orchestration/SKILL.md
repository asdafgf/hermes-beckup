---
name: claude-code-multi-agent-orchestration
description: "Claude Code ile multi-agent orchestration: birden çok Claude Code session'ını aynı projede koordine etme, calibrate skill kullanımı, agent'ları yönetme, proje paylaşımı. AI işletmesi yürütme — bir AI eğitim/danışmanlık işini neredeyse tamamen Claude Code üzerinden yönetme."
version: 1.0
author: hermes
source: "https://youtu.be/UpgjdQJShWg — Claude Code Multi-Agent Orchestration"
category: autonomous-ai-agents
tags: [claude-code, multi-agent, orchestration, calibrate, project-management, ai-business]
---

# Claude Code Multi-Agent Orchestration

## 🎯 Ne Zaman Kullanılır

- Kullanıcı "birden çok AI agent'ı aynı anda nasıl yönetirim?" diye sorduğunda
- Claude Code'da multi-session çalışma gerektiğinde
- Calibrate skill'i ve agent orchestration konuşulduğunda
- AI ile iş yönetimi, danışmanlık, eğitim içeriği üretimi hakkında konuşulduğunda

---

## 🧠 Ana Konsept: Multi-Agent Orchestration

Claude Code ile **birden çok session'ı aynı projede koordine etme** — her session ayrı bir agent gibi çalışır, aynı codebase üzerinde paralel iş yapar.

### Calibrate Skill
Her session'da ilk yapılması gereken şey: **calibrate**.
- Claude Code'a proje bağlamını, hedefleri ve kısıtlamaları hatırlatır
- Session'ın hafızası gibi çalışır
- Her yeni session'da calibrate çalıştırılır

```
Session 1: Frontend geliştirme → calibrate ile başla
Session 2: Backend API → ayrı session, ayrı calibrate
Session 3: Test yazma → paralel çalışır
```

---

## 🔧 Multi-Session Workflow

### 1. Proje Yapısı
```
/my-ai-business/
├── projects/
│   ├── client-1/
│   ├── client-2/
│   └── lessons/        # Yayınlanan eğitim içerikleri
├── shared/
│   ├── memory/         # Calibrate için ortak bağlam
│   └── templates/      # Tekrar kullanılabilir şablonlar
└── agents/
    ├── frontend/       # Session 1
    ├── backend/        # Session 2
    └── content/        # Session 3
```

### 2. Share Projects
Claude Code'da **Share Projects** özelliği:
- Bir session'da yapılan değişiklikler diğer session'larla paylaşılır
- Agent'lar aynı anda aynı projede çalışabilir
- Örn: Session 1 backend yazarken Session 2 frontend'i günceller

### 3. Calibrate ile Session Başlatma
```markdown
# calibrate.md
Proje: [proje adı]
Hedef: [bu session'da ne yapılacak]
Kısıtlamalar: [varsa sınırlamalar]
Referanslar: [ilgili dosyalar]
Önceki session: [son durum]
```

---

## 💼 AI İşletmesi Yürütme

Video'daki içerik üreticisi, **AI eğitim ve danışmanlık işini neredeyse tamamen Claude Code üzerinden yürütüyor:**

### Günlük İş Akışı
```
09:00 → Session 1: Müşteri projesi (calibrate + çalışma)
10:00 → Session 2: Eğitim içeriği hazırlama (ayrı session)
11:00 → Session 3: Agent'ları izleme ve yönlendirme
13:00 → Session 4: Yeni bir müşteri için proje başlatma
15:00 → Tüm session'ları senkronize etme
```

### Agent Yönetimi
- Her session **bağımsız** bir agent gibi çalışır
- Agent'lar **aynı codebase** üzerinde çalışabilir
- Calibrate ile her session **bağlamını korur**
- **Share Projects** ile değişiklikler senkronize olur

### AI İşinin Avantajları
- **Tek kişi + çoklu AI agent = büyük ekip**
- 7/24 çalışabilen agent'lar
- Her müşteri için ayrı session
- Ölçeklenebilir iş modeli

---

## ⚡ Calibrate Skill'inin Önemi

Calibrate, Claude Code'da **en sık kullanılan komutlardan biri**:

```bash
# Her session başında:
claude
# Açılan prompt'a: "calibrate" veya
# Kendi calibrate dosyan varsa:
cat calibrate.md | claude
```

### Calibrate'te Olması Gerekenler
1. **Proje bağlamı:** Ne üzerinde çalışıyoruz?
2. **Hedef:** Bu session'da ne başarmalıyız?
3. **Kısıtlamalar:** Hangi kararlar alındı, hangi teknolojiler kullanılıyor?
4. **Önceki durum:** Son bırakılan yer neresi?
5. **Referanslar:** Hangi dosyalara bakmalı?

---

## 🎯 Pratik Kullanım

### Çoklu Session Yönetimi İçin İpuçları

| İpucu | Açıklama |
|-------|----------|
| **Her session'a bir görev** | Bir session'da frontend, diğerinde backend |
| **Calibrate'i standartlaştır** | Tüm session'larda aynı format |
| **Share Projects kullan** | Değişiklikleri otomatik senkronize et |
| **Agent'ları izle** | Her session'ın çıktısını düzenli kontrol et |
| **Memory kullan** | Calibrate için ortak bir bellek dosyası tut |

### Hangi Senaryoda Kullanılır?
- **Freelancer:** Birden çok müşteri projesini aynı anda yönetme
- **Eğitimci:** Ders içeriği + örnek kod + egzersizleri paralel hazırlama
- **Startup:** Tek geliştirici = tüm ekibi AI ile oluşturma
- **Danışman:** Her müşteri için ayrı session + ortak codebase

---

## 🔗 İlgili Skill'ler
- claude-code-aios-deep-dive — Claude Code AIOS konsepti
- hermes-agent-comparison-guide — Agent karşılaştırması
- claude-ai-cheat-codes-levels — AI kullanım seviyeleri
