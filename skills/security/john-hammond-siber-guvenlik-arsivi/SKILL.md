---
name: john-hammond-siber-guvenlik-arsivi
description: "John Hammond / RootOfTheNull kanalı 1.602 videoluk siber güvenlik arşivini yönetir. Video kataloglama, kategorizasyon, transcript çekme, ve siber güvenlik öğrenimini otomatize eden master skill."
version: 2.1
author: hermes
source: "https://www.youtube.com/@_JohnHammond — 2.14M abone, 1.602 video, 451.2 saat içerik"
category: security
tags: [john-hammond, rootofthenull, siber-guvenlik, arsiv, egitim, phishing, malware, pentest, red-team]
---

# 🛡️ John Hammond / RootOfTheNull Siber Güvenlik Arşivi

## 🎯 BU ARŞİV NE AMAÇLA KULLANILIR?

Bu arşiv **siber güvenlik öğrenimi için eksiksiz bir kaynak havuzudur**. Amaçları:

### 1️⃣ Sistematik Siber Güvenlik Öğrenimi
- **21 kategori** → 1.602 video → 451 saat içerik
- Her kategori ayrı bir öğrenim yolu (learning path)
- Başlangıç → İleri seviye sıralaması

### 2️⃣ Gerçek Dünya Vaka Çalışmaları
- Gerçek phishing kampanyaları (AI destekli, Microsoft Account, Zoom vergi dolandırıcılığı)
- Gerçek malware örnekleri (Clawdbot, Infostealer, Lua stealer)
- Gerçek supply chain saldırıları (npm axios, Next.js)
- Gerçek AI saldırıları (MCP exploitation, prompt injection)
- FBI operasyonları, hacker yakalama hikayeleri

### 3️⃣ Teknik Beceri Geliştirme
- **Malware Analizi**: Infostealer'dan C2'ye tam analiz
- **Phishing Tespiti**: Sahte e-posta, sahte Zoom, sahte DMCA
- **Red Team**: Exploit geliştirme, privilege escalation, persistence
- **Blue Team**: Wazuh SIEM, threat hunting, DFIR
- **Web Güvenlik**: Nuclei, SQL injection, .git exposure
- **Cloud Güvenlik**: API key exposure, AWS/Azure hardening
- **AI Güvenlik**: Prompt injection, MCP exploitation, LLM security

### 4️⃣ Sektörel Farkındalık
- Yıllık siber suç durum raporları (Nick Ascoli ile)
- Sektör liderleriyle röportajlar (50+ podcast)
- Güncel tehdit istihbaratı
- Zero-day haberleri ve analizleri

### 5️⃣ Sertifika & Kariyer Desteği
- TryHackMe Advent of Cyber serisi
- CTF çözümleri ve yarışma hazırlığı
- Kariyer tavsiyeleri, iş bulma stratejileri
- Gerçek işe alım hikayeleri

---

## 📂 ARŞİV YAPISI

```
~/Desktop/rootofthenull_arsiv/
├── dokumanlar/
│   └── ANA_KATALOG.md          # Tüm 1602 videonun tam listesi
├── kategoriler/                 # 21 ayrı kategori dokümanı
│   ├── phishing_social_engineering.md
│   ├── malware_analysis.md
│   ├── ai_security.md
│   ├── red_team_pen_test.md
│   ├── windows_security.md
│   ├── linux_security.md
│   ├── web_security.md
│   ├── cloud_security.md
│   ├── supply_chain_attacks.md
│   ├── incident_response_forensics.md
│   ├── tools_utilities.md
│   ├── podcast_interview.md
│   ├── career_education.md
│   ├── privacy_anonimity.md
│   ├── iot_ot_ics.md
│   ├── mobile_security.md
│   ├── network_security.md
│   ├── osint.md
│   ├── bug_bounty.md
│   ├── news_current_events.md
│   └── other.md
├── transcriptler/               # Çekilen video transcript'leri (.srt/.vtt)
├── skills/                      # Bu arşivden türetilen özel skill'ler
└── john_hammond_videos.json     # Tüm video metadata (1602 satır JSON)
```

---

## 🔧 KULLANIM TALİMATLARI

### Video Arama
```bash
# Kategori bazlı arama
cat ~/Desktop/rootofthenull_arsiv/kategoriler/phishing_social_engineering.md

# Tüm katalogda arama
grep -i "ransomware" ~/Desktop/rootofthenull_arsiv/dokumanlar/ANA_KATALOG.md

# Video ID ile transcript bulma
find ~/Desktop/rootofthenull_arsiv/transcriptler -name "*VIDEO_ID*"
```

### Transcript Çekme
```bash
# Tek video
yt-dlp --write-auto-sub --sub-lang en --skip-download --convert-subs srt \
  -o "%(id)s" "https://youtu.be/VIDEO_ID"

# Toplu çekim (tüm kategori)
yt-dlp --write-auto-sub --sub-lang en --skip-download --convert-subs srt \
  --batch-file video_ids.txt
```

