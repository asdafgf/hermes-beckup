# Hybrid Pip Package + Skill Import (Windows)

Bir GitHub reposu aynı anda **hem Python pip paketi (`setup.py` + `requirements.txt`)** hem de **Claude Code skill'leri (`.claude/skills/`)** içeriyorsa, bu rehberi izle.

## Örnek Vaka: `oguzcankaraman/Watch_Youtube_Skill`

```
repo/
├── setup.py              # pip install -e . ile CLI kaydı
├── requirements.txt      # pip bağımlılıkları
├── .claude/skills/
│   ├── watch-youtube/    # skill 1
│   │   └── SKILL.md
│   └── wiki-schema/      # skill 2
│       └── SKILL.md
└── watch_youtube/        # Python modülü
```

## Adımlar

### 1. Repoyu Klonla

```bash
cd /c/Users/<user>
git clone --depth 1 https://github.com/<org>/<repo>.git
```

### 2. Python Venv + Bağımlılıkları Yükle

```bash
cd <repo_adi>
python -m venv .venv
source .venv/Scripts/activate    # Windows! macOS/Linux'da source .venv/bin/activate

pip install -r requirements.txt  # tüm bağımlılıklar
pip install -e .                 # CLI'ı kaydet (setup.py veya pyproject.toml)
```

**Windows notu:** `source .venv/Scripts/activate` kullan, `.venv/bin/activate` DEĞİL.

### 3. Ekstra Bağımlılıklar

- **spaCy modeli:** `python -m spacy download en_core_web_sm`
- **ffmpeg:** `scoop install ffmpeg` veya `winget install ffmpeg`

### 4. Skill'leri Hermes'e Kopyala

```bash
# Her skill için ayrı klasör
mkdir -p ~/AppData/Local/hermes/skills/<kategori>/<skill-adi>
cp .claude/skills/<skill-adi>/SKILL.md ~/AppData/Local/hermes/skills/<kategori>/<skill-adi>/
```

Uygun kategoriyi seç (örn. `youtube`, `media`, `productivity`).

### 5. CLI'ı Test Et

```bash
source .venv/Scripts/activate
<cli-command> --help   # çalışıyorsa pip install -e . başarılı
```

### 6. GROQ_API_KEY (Opsiyonel — Transcript Fallback)

Transcript'siz videolar (canlı yayın, müzik) için Whisper API fallback:

```bash
setx GROQ_API_KEY "gsk_..."   # kalıcı
export GROQ_API_KEY="gsk_..."  # geçici
```

Key al: https://console.groq.com (ücretsiz tier yeterli).

### 7. Skill'leri Doğrula

```python
skills_list()      # Hermes yeni skill'leri görüyor mu?
skill_view('watch-youtube')  # içerik okunabiliyor mu?
```

## Farklar: Saf Skill İmport vs Hibrit Import

| Özellik | Saf Skill | Hibrit (Paket+Skill) |
|---------|-----------|---------------------|
| Gereken | Sadece SKILL.md kopyala | Venv kur + pip install + SKILL kopyala |
| CLI | Yok | `pip install -e .` ile kaydedilir |
| Bağımlılık | Yok | requirements.txt'dekiler yüklenir |
| Test | skills_list ile doğrula | `--help` çıktısını kontrol et |
| Temizlik | temp-skill-import sil | Proje klasörünü koru (venv yeniden kurulum gerektirir) |
