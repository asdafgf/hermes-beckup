---
name: ollama-sohbet
title: "Ollama Yerel Model ile Araştırma Odaklı Çok Turlu Sohbet"
description: "Hermes'in Ollama'daki yerel modellerle (gemma4:31b, gemma4:latest, hermes3, mistral, vb.) internetten topladığı güncel verilerle besleyerek belirli bir konuda çok turlu, karşılıklı tartışma yürütmesi. Kullanıcı terminalden canlı izler. Her model için ayrı script + PTY/timeout yönetimi."
category: software-development
---

# Ollama Yerel Model ile Araştırma Odaklı Çok Turlu Sohbet

**Amaç:** Kullanıcı, Ollama'daki yerel bir modelle (ör. gemma4:latest, gemma4:31b, hermes3, mistral) belirli bir konuda (finans, politika, teknoloji, siber güvenlik) güncel verilerle beslenmiş, çok turlu bir sohbet yapmak ister. Kullanıcı terminalden canlı izler, ben konuşmayı yönlendiririm.

## ALTIN KURAL: İlk yapılacak şey ilgili skill'i yükle

Kullanıcıdan net talimat: **Her işleme başlamadan önce, sorunun kategorisini belirle, en ilgili skill'i bul, skill_view ile yükle, skill içinde çözüm varsa uygula, yoksa kendi yöntemini kullan.** Sormadan, her zaman yapılır.

Örnek: hata çözümü gerekiyorsa -> once hata-cozum-ollama veya hata-cozum-dongusu skill'ini yukle. Siber güvenlik sorusu -> once ilgili siber-guvenlik-* skill'ini yukle.

## Ne Zaman Kullanılır

- Kullanıcı "hermes ollama içindeki AI ile sohbet etsin" veya "ollama'daki modele sor" dediğinde
- Kullanıcı "X konusunda kullanıcıyı da dahil ederek karşılıklı tartışın" dediğinde
- Kullanıcı "internetten veri alarak X hakkında sorular sorsun, ben cevapları izleyeyim" dediğinde

## Adımlar

### 1. Modeli Seç

```bash
ollama list
```

Kullanıcı belirtmemişse:
- **Hızlı sohbet:** `gemma4:latest` (9.6 GB, 4B parametre) — 120sn timeout yeterli
- **Derin analiz:** `gemma4:31b` (19 GB) — 180sn+ gerekebilir, PTY'de takılabilir
- **Orta yol:** `hermes3:latest` (4.7 GB) veya `mistral:latest` (4.4 GB)
- **Türkçe destek:** gemma4:latest genelde Türkçe cevap verir

### 2. Güncel Verileri Topla (ARAŞTIRMA ADIMI — ATLANAMAZ)

Sohbetin konusuyla ilgili en güncel verileri topla:

```bash
# 1. Google araması
web_search(query="<konu> 2026", limit=5)

# 2. Haber/veri sitelerinden extract
web_extract(urls=["https://tradingeconomics.com/commodity/gold"])
```

**Sakla bunları:** Sayısal veriler (fiyat, yüzde, tarih), haber başlıkları, neden-sonuç ilişkileri. Modelin cevaplarını zenginleştirmek için prompt'a göm.

### 3. Sohbet Script'ini Hazırla

**KRİTİK KURAL:** Doğrudan `ollama run <model>` komutunu tek satırda yollama. Şu sorunlar var:
- Türkçe karakterler (ş, ç, ü, ğ, ö, ı) bash'ta sorun çıkarır
- Tek tırnak/çift tırnak iç içe geçer
- PTY modu uzun cevapları yarıda kesebilir

**DOĞRU YÖNTEM:** Geçici bir `.sh` dosyasına yaz, sonra çalıştır.

```bash
#!/bin/bash
# /tmp/<konu>_chat.sh

MESSAGE="<modelin cevaplamasını istediğin soru/metin>"
echo "$MESSAGE" | ollama run <model-adi> 2>/dev/null
```

