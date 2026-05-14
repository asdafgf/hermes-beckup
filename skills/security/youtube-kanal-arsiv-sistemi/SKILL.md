---
name: youtube-kanal-arsiv-sistemi
description: "Büyük YouTube kanallarını (1.000+ video) tarar, kategorize eder, transcript'lerini çeker ve sistematik öğrenim arşivi oluşturur. John Hammond / RootOfTheNull pipeline'ından türetilmiştir."
version: 2.0
author: hermes
category: security
tags: [youtube, archive, transcript, categorization, learning-path, channel-scan]
---

# 📦 YouTube Kanal Arşiv Sistemi

## 🎯 Ne Zaman Kullanılır

- **Büyük bir YouTube kanalının** tüm videolarını taramak istediğinde
- **500+ videoluk** bir kanalı kategorize edip doküman haline getirmek istediğinde
- **Toplu transcript çekimi** yapılması gerektiğinde
- **Sistematik öğrenim arşivi** oluşturmak istediğinde
- **Aynı anda birden çok kanalı** arşivlemek gerektiğinde

---

## 🔧 Pipeline Adımları

### Adım 1: Tüm Video Metadata'sını Çek
```bash
yt-dlp --flat-playlist --dump-json "https://www.youtube.com/@KANAL_ADI/videos" > kanal_videolari.json
```

`--flat-playlist`: Sadece metadata çeker (video indirmez)
`--dump-json`: JSON formatında çıktı
`n_entries` alanı toplam video sayısını verir

### Adım 2: Doğrulama
Python ile playlist index'lerini kontrol et:
```python
import json
with open('kanal_videolari.json') as f:
    videos = [json.loads(line) for line in f]
print(f"Toplam: {len(videos)} video")
indices = [v['playlist_index'] for v in videos]
print(f"Index aralığı: {min(indices)} - {max(indices)}")
# Eksik var mı?
expected = set(range(1, len(videos)+1))
actual = set(indices)
print(f"Eksik: {expected - actual}")
```

### Adım 3: Kategorizasyon
Anahtar kelime tabanlı kategorizasyon yap:
```python
categories = {
    "kategori_adi": ["keyword1", "keyword2", ...],
}
for v in videos:
    title_lower = v['title'].lower()
    matched = set()
    for cat, keywords in categories.items():
        if any(kw in title_lower for kw in keywords):
            matched.add(cat)
    v['cats'] = matched if matched else {"other"}
```

### Adım 4: Kategori Dokümanlarını Oluştur
Her kategori için ayrı `.md` dosyası:
```
arsiv/
├── dokumanlar/ANA_KATALOG.md     # Tüm videolar (kategorili, linkli)
├── kategoriler/kategori_adi.md    # Her kategori ayrı
├── transcriptler/                 # .srt transcript'ler
└── KULLANIM_KILAVUZU.md
```

### Adım 5: Transcript Çekme (Batch)
Batch script'i oluştur ve background'a at:
```bash
# Öncelikli batch (malware, phishing, AI gibi kritik kategoriler)
yt-dlp --write-auto-sub --sub-lang en --skip-download --convert-subs srt \
  -o "%(id)s" --batch-file oncelikli.txt \
  --sleep-requests 2 --min-sleep-interval 3 --max-sleep-interval 5
```

> **⚠️ ÖNEMLİ:** `--sleep-requests` OLMADAN `--min-sleep-interval` kullanma!
> `--sleep-requests` zorunludur, aksi halde hata alırsın.
> 25'şerli batch'ler halinde çek, aralıklı çalıştır (YouTube rate limit).
> Her videoda çıkan "No supported JavaScript runtime" WARNING'i normaldir — göz ardı edilebilir, transcript yine de çekilir.

### Adım 6: Skill Oluştur
Arşivin kullanım amacını tanımlayan bir Hermes skill'i oluştur:
- Arşivin amacı (öğrenim, vaka çalışması, teknik beceri)
- Dosya yapısı
- Nasıl kullanılacağı
- Öğrenim rotaları

---

