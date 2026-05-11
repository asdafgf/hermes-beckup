---
name: python-dosya-organizasyonu
description: "Organize scattered Python source files: bulk-rename by content analysis, classify by function, deduplicate, and clean up messy work directories."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [python, file-organization, rename, cleanup, code-classification]
prerequisites:
  commands: [python3, pip]
---

# Python Dosya Organizasyonu

Scattered/dump Python files into organized, functionally-named files. Designed for users who have years of accumulated `.py` files across Desktop, Downloads, home directory, and OneDrive.

## When to Use

- User says "Python dosyalarını düzenle / adlandır / organize et"
- User has messy home/Desktop/Downloads with many `.py` files
- User wants to deduplicate or classify scattered source files
- User asks about "temizlik" (cleanup) of code files

## Workflow

### 1. Discover All Python Files

```bash
find ~ -maxdepth 1 -name "*.py" 2>/dev/null          # home dir
ls ~/Desktop/*.py 2>/dev/null                         # Desktop
ls ~/Downloads/*.py 2>/dev/null                       # Downloads
ls "$HOME/OneDrive/Masaüstü"/*.py 2>/dev/null         # OneDrive Desktop
```

Common locations on Windows (git-bash/MSYS):
- `~/` (home = `C:\Users\<user>\`)
- `~/Desktop/`
- `~/Downloads/`
- `~/OneDrive/Masaüstü/`
- `~/Documents/`

### 2. Snapshot File Contents

Quick-read first ~12 lines of every file to classify:

```bash
cd ~/Downloads
for f in *.py; do echo "===FILE: $f==="; head -12 "$f" 2>/dev/null; echo "---"; done
```

### 3. Classification Strategy

Build a mapping dictionary. For each file, identify its core function using **manual inspection of imports, function names, and keywords** — regex-only analysis is brittle and produces false positives (e.g. "baslat.py" classified as "ag_tarama" because the body imports `os` and `subprocess`).

**Priority check order** (high → low specificity):

| Category | Keywords / Imports | Example Name |
|---|---|---|
| Android/Gradle | `assurelens`, `android`, `gradle`, `settings.gradle` | `android_studio_baslat` |
| Face recognition | `cv2`, `face`, `yüz`, `face_recognition` | `yuz_tanima_sistemi` |
| Network scan | `nmap`, `scapy`, `ağ ip`, `mac tarama` | `ag_ip_mac_tarama` |
| LLM/AI | `ollama`, `groq`, `openai`, `anthropic`, `gemini`, `deepseek`, `langchain`, `crewai`, `transformers`, `huggingface` | `ollama_otonom_ajan` |
| Web/Scraping | `selenium`, `BeautifulSoup`, `scrapy`, `requests` + `scrap/kazı/html` | `web_kaziyici` |
| MCP | `fastmcp`, `mcp` + `server` | `mcp_sunucu` |
| Gradio/Streamlit | `gr.Interface`, `st.title`, `gr.ChatInterface` | `gradio_web_arayuz` |
| Web framework | `Flask(`, `FastAPI(` | `flask_sunucu` |
| Finance | `yfinance`, `bist`, `borsa`, `hisse` | `borsa_veri_cekme` |
| Data viz | `matplotlib`, `seaborn`, `plotly`, `plt.plot` | `grafik_cizim_araci` |
| Database | `pyodbc`, `sqlalchemy`, `create_engine` | `veritabani_baglantisi` |
| Automation | `pyautogui`, `pynput`, `pygame` | `ekran_otomasyonu` |
| Windows | `winreg`, `win32com` | `windows_kayit_defteri` |
| Setup | `pip install`, `subprocess.run` + `install/setup/kur` | `kurulum_scripti` |
| Update | `update`, `upgrade`, `güncelle` | `guncelleme_scripti` |
| Fix | `fix`, `düzelt`, `restart` | `hata_duzeltme` |
| Test scratch | `import os`, `import sys`, `import torch` (single import line only) | `test_os_modulu` |

### 4. Handle Duplicates and Variants

Files with `(1)`, `(2)`, `(3)` suffixes → same base name with `_2`, `_3`, `_4` counters.

```python
# Check for conflicts before rename
counter = 1
while os.path.exists(new_path):
    new_fname = f"{base_name}_{counter}.py"
    counter += 1
```

### 5. Cleanup: Handle Pseudocode/Comment-Only Files

Files like `# pip install gerektirmez...` → `kurulum_notu_1.py` (they describe needs, not executable code).

Files that are 0 bytes or contain only comments → move to a `_bak` or `_notlar` subfolder.

Files with nonsense names (`XXX.py`, `XCVBNM.py`, `import osddddcva.py`) → `test_deneme.py`, `test_deneme_2.py`, etc.

### 6. Final Verification

```bash
# Count files before and after
ls ~/Desktop/*.py ~/Downloads/*.py ~/*.py | wc -l

# Spot-check a few renames
head -5 ~/Downloads/kgr_tablo_olustur.py
```

## Pitfalls

1. **WATCH OUT: files that end in `.py` but are NOT Python.** PDFs renamed to `.py` exist. Check with `file <filename>` before renaming if uncertain.
2. **`#` ile başlayan dosyalar** — Windows'ta geçerli dosya adı ama `.py` uzantılı olabilir. "yorum satırı" notlarıdır, `aciklama_notu.py` yap.
3. **Regex-only classification is unreliable** — a file that imports `os` and runs `subprocess.Popen` might be an Android Studio launcher, not a network scanner. Always read the actual function names/strings.
4. **Çakışmalar farklı klasörlerde sorun değil** — `test_os_indirilen.py` hem home'da hem Downloads'ta olabilir, farklı klasör olduğu için çakışma yok.
5. **Küçük/büyük harf ve Türkçe karakter sorunları** — `İLİŞKİLER.py` gibi dosyalar `'İLİŞ' in f.upper()` ile bulunur, doğrudan string eşleme bazen başarısız olur.
6. **Boş dosyalar (0 byte)** — rename etmeden önce kontrol et ve `bos_dosya_silinecek` olarak işaretle veya sil.

## References

See `references/rename-mapping.md` for the full category-to-new-name mapping table from the initial bulk operation.