Dosyayı oluştur: `write_file(content=..., path="/tmp/<konu>_chat.sh")`
Çalıştır: `chmod +x /tmp/<konu>_chat.sh`

### 4. Çalıştırma Modları

#### Mod A: PTY (Canlı İzleme) — Kullanıcı cevapları terminalde canlı görmek isterse

```bash
/tmp/<konu>_chat.sh
```
`pty=true` ile çalıştır. **Risk:** PTY uzun cevaplarda yarıda kesilebilir (timeout veya buffer overflow).

#### Mod B: Normal (Tam Cevap) — Kullanıcı sadece sonucu görmek isterse

```bash
/tmp/<konu>_chat.sh
```
`pty=false`, `timeout=120-180s` ile çalıştır. Cevap tam gelir ama canlı izlenmez.

### 5. Çok Turlu Sohbet Yönetimi

Her turda yeni bir `.sh` dosyası oluştur (aynı dosyayı üzerine yazma — önceki cevabı kaybetme):

| Tur | Dosya | İçerik |
|---|---|---|
| 1 | `/tmp/<konu>_chat.sh` | İlk soru + güncel veriler |
| 2 | `/tmp/<konu>_q2.sh` | Cevaba dayalı takip sorusu |
| 3+ | `/tmp/<konu>_q3.sh` | Daha derin / spesifik soru |

**Her turda:** Topladığın verilerden referans ver, modelin cevaplarını sorgula (örn. "Söylediğin gibi ama verilere göre X...")

### 6. Kullanıcıya Raporla

Her turdan sonra kullanıcıya modelin cevabını özetle:

```
Model <adı> cevap verdi:

[Öne çıkan noktalar — 3-5 madde]

Bir sonraki soruyu soruyorum...
```

## Yeni Model Yükleme

Ollama'ya yeni model çekerken:

```bash
# Modeli indir (arka planda spinner + progress bar gösterir)
ollama pull qwen2.5-coder:7b-instruct-q4_K_M

# İndirme tamamlanınca listede görünür
ollama list | grep qwen2
```

- **İlerleme yüzdesi:** Terminal çıktısı canlı olarak `13%` gibi yüzde, indirilen MB, hız ve kalan süreyi gösterir. Kullanıcı bunu sorarsa normal terminal modunda (PTY değil) çalıştır.
- **Timeout:** 4.7 GB model ~5-6 MB/s hızla ~12-14 dk sürer. `timeout=600` (10 dk) ayarla.
- **Yarıda kesilen indirme:** Eğer kesilirse, kaldığı yerden devam eder (arka planda önbellek var). Tekrar `ollama pull` yeterli.
- **İndirme sonrası:** Model listede iki etiketle görünebilir: kısa ad (`qwen2.5-coder:7b`) ve tam ad (`qwen2.5-coder:7b-instruct-q4_K_M`). İkisi de aynı model.
- **Onay gerektirmez:** Kullanıcı "yükle ve aktif et" derse direkt çek, sorma.

## KRİTİK DÜZELTME (14 May 2026): `ollama run` YERİNE `curl REST API`

**`ollama run` PTY gerektirir ve background'da ÇALIŞMAZ.** Bu session'da 10+ kez test edildi ve doğrulandı. `ollama run` komutu çıktı olarak sadece Braille loading animasyonu (`⠋⠹⠸⠼`) döndürür, gerçek yanıt gelmez. Bunun yerine **Ollama REST API** kullan:

```bash
# DOĞRU YÖNTEM — curl ile REST API (PTY gerektirmez)
curl -s --max-time 120 -X POST http://localhost:11434/api/generate \
  -d "$(python -c "import json; print(json.dumps({'model':'qwen2.5-coder:7b','prompt':'Soru','stream':False}))")"

# Yanıtı parse et:
python -c "import sys,json; d=json.load(sys.stdin); print(d.get('response',''))"
```

