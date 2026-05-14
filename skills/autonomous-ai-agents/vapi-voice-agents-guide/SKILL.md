---
name: vapi-voice-agents-guide
description: "Vapi ile voice AI agent oluşturma ve yönetme kılavuzu. Sesli AI ajanlarının temelleri: Input/Output dönüşümü (ses→metin→LLM→metin→ses), tools/function calling, appointment booking, inbound/outbound calls. Vapi platformu: dashboard, agents, tools, numbers yönetimi."
version: 1.0
author: hermes
source: "https://youtu.be/zWLZ3bVVwD8 — Vapi Voice Agents Guide"
category: autonomous-ai-agents
tags: [vapi, voice-agents, ai-voice, voice-assistant, llm, tools, function-calling]
---

# Vapi Voice Agents — Sesli AI Ajanları Kılavuzu

## 🎯 Ne Zaman Kullanılır

- Kullanıcı "sesli AI asistan nasıl yapılır?" diye sorduğunda
- Voice agents, Vapi, Twilio gibi platformlar hakkında bilgi istendiğinde
- AI sesli görüşme, appointment booking, inbound/outbound call otomasyonu konuşulduğunda
- Ses → metin → LLM → metin → ses dönüşüm zinciri anlatılırken

---

## 🧠 Voice Agent Nedir?

Bir voice agent, sesli konuşmayı anlayıp yanıtlayan AI sistemidir. Temel dönüşüm:

```
Kullanıcı (ses) → STT (Speech-to-Text) → LLM → TTS (Text-to-Speech) → Kullanıcı (ses)
     ↑                                                                       ↓
     └─────────────────── Tools / Function Calling ──────────────────────────┘
```

### Dönüşüm Adımları

1. **Input:** Kullanıcının sesi alınır
2. **STT (Speech-to-Text):** Ses metne çevrilir (Whisper, Deepgram, vb.)
3. **LLM:** Metin işlenir, anlam çıkarılır, yanıt oluşturulur
4. **Tools (Opsiyonel):** LLM takvim, CRM, veritabanı gibi dış araçlara erişir
5. **TTS (Text-to-Speech):** Metin tekrar sese çevrilir
6. **Output:** Kullanıcıya sesli yanıt verilir

---

## 🔧 Vapi Platformu

### Genel Bakış
Vapi, voice agent oluşturma ve yönetme platformu. Dashboard üzerinden:
- Agent'lar oluşturma ve yapılandırma
- Tools (araçlar) tanımlama
- Telefon numaraları yönetimi
- Inbound/Outbound call yönetimi

### Dashboard Bölümleri

| Bölüm | Açıklama |
|-------|----------|
| **Agents** | Voice agent'ları oluşturma ve düzenleme |
| **Tools** | Function calling için araç tanımlama |
| **Numbers** | Telefon numaraları satın alma/yönetme |
| **Assistants** | Yardımcı asistan yapılandırmaları |
| **Analytics** | Çağrı istatistikleri ve loglar |

---

## 🛠️ Voice Agent Oluşturma

### 1. Agent Tanımlama
Her agent için:
- **System prompt:** AI'nın kişiliği ve görevi
- **Voice:** Kullanılacak TTS sesi (cinsiyet, aksan, ton)
- **Model:** Arka plandaki LLM (GPT-4, Claude, vb.)
- **Tools:** Kullanabileceği araçlar

### 2. Tools (Function Calling)
Tools, voice agent'ın dünyayla etkileşime girmesini sağlar:

```python
# Örnek: Google Calendar appointment booking
tool = {
    "name": "book_appointment",
    "description": "Google Calendar'a randevu oluşturur",
    "parameters": {
        "date": "string",
        "time": "string",
        "duration": "integer",
        "email": "string"
    }
}
```

**Yaygın Tools:**
- Google Calendar randevu alma
- Airtable CRM sorgulama
- Veritabanı sorgulama
- E-posta gönderme
- Sipariş takibi

### 3. Telefon Numarası
- Vapi üzerinden numara satın al
- Inbound (gelen arama) veya Outbound (giden arama) seç
- Numara başına bir agent atanabilir

---

## 📞 Call Tipleri

### Inbound (Gelen Arama)
```
Müşteri arar → Vapi karşılar → Agent konuşur → Result
```

- Müşteri hizmetleri
- Destek hattı
- Sipariş takibi
- Randevu değişikliği

### Outbound (Giden Arama)
```
Agent arar → Müşteri açar → Agent konuşur → Result
```

- Telefon satış
- Anket
- Hatırlatma
- Bilgilendirme

### Website Widget
Web sitesine gömülebilir voice agent:
- Ziyaretçi siteye gelir → widget açar → konuşur
- Canlı destek benzeri
- 7/24 hizmet

---

## 💡 Kullanım Senaryoları

| Senaryo | Tool'lar | Verdiği |
|---------|----------|---------|
| **Doktor randevusu** | Google Calendar, CRM | 7/24 randevu alma |
| **Müşteri desteği** | Ticket sistemi, KB | İlk yanıt süresi ↓ |
| **Telefon satış** | CRM, Email | Outbound arama otomasyonu |
| **Restoran rezervasyon** | Takvim, SMS | Rezervasyon + hatırlatma |
| **Anket** | Database, Analytics | Müşteri geri bildirimi |

---

## ⚙️ Teknik Altyapı

### Gereksinimler
- Vapi hesabı (veya alternatif: Twilio, Retell, Bland AI)
- LLM API key (OpenAI, Anthropic)
- TTS sağlayıcı (ElevenLabs, PlayHT, Deepgram)
- STT sağlayıcı (Deepgram, Whisper, AssemblyAI)
- Telefon numarası

### Maliyet Faktörleri
- STT ($/dk)
- LLM ($/token)
- TTS ($/karakter)
- Telefon ($/ay + $/dk)
- Toplam: ~$0.05-0.15/call

---

## 📚 İlgili Skill'ler

- hermes-agent-comparison-guide — AI agent karşılaştırması
- claude-ai-cheat-codes-levels — AI kullanım seviyeleri