### Yeni Video Ekleme (kanal güncellendiğinde)
```bash
# Tüm videoları yeniden çek
yt-dlp --flat-playlist --dump-json "https://www.youtube.com/@_JohnHammond/videos" \
  > john_hammond_videos.json

# Ardından katalogları yeniden oluştur (bu skill'i kullan)
```

### Öğrenim Rotası Oluşturma
```bash
# "AI Güvenlik öğrenmek istiyorum" → ai_security.md'deki videoları sırayla izle
# "Phishing analizi" → phishing_social_engineering.md
# "CTF hazırlığı" → red_team_pen_test.md
```

---

## 🧠 ÖNEMLİ VİDEOLAR (Başlangıç İçin)

### En Popüler / Güncel 20 Video
| # | Video | Süre | Kategori | Neden Önemli |
|---|-------|------|----------|-------------|
| 1 | FAKE Zoom Taxes MALWARE | 15:52 | malware_analysis | Gerçek dünya malware analizi |
| 2 | the WORST phishing email i've ever seen | 21:05 | phishing | AI çağı phishing örneği |
| 3 | Hackers Stole Your Account (for free) | 14:59 | red_team | Hesap ele geçirme vektörü |
| 4 | The Dawn of AI Warfare | 27:52 | ai_security | AI savaşları geleceği |
| 5 | HUGE AI-powered Microsoft Account phishing | 15:00 | phishing | AI destekli büyük kampanya |
| 6 | How Teenage Hackers Hijack the Internet | 30:32 | red_team | Genç hacker profili |
| 7 | Hackers make FAKE notifications | 22:38 | iot_ot_ics | Bildirim manipülasyonu |
| 8 | Extremely Easy Identity Management (Authentik!) | 14:00 | tools | Kimlik yönetimi aracı |
| 9 | HUGE npm axios supply chain attack | 14:06 | supply_chain | Gerçek supply chain saldırısı |
| 10 | ChatGPT For The Dark Web | 22:30 | ai_security | AI + dark web kesişimi |
| 11 | NahamSec Bug Bounty Basics | 30:21 | bug_bounty | Bug bounty başlangıç |
| 12 | GraphSpy: Hacker's Tooling Deep Dive | 41:32 | tools | Hacker tool'u derinlemesine |
| 13 | "I made an Evil MCP server" (and AI fell for it) | 31:53 | ai_security | MCP güvenlik açığı |
| 14 | Infostealer Malware Logs Analyzed by... AI!?! | 22:12 | malware | AI + infostealer analizi |
| 15 | so malware is invisible now lol | 20:05 | malware | Görünmez malware teknikleri |
| 16 | Next.js & React vulnerability | 11:14 | supply_chain | Kritik web güvenlik açığı |
| 17 | The State of Cybercrime in 2025 | 43:22 | news | Yıllık siber suç raporu |
| 18 | LEAKED Russian Hackers Internal Chats | 24:02 | news | Rus hacker dahili yazışmaları |
| 19 | NPM malware now has multiple targets! | 54:38 | supply_chain | NPM malware derin analiz |
| 20 | Hacking with Nuclei: .git Secrets | 23:18 | web_security | Nuclei ile .git keşfi |

---

## 🤖 AI ÖĞRENME ENTEGRASYONU

Bu arşiv Hermes Agent ile şu şekilde entegre çalışır:

1. **Video izle → Skill oluştur**: John Hammond videolarındaki teknikleri skill'e dönüştür
2. **Transcript analizi → Özet çıkar**: Uzun videoların transcript'lerini özetle
3. **Kategori bazlı öğrenim rotası**: "Bugün X konusunu öğren" → ilgili videoları listele
4. **Pratik uygulama**: Videodaki tekniği kendi ortamında dene (güvenli şekilde)
5. **Sınav hazırlığı**: Video içeriğinden quiz/soru üret

---

## 📄 REFERANS DÖKÜMANLARI

Bu umbrella altında:
- `references/batch_aciklama.md` — Batch transcript çekme detayları
- `references/qwen_kullanim_rehberi.md` — Qwen2.5-Coder'ın bu arşiv kapsamında ne zaman/nerede kullanılacağı

## 🔗 İLGİLİ SKILL'LER ve ARŞİVLER
- hermes-agent-setup-and-config-guide
- qwen-siber-denetim
- otonom-siber-arastirma
- ai-agents-ogrenim-notlari
- olasilik-oncelik-ilkesi
- youtube-kanal-arsiv-sistemi — Genel YouTube kanal arşiv pipeline'ı
- **networkchuck_arsiv** — `~/Desktop/networkchuck_arsiv/` (372 video, CCNA/kariyer/AI ağırlıklı)
- **davidbombal_arsiv** — `~/Desktop/davidbombal_arsiv/` (1.483 video, Python hacking/CCNA ağırlıklı)