**Streaming=False** kullan — streaming True ise her satır ayrı JSON olarak gelir, birleştirmek için döngü gerekir. `stream:False` ile tek JSON yanıt alırsın.

### qwen_sor() Şablon Fonksiyonu (Test Edildi ✅)

Bu session'da 30+ kez başarıyla çalıştırılan fonksiyon:

```bash
# Qwen'e sor — curl ile REST API (PTY gerektirmez, timeout+retry dahil)
qwen_sor() {
  local prompt="$1"
  local payload=$(python -c "import json; print(json.dumps({'model':'qwen2.5-coder:7b','prompt':'''$prompt''','stream':False}))" 2>/dev/null)
  
  local response=""
  for attempt in 1 2; do
    response=$(curl -s --max-time 120 -X POST http://localhost:11434/api/generate -d "$payload" 2>&1)
    if [ -n "$response" ]; then
      break
    fi
    echo "[RETRY $attempt]"
    sleep 3
  done
  
  echo "$response" | python -c "
import sys,json
try:
    d=json.load(sys.stdin)
    print(d.get('response',''))
except: pass" 2>/dev/null
}
```

**ÖNEMLİ:** Python `json.dumps` içinde `stream:False` yazma — Python `False` kullan (büyük F). `false` yazarsan `NameError: name 'false' is not defined` hatası alırsın.

### Ollama Deadlock Kurtarma

Model "Stopping..." state'inde takılırsa:

```bash
taskkill //F //IM ollama.exe 2>&1   # Tüm ollama process'lerini öldür
sleep 3
ollama serve 2>&1 &                 # Yeniden başlat
sleep 3
ollama ps                           # "Stopping..." kaybolmuş olmalı
```

Bazen 5-6 tane ollama.exe process'i olur. `taskkill //F //IM ollama.exe` hepsini öldürür.

### Skill Otomatik Kaydetme (qwen_otonomegitim.sh)

Bu session için geliştirilen protokol — internetten konu bul → qwen'e sor → skill olarak kaydet:

```bash
# ~/.hermes/scripts/qwen_otonomegitim.sh
# Kullanım: bash qwen_otonomegitim.sh "BASLIK" "KONU_ID" "KATEGORI" "PROMPT"
#
# Yaptığı:
# 1. Qwen API'ye prompt'u gönderir (curl)
# 2. Yanıtı kaydeder: ~/.hermes/skills/security/<skill-adi>/references/qwen_yanit.txt
# 3. SKILL.md oluşturur: ~/.hermes/skills/security/<skill-adi>/SKILL.md
# 4. Registry'ye kaydeder (tekrar kontrolü için)
# 5. Rapor dosyasına ekler
#
# Türkçe karakter temizleme: sed 's/ş/s/g;s/ğ/g/g;s/ü/u/g;...'
# Benzersiz ID sistemi: WEB-001, AND-101, KVK-001, PYT-101, HACK-001
```

## Bilinen Tuzaklar

1. **`ollama run` KULLANMA — curl kullan.** `ollama run` PTY gerektirir, background'da çalışmaz. Bu session'da 10+ kez kanıtlandı. Her zaman `curl -X POST http://localhost:11434/api/generate` kullan.

2. **JSON payload'da False vs false:** Python `json.dumps` ile `{'stream':False}` yaz (büyük F). `{'stream':false}` → NameError.

3. **Ollama "Stopping..." deadlock:** Model takılı kalırsa `taskkill //F //IM ollama.exe` + `ollama serve`. Sadece `ollama stop model_adi` yeterli olmaz.

4. **Lock dosyası kilitlenmesi:** Background script'ler lock dosyası bırakır. Yeni süreç başlatmadan önce `rm -f .qwen_lock` yap.

5. **Kullanıcı beklemekten nefret eder:** Konular arası max 15 saniye bekle. 4 dk bekleme koyarsan "ne bekliyorsun" diye bağırır. Her konu sonunda ilerleme yüzdesi göster (`%YUZDE=$((ISLENEN * 100 / TOTAL))`).