## 📁 Çıktı Dizin Yapısı
```
~/Desktop/kanal_arsivi/
├── dokumanlar/
│   ├── ANA_KATALOG.md
│   └── KULLANIM_KILAVUZU.md
├── kategoriler/
│   ├── kategori1.md
│   ├── kategori2.md
│   └── ...
├── transcriptler/
│   ├── cekme_yoneticisi.sh     # Batch yönetici script
│   ├── cekme_log.txt            # Çekim log'u
│   ├── tum_linkler.txt          # Tüm video linkleri
│   ├── batch_oncelikli.txt      # Öncelikli video listesi
│   ├── batch_diger.txt          # Düşük öncelik listesi
│   ├── VIDEO_ID1.en.srt
│   └── VIDEO_ID2.en.srt
├── skills/                     # Buradan türetilen skill'ler
└── kanal_videolari.json        # Tüm metadata
```

---

## ⚙️ Background Transcript Çekme Stratejisi

### yt-dlp PATH Sorunu (Windows)
yt-dlp `pip install` ile gelir ama PATH'e eklenmeyebilir:
```bash
# Önce yt-dlp'nin nerede olduğunu bul
find /c/Users/kullanici -name "yt-dlp*" -type f 2>/dev/null
# veya
which yt-dlp

# Background process'te MUTLAKA full path kullan
YTDLP="/c/Users/kullanici/temp-watch-youtube/Watch_Youtube_Skill/.venv/Scripts/yt-dlp"
```
> ⚠️ Background process (`terminal` ile `background=true`) PATH'i inherit ETMEZ! Full path zorunludur.

### Batch Script Template
```bash
#!/bin/bash
# TRANSCRIPT ÇEKME YÖNETİCİSİ
cd /c/Users/eymen/Desktop/KANAL_ARSIVI/transcriptler
YTDLP="/c/Users/eymen/temp-watch-youtube/Watch_Youtube_Skill/.venv/Scripts/yt-dlp"
BATCH="tum_linkler.txt"
TOPLAM=$(wc -l < "$BATCH")
BATCH_SIZE=25
LOG="cekme_log.txt"

echo "=== TRANSCRIPT ÇEKİMİ ===\n" > "$LOG"
date >> "$LOG"

for ((start=1; start<=TOPLAM; start+=BATCH_SIZE)); do
  end=$((start + BATCH_SIZE - 1))
  [ $end -gt $TOPLAM ] && end=$TOPLAM
  batch_no=$(( (start - 1) / BATCH_SIZE + 1 ))
  total_batches=$(( (TOPLAM + BATCH_SIZE - 1) / BATCH_SIZE ))
  
  echo "=== Batch $batch_no/$total_batches ($start-$end) ===" >> "$LOG"
  
  "$YTDLP" --write-auto-sub --sub-lang en --skip-download --convert-subs srt \
    -o "%(id)s" \
    --batch-file "$BATCH" \
    --playlist-start "$start" --playlist-end "$end" \
    --sleep-requests 2 --min-sleep-interval 3 --max-sleep-interval 5 \
    2>&1 | tail -5 >> "$LOG"
  
  echo "Batch $batch_no/$total_batches OK" >> "$LOG"
  sleep 3
done

echo "" >> "$LOG"
echo "TAMAM — $(ls *.srt 2>/dev/null | wc -l) transcript" >> "$LOG"
date >> "$LOG"
```

### Background'a At ve Haber Ver
```bash
terminal(command="bash cekme_yoneticisi.sh", background=true, notify_on_complete=true, timeout=600)
```
Kullanıcıya "bitince haber veririm" de, `notify_on_complete=true` ile tool sonucu gelir.

### Çoklu Kanal Yönetimi
Her kanal ayrı klasör, ayrı background process:
```bash
mkdir -p ~/Desktop/{kanal1_arsiv,kanal2_arsiv}/{dokumanlar,kategoriler,transcriptler}
```

