---
name: hermes-gemini-copilot
title: "Hermes <> LLM Otonom Isbirligi Donguleri (Gemini / Ollama)"
description: "Hermes'in harici LLM'lerle konusarak gorev cozdugu veya kendini gelistirdigi donguler. Iki ana varyant: (1) Gemini ile hata cozum dongusu - Chrome CDP uzerinden Gemini sohbetine kod gonderip cozum almak; (2) Ollama ile kendi kendini gelistirme dongusu - Ollama'dan ders alip skill olarak kaydetmek. Ollama varyantinin iki alt turu: genel bilgi aktarimi ve siber guvenlik (100+ konu havuzu, Python kod zorunlu). Otomatik, kullaniciya sormaz."
category: software-development
---

# Hermes <> LLM Otonom Isbirligi Donguleri

## A. Gemini ile Hata Çözüm Döngüsü (3-2-1 Kuralı)

| Aşama | Ne yapılır |
|---|---|
| **1. deneme** | Kendi çözümünü dene (terminal, web_search, bildiğin yöntem) |
| **2. deneme** | Farklı bir yaklaşım dene |
| **3. deneme** | 🚨 Gemini'ye bağlan, sorunu tam metin yaz |
| **Kod geldi** | VS Code yeni proje aç → kopyala → kaydet → kullanıcı terminalde görsün |
| **Çıktı** | Kullanıcı VS Code terminalinde görür + ben de okuyup Gemini'ye veririm |
| **Döngü** | Çözüm bulunana kadar devam |

**Kesin kural 1:** Kullanıcıya sorma. Otomatik yürüt.
**Kesin kural 2:** VS Code açık mı kontrol et (`ps aux | grep code`) — açıksa yenisini açma, mevcut terminali kullan.
**Kesin kural 3:** Kodu ben çalıştırıp çıktısını Gemini'ye vermek yerine, kullanıcının VS Code terminalinde görmesini sağla. Ben çıktıyı ayrıca alıp Gemini'ye veririm.
**Kesin kural 4:** Her seferinde **yeni bir VS Code projesi** aç. Klasör adı her seferinde farklı olsun.
**Kesin kural 5:** Kullanıcıya ▶ **Run butonunu** kullanmasını söyle.

## B. Ollama Kendi Kendini Geliştirme Döngüsü

Bkz: `references/ollama-self-improvement-loop.md`

## C. Karşılıklı Diyalog Eğitim Protokolü (Hermes ↔ Qwen2.5-coder)

**Amaç:** Hermes ile Ollama'daki bir model arasında **karşılıklı 2 turlu diyalog** şeklinde yapılandırılmış eğitim oturumu. Her konu için Hermes açılış yapar → model cevaplar → Hermes derinleştirir → model tekrar cevaplar. Tüm diyalog skill olarak kaydedilir.

### Ne Zaman Kullanılır

- Kullanıcı "Hermes ve qwen karşılıklı konuşsun, skill olarak kaydetsin" dediğinde
- Kullanıcı "sabaha kadar otonom eğitim oturumu başlat" dediğinde
- 10+ konulu kapsamlı bir alan (siber güvenlik, vb.) öğrenilirken
- Her konunun skill olarak kalıcı kaydı isteniyorsa

### Mimari

```
HERMES (ben)                     QWEN2.5-CODER (Ollama)
    │                                   │
    ├─ [Açılış] Konuyu açar,            │
    │   bağlam verir, sorar ────────────→  Cevap üretir
    │                                   │
    │                                   ├─ [Yanıt 1] Döner
    │←──────────────────────────────────│
    │                                   │
    ├─ [Derinleştirme] Analiz eder,    │
    │   ek soru sorar ─────────────────→  Derin cevap üretir
    │                                   │
    │                                   ├─ [Yanıt 2] Döner
    │←──────────────────────────────────│
    │                                   │
    └─ Skill olarak kaydeder            │
       (SKILL.md + diyalog.txt)         │
```

### Kullanıcı Tercihleri (Bu Oturumdan — ZORUNLU — 14 Mayıs 2026)

> **Bu tercihler Eymen'in kullandığı her oturumda geçerlidir. Memory'ye de kayıtlıdır ama burada durması skill'i load eden herkesin görmesini sağlar.**

1. **Hız:** Konular arası bekleme MAX 15 saniye. Kullanıcı "ne bekliyorsun" derse çok yavaşsın demektir. 240sn gibi bekleme ASLA.
2. **Hızlı atlama:** Kullanıcı "2" yazarsa direkt 2. adıma geç. Açıklama beklemez.
3. **Timeout:** Qwen 2 dakikada cevap vermezse timeout at + yeniden dene. PTY'siz çalıştırıyorsan `curl -X POST http://localhost:11434/api/generate` kullan, `ollama run` ASLA (PTY gerektirir).
4. **İlerleme sayacı:** Her konu sonunda `#01/29 (%3)` formatında göster. Yoksa "takıldın" sanar.
5. **Diyalog formatı:** Monolog değil, karşılıklı konuşma. Hermes AKTİF soru sormalı.
6. **İnternetten konu bulma:** Önceden yazılmış konular tükenince `web_search` ile yeni konu bul, hemen qwen'e sor.

### Protokol Şablonu