6. **Saat karşılaştırması:** `23 >= 8` kontrolü gece çalışmayı engeller. `$((10#saat))` ile integer'a çevir, gece aralığı için `[ saat -ge 23 ] || [ saat -lt 8 ]` kullan.

7. **grep -c boş string:** `grep -c 'pattern'` eşleşme yoksa boş döner, integer karşılaştırması patlar. `KOD=${KOD:-0}` ile koru.

8. **Bash yorumunda parantez = syntax error:** `# (KONU ADI)` yorumu bile bash tarafından alt-shell olarak yorumlanır. Script'te hiçbir yerde parantez kullanma.

9. **PTY yarıda kesilmesi:** PTY modu >60sn süren cevaplarda veya çok satırlı çıktılarda kill olabilir. Alternatif: Normal mod (pty=false) ile dene.

10. **Timeout:** Büyük modeller (31B) 180sn'de yetişmeyebilir. `timeout=300-600` yap veya daha küçük model kullan.

11. **Boş çıktı (sessiz fail):** Bazen output tamamen boş döner. Soruyu kısalt, `"Kisa cevap ver"` ekle ve tekrar dene.

12. **Türkçe karakter sorunu:** Script dosyası UTF-8 olarak yazılır (`write_file` ile sorun olmaz).

13. **Ardışık sorular:** Her turda yeni bir API çağrısı — model önceki konuşmayı hatırlamaz, prompt'da özet geçmelisin.

14. **Çıktı parse sorunu:** Model çıktısında `[Command interrupted]` varsa cevap yarıda kalmıştır. Aynı soruyu normal modda tekrar dene.

15. **Arka plan indirme vs PTY:** `ollama pull` spinner satırları PTY'de çok fazla çıktı üretir. Normal terminal modunda çalıştır.

### Otonom Overnight / Arkaplan Öğrenme Oturumu

**Amaç:** Bir Ollama modelini (örn. qwen2.5-coder:7b) gece boyunca (23:00 - 08:00) otonom olarak önceden belirlenmiş konuları işlemesi için çalıştırmak. Kullanıcı müdahalesi gerekmez — model kendi kendine sırayla konuları tartışır.

Detaylı protokol script: `skill_view('ollama-sohbet', 'scripts/qwen_otonomegitim.sh')`
Detaylı doğrulama script: `skill_view('ollama-sohbet', 'scripts/qwen_skill_dogrulama.sh')`
Detaylı diyalog protokolü: `skill_view('ollama-sohbet', 'scripts/qwen_diyalog_protokolu.sh')`

### Ne Zaman Kullanılır

- Kullanıcı "saat X'e kadar otonom öğrenme/tartışma oturumu başlat" dediğinde
- Kullanıcı "gece boyunca X modeli çalışsın, konuları işlesin" dediğinde
- Uzun süreli (4 saat+) arkaplan araştırma/tartışma gerektiğinde

### Adımlar

#### 1. Cronjob + Background PTY (İKİSİ BİRDEN)

En güvenilir yaklaşım: **hem cronjob** (her saat başı tetikleme) hem **background PTY süreci** (45dk aralıklarla konuları işleyen script).

```
Cronjob: saat başı tetikleme → kaçırılan adımları kurtarır
PTY:     canlı sürekli işleme → kullanıcı terminalde izleyebilir
```

#### 2. Script Hazırlama (KRİTİK: Bash Syntax Kuralları)

**UYARI:** Bash script'lerinde parantez `()` YORUM satirlarinda bile tehlikelidir. `# ===== (KONU BASLIGI) =====` gibi bir yorum satırı bash tarafından alt-shell olarak yorumlanır ve `syntax error near unexpected token` hatasına yol açar. Asla kullanma. Alternatif: köşeli parantez `[]`, tire `--`, veya hiç kullanma.