Aynı anda 3 kanala kadar transcript çekilebilir (YouTube rate limit paylaşılmaz çünkü farklı hedef URL'ler):
- 🟢 John Hammond (412 öncelikli)
- 🟠 NetworkChuck (372)
- 🔴 David Bombal (1.483)
Her biri ayrı batch script'i ile bağımsız çalışır.

### Process Kill ve Yeniden Başlatma
Bir background process hatalı parametreyle başlatıldıysa:
1. `process(action="kill", session_id="...")` ile öldür
2. Düzeltilmiş script'i yeni `terminal(background=true)` ile başlat
3. Eski process'in `exit_code -15` (SIGTERM) dönmesi normaldir — sorun değil

### İlerleme Takibi
Background process çıktısı doğrudan görünmez (pipe ile log'a yönlendirilir):
```bash
# Log'dan kontrol
tail -20 transcriptler/cekme_log.txt

# Kaç .srt dosyası var?
ls transcriptler/*.srt 2>/dev/null | wc -l

# Toplam boyut
du -sh transcriptler/*.srt 2>/dev/null | tail -3
```

### Öncelikli vs Tam Çekim
```python
# Önce kritik kategorilerden başla
priority_keywords = ["malware", "phishing", "ai", "hack", "exploit",
                     "windows", "linux", "burp", "nmap", "metasploit"]
```

---

## 🔄 Transcript → Skill Pipeline v5 (AKTİF)

Transcript'ler çekildikçe **otomatik skill'e dönüştüren** pipeline. **Hiçbir şey sormaz, direkt yapar.**

### Mimari (v5)

```
SRT dosyası
  → extract_clean_text()  (SRT timestamp'leri temizle, ASR tekrarlarını kaldır)
  → Gemini API'ye sor     (tek deneme, 429'da hemen geç)
  → OpenRouter'a sor      (GPT-4o-mini, ana kaynak)
  → Ollama'ya sor         (qwen2.5-coder:7b, sınırsız)
  → Ollama'ya sor         (gemma4:latest, alternatif)
  → Fallback              (transcript özeti, hiçbiri çalışmazsa)
  → En iyi yanıtı seç     (daha uzun/detaylı olan)
  → SKILL.md yaz          (security kategorisi altına)
  → processed_ids.txt'ye ekle (tekrar işleme)
```

### Cronjob
- `otomatik-skill-uretici` → her 5 dk'da bir çalışır
- Script: `~/.hermes/scripts/otomatik_skill_uretici_v4.py`
- Tüm kanalları tarar, yeni transcript'leri bulur, skill'e çevirir
- Asla kullanıcıya sormaz — direkt yapar

### Çoklu API Sıralaması (v5, AKTİF)
Pipeline sırayla dener, ilk başarılı yanıtı kullanır. **Her API tek deneme yapar — başarısız olursa hemen sıradakine geçer** (bekleme yok):

| Sıra | Kaynak | Model | Limit | Not |
|------|--------|-------|-------|-----|
| 1 | Gemini API | gemini-2.0-flash | Kota (günlük) | 429 alınırsa retry YOK, hemen geç |
| 2 | OpenRouter | GPT-4o-mini | Kredi bazlı | Çoğu API çağrısını bu karşılar |
| 3 | Ollama (yerel) | qwen2.5-coder:7b | Sınırsız | API'ler çökerse devreye girer |
| 4 | Ollama (alternatif) | gemma4:latest | Sınırsız | qwen2.5 başarısız olursa yedek |
| 5 | Fallback | Keyword-based | Yok | Transcript'ten manuel skill üret |

**⚠️ Hayati performans kuralı:** Hiçbir API çağrısında 3 kez retry yapma. Gemini kota doluyken 10+20+30=60 saniye beklemek script'in 120s timeout'unda çökmesine yol açar. Her API tek deneme yapar, başarısızsa hemen sıradaki API'ye veya fallback'e geçer.

### API Model Adları (OpenRouter)
OpenRouter model ID'leri zamanla değişir. **Doğru model adı almak için:**
```bash
curl -s "https://openrouter.ai/api/v1/models" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  | python -c "import sys,json; d=json.load(sys.stdin); [print(m['id']) for m in d.get('data',[]) if 'sonnet' in m['id'].lower()]"
```
Bilinen geçerli modeller (Mayıs 2026):
- `anthropic/claude-sonnet-4.6` (en güncel)
- `anthropic/claude-sonnet-4.5`
- `anthropic/claude-sonnet-4`
- `openai/gpt-4o-mini` (ucuz, hızlı, mevcut pipeline'da kullanılıyor)

**⚠️ `anthropic/claude-sonnet-4-20250514` GEÇERSİZDİR** — OpenRouter bu model ID'sini tanımaz, 400 Bad Request döner. Kullanma.

### Gemini API URL Hatası (Yaygın Tuzak)
Python f-string'te API key'i placeholder olarak bırakma:
```python
# YANLIŞ — key gönderilmez, her zaman hata alınır:
url = f"https://generativelanguage.googleapis.com/v1beta/models/.../generateContent?key=***"

# DOĞRU:
url = f"https://generativelanguage.googleapis.com/v1beta/models/.../generateContent?key={GOOGLE_API_KEY}"
```
Script düzenlenirken `***` placeholder'ı fark edilmezse Gemini hiç çalışmaz ve sessizce fallback'e düşer. Değişiklik yaparken MUTLAKA kontrol et.

### Script Sürüm Kirliliği
`otomatik_skill_uretici_v4.py` dosyası zamanla **v5 içeriğiyle** değiştirilir (Ollama desteği eklendiğinde). Dosya adı `v4` kalsa da içerik `v5` olabilir. Eğer script beklendiği gibi çalışmıyorsa:
1. İlk 5 satırda başlık/versiyon bilgisini kontrol et
2. `def ask_ollama` fonksiyonu varsa v5 kullanılıyor demektir
3. Gemini URL'sinde `***` placeholder'ı olup olmadığını kontrol et

### API Key Sızıntısı Önleme
API key'ler PowerShell User değişkeninde saklanır, asla SKILL.md veya memory'ye yazılmaz:
```python
def get_api_key(name):
    v = os.environ.get(name, "")
    if v: return v
    import subprocess
    r = subprocess.run(["powershell.exe", "-Command",
        f"[System.Environment]::GetEnvironmentVariable('{name}','User')"],
        capture_output=True, text=True, timeout=5)
    return r.stdout.strip()
```

### Anahtar Kelime Havuzu (Fallback)
```python
terms = [
    r'\bmalware\b', r'\bransomware\b', r'\bphishing\b', r'\bexploit\b',
    r'\bpayload\b', r'\bbackdoor\b', r'\btrojan\b', r'\bkeylogger\b',
    r'\bc2\b', r'\bcommand.{0,20}control\b', r'\binfostealer\b',
    r'\bdropper\b', r'\bpowershell\b', r'\bpython\b', r'\bbash\b',
    r'\blinux\b', r'\bwindows\b', r'\bactive directory\b', r'\bentra\b',
    r'\bazure\b', r'\baws\b', r'\bcloud\b', r'\bdocker\b',
    r'\bnmap\b', r'\bmetasploit\b', r'\bburp\b',
    r'\bsql injection\b', r'\bxss\b', r'\brce\b',
    r'\bprivilege escalation\b', r'\bpersistence\b',
    r'\bcredential\b', r'\bpassword\b', r'\bmfa\b', r'\b2fa\b',
    r'\bvpn\b', r'\btor\b', r'\bdark web\b', r'\bencryption\b',
    r'\bsupply chain\b', r'\bnpm\b', r'\bdependency\b',
    r'\bai\b', r'\bgpt\b', r'\bllm\b', r'\bprompt injection\b', r'\bmcp\b',
    r'\bwireshark\b', r'\bfirewall\b', r'\bsiem\b', r'\bwazuh\b',
    r'\bthreat hunting\b', r'\bforensic\b', r'\bdfir\b',
    r'\bctf\b', r'\bhackthebox\b', r'\btryhackme\b',
    r'\bwindows firewall\b', r'\blsass\b', r'\bmimikatz\b',
    r'\bntlm\b', r'\bkerberos\b', r'\bbloodhound\b', r'\bresponder\b',
    r'\bgolang\b', r'\bcursor\b', r'\bcopilot\b', r'\bcodex\b',
]
```

### Skill İsmi Üretme Kuralları (Fallback)
```python
# 1. Keyword'lerden dene (en iyi sonuç)
if keywords:
    name = '-'.join(keywords[:3])
    name = re.sub(r'[^a-z0-9-]', '', name.lower())

# 2. Cümle başlığından dene (keyword yoksa)
#    Ama şu giriş kalıplarını ATLA:
skip_patterns = [
    r'^hey\b', r'^all right', r'^alrighty', r'^hello\b',
    r'^well hey', r'^before dive', r'^what.s\b', r'^righty'
]
#    Bunlar tespit edilirse 2. cümleye geç
```

### Skill İsmi Temizleme (Anlamsızları Silme)
Pipeline anlamsız skill isimleri üretebilir (`all-righty`, `hey-everyone`). Bunları temizlemek için:

```python
import os, shutil, re

skills_dir = '/c/Users/eymen/AppData/Local/hermes/skills/security'

# Anlamsız kalıplar
garbage_patterns = [
    r'^music[\- ]', r'^hey[\- ]', r'^hello[\- ]', r'^alrighty',
    r'^all[\- ]?right', r'^well[\- ]hey', r'^thanks[\- ]much',
    r'^before[\- ]dive', r'^guys[\- ]', r'^everyone[\- ]',
    r'^whats[\- ]going', r'^hows[\- ]going', r'^righty[\- ]',
    r'^for[\- ]later', r'^this[\- ]video', r'^lets[\- ]',
    r'^gonna[\- ]', r'^okay[\- ]', r'^so[\- ]',
    r'^now[\- ]again', r'^short[\- ]video', r'^just[\- ]',
    r'^alrighty$', r'^all[\- ]right$', r'^python$',
    r'^theres[\- ]', r'^ill[\- ]start', r'^weve[\- ]now',
]

def is_garbage(name):
    for pattern in garbage_patterns:
        if re.search(pattern, name.lower()):
            return True
    if len(name) < 4:
        return True
    return False

for skill_name in os.listdir(skills_dir):
    if is_garbage(skill_name):
        shutil.rmtree(os.path.join(skills_dir, skill_name))
```

**2. aşama:** Anlamlı keyword içermeyenleri sil (sadece giriş cümlelerinden oluşanları):
```python
meaningful_keywords = ['malware', 'ransomware', 'phishing', 'exploit', 'payload',
    'backdoor', 'trojan', 'windows', 'linux', 'bash', 'python', 'powershell',
    'active', 'entra', 'azure', 'network', 'firewall', 'cisco', 'ccna',
    'ai', 'gpt', 'cloud', 'docker', 'kubernetes', 'ctf', 'hack', ...]

def is_meaningful(name):
    name_lower = name.lower().replace('-', '')
    return any(kw.replace('-', '') in name_lower for kw in meaningful_keywords)
```

> ⚠️ **ÖNEMLİ:** `siber-guvenlik-*` ve `john-hammond-siber-guvenlik-arsivi` gibi özel skill'leri korumak için `protected` listesi kullan.

### Pipeline'ı Çalıştırma
```bash
# Single run
cd /c/Users/eymen/Desktop/transcript_skills && python3 pipeline_v2.py

# Background sürekli çalışma
terminal(
  command="cd /c/Users/eymen/Desktop/transcript_skills && python3 pipeline_v2.py",
  background=True, notify_on_complete=True, timeout=600
)
```

### Çıktı
Her işlenen video için `~/AppData/Local/hermes/skills/security/<anlamli-isim>/SKILL.md`

### İzleme
```python
# processed_ids_v4.txt ile işlenenler takip edilir
# Aynı video 2 kere işlenmez
# 3 kanaldaki tüm .srt'leri tarar: john-hammond, networkchuck, david-bombal
```

---

## 💡 Püf Noktaları

### YouTube Rate Limit Koruması
- `--sleep-requests 2` → her istek arası 2 sn
- `--min-sleep-interval 3` → minimum bekleme
- `--max-sleep-interval 5` → maksimum bekleme
- **25'şerli batch** idealdir
- Batch'ler arası **5-10 sn** bekle

### Kategorizasyon İpuçları
- Title-based matching yeterli (description gerekmez)
- Türkçe kanallar için Türkçe keyword'ler ekle
- `other` kategorisi kaçınılmazdır (tüm videolar kategorize OLABİLİR değil)
- Her kategori için **en önemli 20 video** ayrı listelenebilir
- Kanalın içerik profiline göre keyword'leri ayarla:
  - **John Hammond:** malware analizi, phishing, CTF ağırlıklı
  - **NetworkChuck:** CCNA, kariyer, AI otomasyonu ağırlıklı
  - **David Bombal:** Python hacking, CCNA, röportaj ağırlıklı

### yt-dlp PATH Sorunu
Windows'ta yt-dlp genelde `pip install yt-dlp` ile gelir ama PATH'te olmayabilir:
```bash
# Doğru yolu bul
find /c/Users/kullanici -name "yt-dlp*" -type f
# veya
which yt-dlp
```

### JS Runtime Uyarısı
Her videoda şu uyarı çıkar:
```
WARNING: No supported JavaScript runtime could be found.
```
Bu **normaldir**, transcript yine de çekilir. Deno yüklemeye gerek yok.

### Kullanıcıya İlerleme Bildirimi
Kullanıcı "sıkıntı mı çıktı" gibi sorular sorabilir. Panik yapma:
1. `process(action="poll")` ile durumu kontrol et
2. Devam ediyorsa "sorun yok, çalışıyor" de
3. Çıktıyı log'dan oku (process log'u boşsa log dosyasına bak)

---

## 🔗 İlgili Skill'ler
- watch-youtube — Tek video analizi (bu skill onun kanal-çapı versiyonu)
- john-hammond-siber-guvenlik-arsivi — John Hammond özel arşivi (1.602 video)

## 🕰️ Eski Videoları Bulma Stratejisi

Bir kanalın eski videolarına erişmek (`--dateafter` olmadan yt-dlp en son 50 videoyu döner):

```bash
# 2020 öncesi videoları bul
yt-dlp --dateafter 20200101 --flat-playlist --dump-json \
  "https://www.youtube.com/@KANAL/videos" 2>/dev/null | \
  python -c "import sys,json; [print(f\"{json.loads(l)['id']}\") for l in sys.stdin]" \
  > eski_videolar.txt

# --dateafter ile batch çekim
"$YTDLP" --write-auto-sub --sub-lang en --skip-download --convert-subs srt \
  -o "%(id)s" --batch-file eski_videolar.txt \
  --sleep-requests 2 --min-sleep-interval 3 --max-sleep-interval 5
```

**⚠️ Bilinen tuzak:** yt-dlp `--flat-playlist --dump-json` kanal URL'sine ilk çağrıda yalnızca ~50 video döner. `--dateafter 20200101` ile eski videolara ulaşılır. `--dateafter 20150101` daha da eski videoları getirir.

Eğer bir kanal uzun süredir yeni transcript eklemiyorsa (ör. john-hammond %27'de takılı):
1. `--dateafter 20200101` ile eski videoları bul
2. Batch'e ekle
3. `--playlist-end 50` ile sınırla, sonra bir sonraki turda kalanını çek

## 📜 Referans Dosyalar
- `references/john-hammond-kategorileri.md` — John Hammond kategori eşleştirme tablosu (1.602 video, 21 kategori)
- `references/networkchuck-kategorileri.md` — NetworkChuck kategori eşleştirme tablosu (372 video, 12 kategori)
- `references/davidbombal-kategorileri.md` — David Bombal kategori eşleştirme tablosu (1.483 video, 13 kategori)
- `references/asr-transcript-cleaning.md` — YouTube ASR transcript'lerdeki tekrarları temizleme ve skill ismi oluşturma notları
- `references/pipeline-v3-api-integration.md` — Detaylı API entegrasyon notları (model adları, performans ipuçları, retry stratejileri)
- `scripts/cekme_yoneticisi.sh` — Batch transcript çekme script'i
- `scripts/otomatik_skill_uretici_v4.py` — Otomatik skill üretme script'i (v5 içeriğiyle güncellenmiştir)