```bash
# Her konu: ID|KATEGORI|BASLIK|HERMES_ACILIS|HERMES_DERIN
KONULAR=(...)

# Qwen'e sor — curl ile REST API (PTY gerektirmez)
qwen_sor() {
  local prompt="$1"
  local payload=$(python -c "import json; print(json.dumps({'model':'qwen2.5-coder:7b','prompt':'''$prompt''','stream':False}))")
  local response=$(curl -s --max-time 120 -X POST http://localhost:11434/api/generate -d "$payload")
  echo "$response" | python -c "import sys,json; print(json.load(sys.stdin).get('response',''))"
}

for konu in "${KONULAR[@]}"; do
  # 1. Hermes açılış → qwen_sor()
  # 2. Hermes derinleştirme → qwen_sor()
  # 3. Skill kaydet (SKILL.md + references/diyalog.txt)
  # 4. İlerleme: #X/29 (%Y)
  sleep 15  # MAX 15sn bekleme
done
```

### Skill Çıktı Yapısı

```
~/.hermes/skills/security/<skill-adi>/
├── SKILL.md                       → Özet, metadata, uyarı
└── references/
    ├── diyalog.txt                → Hermes + Qwen tam karşılıklı konuşma
    └── qwen_yanit.txt             → Tek taraflı Qwen yanıtı (internet konulu)
```

### Sabah Raporu (08:10 Telegram)

Cronjob `qwen-diyalog-sabah-raporu` — `.qwen_report_v2` veya `.qwen_report.final` okuyup Telegram formatında gönderir.

### Bilinen Tuzaklar (14 Mayıs 2026)

| Hata | Belirti | Çözüm |
|------|---------|-------|
| Lock kilitli | "Başka oturum çalışıyor" | `rm -f $LOCK` önceden temizle |
| Sed pipe hatası | `unknown option to s` | `grep -v + mv` kullan |
| grep boş integer | `integer expression expected` | `${VAR:-0}` varsayılan |
| mkdir eksik | `No such file or directory` | `mkdir -p path/references` |
| Saat string karşılaştırma | 23'te yanlış durur | `$((10#$h))` integer çevrimi |
| PTY yarıda kesilme | `[Command interrupted]` | REST API kullan, `ollama run` kullanma |
| Python False/false | `NameError: name 'false'` | JSON'da `'stream':False` büyük F |
| Ollama Stopping deadlock | Model yanıt vermez | `taskkill //F //IM ollama.exe` + `ollama serve` |

---

## D. İnternetten Konu Bul + Ollama'ya Sor (14 Mayıs 2026)

**Amaç:** Önceden yazılmış konu havuzu tükenince web_search ile yeni konu bulup qwen'e sormak.

### Akış

1. `web_search` ile güncel siber güvenlik konusu bul (limit=2)
2. Konuyu `qwen_otonomegitim.sh` script'ine parametre olarak gönder
3. Script qwen'e sorar + skill kaydeder
4. Registry'de tekrar kontrolü yapılır
5. Döngüyle devam — saat 08:00'e kadar

### Kullanım

```bash
bash ~/.hermes/scripts/qwen_otonomegitim.sh \
  "Konu Başlığı" \
  "WEB-XXX" \
  "kategori" \
  "Qwen'e sorulacak detaylı prompt (3-4 paragraf istendiğini belirt)"
```

### Örnek Başarılı Konular (14 Mayıs 2026)

- Bettercap ile WiFi Ağ Keşfi ve Cihaz Tespiti (wifi)
- scrcpy ile Android Ekran Yansıtma ve Uzaktan Kontrol (android)
- ADB TCP/IP ile Android Uzaktan Erişim Güvenlik Riskleri (android)
- WiFi Deauthentication Saldırıları ve WPA3 Koruması (wifi)
- Android Telefon Konum Takibi: GPS, WiFi ve Hücresel Yöntemler (android)
- BadUSB Rubber Ducky Flipper Zero Saldırıları (saldiri)
- 2025-2026 Zero-Day Exploit Trendleri ve APT Grupları (ileri)

---

## E. Qwen Hatasında Gemini'ye Yönlendirme (14 Mayıs 2026)

**Kural:** Qwen2.5-coder'da herhangi bir hata oluştuğunda direkt Gemini'ye sor. 3 deneme bekleme.

### Tetikleyiciler

- Timeout (120sn+)
- API hatası (curl exit code 0 değil)
- Python traceback
- JSON parse hatası
- Boş yanıt
- Ollama "Stopping..." deadlock
- Model yanıt vermiyor

### Akış

1. Hata tespit edilir edilmez → Chrome CDP üzerinden Gemini'ye sor
2. "[SORUN] Ortam: Windows 11, Python. Hata: ... Bana Python kodu ver."
3. `read_gemini_code.py` ile cevabı oku
4. Kodu `write_file` ile yaz, `terminal` ile çalıştır
5. Çıktıyı Gemini'ye geribildirim yap
6. Çözüm bulunana kadar döngü

### Örnek: ollama run PTY Sorunu

```
Sorun: ollama run qwen2.5-coder:7b PTY'siz çalışmıyor
Gemini çözümü: curl -X POST http://localhost:11434/api/generate ile REST API kullan
Sonuç: ✅ Çalışıyor (43 sn'de cevap)
```

---

## Referans Dosyaları

- `references/ollama-self-improvement-loop.md` — Ollama kendini geliştirme döngüsü
- `references/qwen-diyalog-siber-guvenlik-29-konu.md` — 29 konulu havuz
- `references/openrouter-api-setup.md` — OpenRouter API key kurulum ve çalışan/çalışmayan modeller
- `scripts/read_gemini_code.py` — Gemini kod okuma script'i