```bash
# YANLIŞ — syntax hatası:
# ============== KONU 1: AGENTIC AI (OTONOM AJANLAR) ==============

# DOĞRU:
# ============== KONU 1: AGENTIC AI - OTONOM AJANLAR ==============
```

Aynı şekilde `echo` içinde de parantez kullanma:
```bash
# YANLIŞ:
echo "=== KONU 3: Zero Trust (ZT) ==="

# DOĞRU:
echo "=== KONU 3: Zero Trust ==="
```

**Self-healing retry pattern.** Bu session'da geliştirilen ve test edilen yaklaşım:

```bash
#!/bin/bash
RETRY_FILE="/tmp/oturum_retry_count.txt"
MAX_RETRY=3

# Her soruyu 3 kez dene, başarısızsa Ollama'yı restart et
run_safe() {
  local question="$1"
  local label="$2"
  local retry=0

  while [ $retry -lt $MAX_RETRY ]; do
    echo "$question" | ollama run $MODEL 2>/dev/null
    local exit_code=$?
    if [ $exit_code -eq 0 ]; then
      echo 0 > "$RETRY_FILE"
      return 0
    fi
    retry=$((retry + 1))
    echo "[UYARI] $label — $retry/$MAX_RETRY basarisiz, yeniden..."
    sleep 5
  done

  # 3 kez basarisiz -> servisi restart et
  RETRY_COUNT=$(cat "$RETRY_FILE" 2>/dev/null || echo 0)
  RETRY_COUNT=$((RETRY_COUNT + 1))
  echo "$RETRY_COUNT" > "$RETRY_FILE"

  if [ $RETRY_COUNT -ge 3 ]; then
    echo "[KRITIK] 3 kez takilma — Ollama restart..."
    ollama serve 2>/dev/null &
    sleep 10
    echo 0 > "$RETRY_FILE"
  fi

  # Son bir deneme
  echo "$question" | ollama run $MODEL 2>/dev/null
}
```

**`$SAAT` degiskeni icin de dogru syntax:** `SAAT=$(date '+%H:%M')` — `$[...]` eski syntax'tir ve basarisiz olur.

Script template:

```bash
#!/bin/bash
# ~/.hermes/scripts/<oturum_adi>.sh

KONULAR=(
  "1. Konu başlığı. 3-4 paragraf analiz yap, sonunda [DEVAM] yaz."
  "2. Sonraki konu. Detaylı yorumla..."
)

for i in "${!KONULAR[@]}"; do
  echo "${KONULAR[$i]}" | ollama run <model-adi> 2>&1
  
  # Konular arası bekle (30-60 dk)
  if [ $i -lt $((${#KONULAR[@]} - 1)) ]; then
    sleep 2700  # 45 dk
  fi
done
```

#### 3. Cronjob Kurulumu

```bash
cronjob(name="<oturum-adi>", schedule="0 0,1,2,3,4,5,6,7 * * *", 
        repeat=8, deliver="origin",
        prompt="Şu an saat $(date '+%H:%M'). Sıradaki konuyu işle...")
```

#### 4. Background Süreç Başlatma (Canlı İzleme İçin)

```bash
terminal(command="bash ~/.hermes/scripts/<oturum_adi>.sh", 
         background=true, pty=true, notify_on_complete=true)
```

#### 5. Konu Listesi Şablonu (7 konu — gece oturumu için ideal)

1. {alan} trendleri / son gelişmeler
2. SLM vs büyük modeller karşılaştırması
3. {konu} AI asistanların geleceği
4. Açık kaynak vs kapalı kaynak karşılaştırması
5. Edge computing / local AI yükselişi
6. {alan} AI'ın rolü — yardımcı mı, ikame mi?
7. Meta-değerlendirme (modelin kendi yetenek/sınırlılıkları)

#### 6. İlerleme Takibi

Background sürecin durumunu kontrol et:

