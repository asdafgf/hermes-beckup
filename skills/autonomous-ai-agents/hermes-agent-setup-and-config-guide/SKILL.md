---
name: hermes-agent-setup-and-config-guide
description: "Hermes Agent kurulum ve yapılandırma rehberi: CLI kurulumu, provider ayarları (OpenAI, OpenRouter, Anthropic, Codex), terminal seçimi, skills sistemi, GitHub'dan skill import. Hermes Agent'ı local veya cloud'da çalıştırma."
version: 1.0
author: hermes
source: "https://youtu.be/BWprePrNwWU — Hermes Agent Setup Guide"
category: autonomous-ai-agents
tags: [hermes, setup, install, configure, provider, terminal, skills]
---

# Hermes Agent Kurulum ve Yapılandırma Rehberi

## 🎯 Ne Zaman Kullanılır

- Kullanıcı "Hermes Agent nasıl kurulur?" diye sorduğunda
- Provider ayarları (OpenAI, OpenRouter, Anthropic, Codex) yapılandırılırken
- Terminal seçimi ve skills sistemi hakkında bilgi gerektiğinde
- Hermes Agent'ı ilk kez kuran birine yardım ederken

---

## 🔧 Kurulum

### CLI ile Kurulum
```bash
# Ana kurulum komutu
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | sh

# Veya npm ile
npm install -g @nousresearch/hermes-agent
```

### İlk Çalıştırma
```bash
hermes
# İlk çalıştırmada setup wizard açılır
```

---

## ⚙️ Yapılandırma

### Provider Seçimi
Hermes Agent birden çok AI provider'ı destekler:

| Provider | API Key | Model | Not |
|----------|---------|-------|-----|
| **OpenAI** | `OPENAI_API_KEY` | GPT-4, GPT-5 | En yaygın |
| **OpenRouter** | OPENROUTER_API_KEY | Çoklu model | Tek key ile tüm modeller |
| **Anthropic** | ANTHROPIC_API_KEY | Claude | Claude Code entegrasyonu |
| **Codex** | CODEX_API_KEY | Codex modelleri | OpenAI Codex |

### Provider Yapılandırma
```bash
# Provider ayarlama
hermes config set provider openrouter
hermes config set model openai/o3-mini

# API Key ekleme
hermes config set api_key YOUR_API_KEY

# Veya ortam değişkeni olarak
export OPENROUTER_API_KEY="sk-..."
```

### Terminal Seçimi
Hermes Agent farklı terminallerde çalışabilir:
- **Local:** Kendi bilgisayarında çalıştırma
- **SSH:** Uzak sunucuya bağlanma
- **Docker:** Container içinde çalıştırma

```bash
# Terminal tipini seçme
hermes config set terminal local
# veya
hermes config set terminal ssh
```

---

## 🧠 Skills Sistemi

### Skills Kategorileri
```
~/.hermes/skills/
├── security/        # Güvenlik skill'leri
├── devops/          # DevOps skill'leri
├── github/          # GitHub workflow skill'leri
├── youtube/         # YouTube analiz skill'leri
└── ...              # Diğer kategoriler
```

### GitHub'dan Skill Import
```bash
hermes skills import trailofbits/skills
hermes skills import getsentry/skills
hermes skills import expo/skills
```

---

## 💡 Önemli İpuçları

### Subscription vs Pay-as-you-go
- **Subscription:** OpenAI/Anthropic aboneliği olanlar için — daha ucuz
- **Pay-as-you-go:** Kendi API key'ini kullananlar için — esnek
- **Codex aboneliği olanlar:** Codex provider'ı en iyi seçenek (ban riski yok)

### En İyi Uygulamalar
1. **Provider'ı doğru seç:** Kullanım amacına göre OpenAI, Anthropic veya OpenRouter
2. **Terminal tipini ayarla:** Local mi, SSH mi, Docker mı?
3. **Skills import et:** GitHub'dan hazır skill'leri yükle
4. **Auto-update ayarla:** `hermes config set auto_update true`
5. **Yedekle:** `~/.hermes/` klasörünü düzenli yedekle

---

## 🔗 İlgili Skill'ler
- hermes-agent-comparison-guide — Hermes vs diğer araçlar
- hermes-agent — Hermes Agent ana yapılandırma
- skill-import — GitHub'dan skill import
