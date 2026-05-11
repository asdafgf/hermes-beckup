# GitHub Repo: hermes-skill-turkce

## Konum
`C:\Users\eymen\Desktop\hermes-skill-turkce\`

## İçerik
- `skills/gorsel-analiz/` — Ana görsel analiz skill'i (SKILL.md + ref'ler + script'ler)
- `skills/claude-dongusu/` — Hata cozum dongusu skill'i
- `skills/hata-ayiklama/` — AI yardim stratejisi skill'i
- `plugin-goruntu-analiz/` — Hermes plugin'i (plugin.yaml + setup.py + script)
- `scripts/` — Bagimsiz calisan script'ler
- `README.md` — Kurulum ve kullanim talimati

## GitHub'a Push
```bash
cd /c/Users/eymen/Desktop/hermes-skill-turkce
gh auth login  # once web'de dogrula
gh repo create hermes-skill-turkce --public --description "Hermes Agent icin Turkce skill'ler + gorsel analiz plugin'i"
git remote add origin https://github.com/eymen/hermes-skill-turkce.git
git branch -M main
git push -u origin main
```

## Hermes'e Yukleme
```bash
# Skill'leri ekle
cp -r skills/* ~/AppData/Local/hermes/skills/

# Plugin'i ekle
cp -r plugin-goruntu-analiz ~/AppData/Local/hermes/hermes-agent/plugins/

# Bagimliliklari kur
pip install pytesseract pandas pillow
scoop install tesseract
cd ~/scoop/apps/tesseract/current/tessdata
curl -O https://github.com/tesseract-ocr/tessdata_fast/raw/main/eng.traineddata
curl -O https://github.com/tesseract-ocr/tessdata_fast/raw/main/tur.traineddata
```