```bash
process(session_id="<proc_id>", action="poll")
```

Çıktı önizlemesinde hangi konuda olduğu ve saat görünür.

### Bilinen Tuzaklar (Otonom Session)

1. **PTY buffer taşması:** >500 satır çıktıda PTY yarıda kesilebilir. Çözüm: Script içinde `head -c 2000` veya kısa yanıt iste.
2. **Tekrarlayan çıktı:** Model aynı konuyu tekrar edebilir (loop). Çözüm: Prompt'a "Daha önce söylediklerini tekrar etme, yeni noktalara değin" ekle.
3. **Cronjob ile PTY çakışması:** İkisi de aynı modeli çağırırsa sırayla çalışır (Ollama queue). Sorun olmaz ama gecikme olabilir.
4. **Sabah bitiş kontrolü:** Cronjob 8 kez (00-07) çalışacak şekilde ayarlanır. Saat 08:00'de durur. Background PTY script'i de ~7 konuyu bitirdiğinde kendi durur.
5. **Model context kaybı:** Her `ollama run` çağrısı bağımsızdır — önceki konuşmayı hatırlamaz. Her prompt'a "Önceki konuda X demiştin. Şimdi Y konusuna geçiyoruz." ekleyerek bağlam kurabilirsin (ama cronjob'da bu ekstra iş yükü genelde değmez).
6. **Lock dosyası kilitlenmesi:** Birden çok çalıştırma aynı anda lock dosyası oluşturursa ikinci süreç "başka oturum çalışıyor" diye çıkar. Her restart öncesi `rm -f .qwen_lock` yap.
7. **İlerleme yüzdesi olmazsa kullanıcı "takıldın" sanar:** Her konu sonunda `%YUZDE=$((ISLENEN * 100 / TOTAL))` hesapla ve göster.
8. **Saat karşılaştırması hilesi:** `[ "$(date '+%H')" -ge 8 ]` string karşılaştırmasıdır, `23 >= 8` true döner. `$((10#saat))` ile integer'a çevir, 23-07 aralığını `[ saat -ge 8 ] && [ saat -lt 23 ]` olarak kontrol et.
9. **Qwen 2dk timeout:** Uzun prompt'larda qwen 30+ sn sürebilir. 2 dk timeout koy, yetmezse yeniden dene. Kullanıcı beklemekten nefret eder.
10. **grep -c bos string hatasi:** `KOD_KONTROL=$(echo "$cevap" | grep -c)`) eslesme yoksa bos string dondurur. `KOD=${KOD:-0}` ile varsayilan deger ver.
11. **Bash yorumunda parantez = syntax error:** `# (KONU ADI)` yorumu bile bash alt-shell olarak yorumlanir. Script'te hicbir yerde parantez kullanma — ne yorumda, ne echo'da.
12. **`$[komut]` eski syntax:** `SAAT=$[date '+%H:%M']` POSIX uyumlu degil. Her zaman `SAAT=$(date '+%H:%M')` kullan.
13. **sed ile parantez temizleme:** Script sonradan duzeltiliyorsa `sed -i 's/(/[/g; s/)/]/g' script.sh` calisir. Ama tercih edilen: bastan dogru yazmak.

14. **`sed` fonksiyon adlarindaki parantezleri de kirpar:** `run_safe() { ... }` tanimi `sed -i 's/(/[/g'` ile `run_safe[] { ... }` olur ve fonksiyon bulunamaz. `sed` ile parantez temizligi yaparken `grep -n '(' script.sh` ile once hangi satirlarda parantez oldugunu kontrol et. Fonksiyon tanim satirlarini (`run_safe()`) manuel olarak koru veya sed'i sadece yorum ve echo satirlarina uygula: `sed -i '/^#/ s/(/[/g; /^#/ s/)/]/g; /^echo/ s/(/[/g; /^echo/ s/)/]/g' script.sh`

15. **`run_safe` fonksiyon adina parantez koyma:** `function run_safe { ... }` veya `run_safe() { ... }` kullan. `run_safe[]` calismaz.

### Ornek: qwen2.5-coder:7b Gece Ogrenme Oturumu (13 Mayis 2026)

Detaylar: `skill_view('ollama-sohbet', 'references/qwen-gece-oturumu-13-mayis-2026.md')`

### Ornek: Siber Guvenlik Gece Oturumu (14 Mayis 2026)

Detaylar: `skill_view('ollama-sohbet', 'references/siber-guvenlik-gece-oturumu-14-mayis-2026.md')`

Bu oturumda 15 konu, ~90 soru gemma4:latest'e soruldu. Her konu ayri bir skill olarak kaydedildi. Olusturulan skill'ler: `skill_view('siber-guvenlik-agentic-ai')`, `siber-guvenlik-deepfake`, `siber-guvenlik-zero-trust`, `siber-guvenlik-tedarik-zinciri`, `siber-guvenlik-regulasyon`, `siber-guvenlik-ransomware`, `siber-guvenlik-api`, `siber-guvenlik-kuantum`, `siber-guvenlik-ctem`, `siber-guvenlik-kariyer`, `siber-guvenlik-sosyal-muhendislik`, `siber-guvenlik-siem-soar-xdr`, `siber-guvenlik-bulut`, `siber-guvenlik-iot-ot`, `siber-guvenlik-mobil`.

**Script:** `~/.hermes/scripts/qwen_gece_oturumu.sh` — 7 konu, 45dk aralık, PTY canlı.
**Cronjob:** Her saat başı (00-07) tetikleme, toplam 8 kez.
**İlk konu:** "Yapay zeka ve yazılım geliştirmede son trendler (2025-2026)"
**Son konu:** "Kendi yeteneklerin ve sınırlamaların hakkında meta-değerlendirme"
**Teslimat:** HTTP endpoint'e (bu sohbet + Telegram)

## Desteklenen Modeller (test edilen gemma4)

| Model | Boyut | Parametre | Hız | PTY Uyumu | Önerilen Kullanım |
|---|---|---|---|---|---|
| `gemma4:latest` | 9.6 GB | 4B | Hızlı | 120sn yeterli | Günlük sohbet |
| `gemma4:31b` | 19 GB | 31B | Yavaş | 300sn'de zor | Derin analiz, PTY değil |
| `gemma4:7b` (yok) | - | - | - | - | `4b` kullan |
| `hermes3:latest` | 4.7 GB | ? | Orta | 120sn yeterli | Alternatif |
| `mistral:latest` | 4.4 GB | 7B | Hızlı | 90sn yeterli | Hızlı cevaplar |

## Örnek: Altın Ons Sohbeti (13 May 2026)

Detaylar: `skill_view('ollama-sohbet', 'references/altin-sohbet-13-mayis-2026.md')`

**Veri toplama:** TradingEconomics'ten ons altın ($4,699), gram altın (6,852 TL), ABD enflasyonu (%3.8), gümüş ($89), jeopolitik olaylar.

**1. Tur:** "Altın ons fiyatı nedir? Sence düşüş devam eder mi?" → model 3 senaryo analizi yaptı (ayı/boğa/konsolidasyon)

**2. Tur:** "Rekor 5,602'den 4,700'e düşüş. En büyük sebep faiz mi jeopolitik mi? Gümüş neden %176 yükseldi?" → faiz beklentilerini ana sebep olarak verdi, gümüşün endüstriyel taleple yükseldiğini açıkladı

**Script şablonu:**

```bash
#!/bin/bash
MESSAGE="Guncel verilere gore: Ons altin $4,699, ABD enflasyonu %3.8, gecen yila gore %47 yukarida. Recep Tayyip Erdogan ... Soru: Sence ..."
echo "$MESSAGE" | ollama run gemma4:latest 2>/dev/null
```
