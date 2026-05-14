---
name: watch-youtube
description: "Analyze a YouTube video: download transcript, extract semantically relevant frames using NLP, compile storyboard grids optimized for Vision LLM. Writes extracted knowledge to docs/wiki/. Use when the user provides a YouTube URL and wants to analyze, summarize, or understand a video's visual content."
tags: [youtube, video-analysis, nlp, storyboard, vision-llm, ffmpeg]
related_skills: [wiki-schema, mevcut-ollama-modelleri-entegrasyonu]
---

# watch-youtube: YouTube Video Storyboard for Vision LLMs

Turns a YouTube video into annotated JPEG storyboard grids, analyzes them with Vision LLM, and writes the extracted knowledge to `docs/wiki/` using wiki-schema rules.

## When the user invokes this skill

1. Confirm the YouTube URL and desired output directory.
2. Check that dependencies are installed (see **Setup** below).
3. Run the pipeline via the `watch-youtube` CLI.
4. Read storyboards from `output/<video_id>/storyboard_page_*.jpg` and analyze with Vision LLM.
5. Show the user a structured analysis.
6. Write the extracted knowledge to `docs/wiki/` following **wiki-schema** rules (see section below).
7. **Add a video record to `docs/wiki/Videos.md`** (see section below).
8. Update `docs/wiki/Index.md`.

---

## Setup (run once per environment)

```bash
cd /path/to/project
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install the spaCy English model (required for NLP)
python -m spacy download en_core_web_sm

# Install the CLI in editable mode
pip install -e .

# Install ffmpeg (required for frame extraction)
# macOS: brew install ffmpeg
# Windows (scoop): scoop install ffmpeg
```

---

## Running the pipeline

```bash
watch-youtube "<YOUTUBE_URL>" \
    --output-dir ./output \
    --max-frames 20 \
    --jpeg-quality 85 \
    --verbose
```

### Key options

| Flag | Default | Purpose |
|------|---------|---------|
| `--output-dir / -o` | `.` | Where to save storyboard JPEGs |
| `--max-frames / -n` | `30` | Cap on smart frames extracted |
| `--jpeg-quality / -q` | `85` | JPEG quality 1-95 |
| `--silence-gap / -g` | `5.0` | Seconds of silence that triggers a frame |
| `--groq-api-key / -k` | env `GROQ_API_KEY` | Whisper fallback when no transcript |
| `--no-learn` | off | Skip self-learning keyword store update |
| `--keep-temp` | off | Keep raw frames and video file |
| `--verbose / -v` | off | Show per-timestamp debug output |

---

## Pipeline architecture

```
YouTube URL
    |
    v
downloader.py        Download transcript (VTT/SRT) + video MP4
    |                Fallback: download audio to Groq Whisper API
    v
analyzer.py          NLP timestamp extraction (spaCy + learned keyword store)
    |                Rule A: keyword/deictic pattern matching
    |                Rule B: silence gap detection (>= silence_gap seconds)
    |                Post-run: TF-IDF self-learning updates data/keyword_store.json
    v
extractor.py         ffmpeg frame extraction at smart timestamps only
    |                Adaptive quality; skips black/corrupt frames
    v
compiler.py          Pillow storyboard grid compilation
    |                Adaptive cell resolution (720-1280px depending on grid density)
    |                Transcript captions burned in below each frame
    v
output/<video_id>/storyboard_page_NNN.jpg  (one or more JPEG grids, isolated per video)
    |
    v
Vision LLM analysis  Read storyboard images to structured summary
    |
    +--> docs/wiki/<title>.md      Write topic pages (wiki-schema rules)
    +--> docs/wiki/Videos.md       Append video record (URL, date, pages)
    +--> docs/wiki/Index.md        Update index with new pages
```

---

## Writing to docs/wiki (wiki-schema integration)

After analyzing the storyboard, **always** write a wiki entry to `docs/wiki/` following these rules from `wiki-schema`:

### Required frontmatter structure for each wiki page

```markdown
**Ozet:** [Max 3 sentences describing what was learned]
**Kutuphaneler/Teknolojiler:** [Key technologies/tools covered]
**Baglantilar:** [[Related_Topic]], [[Another_Topic]]
```

### Wiki file naming

- Use descriptive PascalCase filenames: `OperatingSystemFundamentals.md`, `VirtualMemory.md`
- After writing, update `[[docs/wiki/Index.md]]` with a pointer to the new file

### What to write in the wiki entry

- Main concepts explained in the video
- Key diagrams or visual structures (describe them in text)
- Relationships to other topics (with Obsidian-style `[[links]]`)
- Sponsor segments or tool mentions (tagged as such)

### Example wiki entry

```markdown
**Ozet:** Bu video isletim sisteminin temel bilesenlerini anlatiyor: surecler, kernel modu, sanal bellek ve dosya sistemi.
**Kutuphaneler/Teknolojiler:** Linux Kernel, C, ffmpeg, spaCy
**Baglantilar:** [[VirtualMemory]], [[FileSystem_Inodes]], [[DeviceDrivers]]

## Icerik
...
```

### Always update Index.md

After writing a new wiki page, open `docs/wiki/Index.md` and add a link:
```markdown
- [[NewPageTitle]] -- one-line summary
```

---

## Recording the video in docs/wiki/Videos.md

**Always** append a record to `docs/wiki/Videos.md` after each analysis:

```markdown
### [Video Basligi](https://www.youtube.com/watch?v=VIDEO_ID)
- **ID:** `VIDEO_ID`
- **Analiz tarihi:** YYYY-MM-DD
- **Sure:** ~X dakika
- **Transcript:** vtt / srt / whisper / synthetic
- **Kare sayisi:** N kare, M storyboard sayfasi
- **Olusturulan wiki sayfalari:** [[Sayfa1]], [[Sayfa2]]
- **Ozet:** Tek cumlelik icerik ozeti
```

This is the single source of truth for "which videos have been analyzed." Always check `Videos.md` before re-analyzing a URL that may already exist.

---

## Adaptive resolution table

| Frames | Grid | Cell width |
|--------|------|-----------|
| 1 | 1x1 | 1280px |
| 2 | 2x1 | 1024px |
| 3-4 | 2x2 | 960px |
| 5-6 | 3x2 | 800px |
| 7-9 | 3x3 | 720px |
| 10-12 | 4x3 | 640px |
| 13+ | 3x3 pages | 720px |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ffmpeg not found` | `brew install ffmpeg` (macOS) or `scoop install ffmpeg` (Windows) |
| `No module named spacy` | `pip install spacy && python -m spacy download en_core_web_sm` |
| `Cannot access video` | Video may be private, age-restricted, or region-blocked |
| No transcript found | Pass `--groq-api-key` or set `GROQ_API_KEY` env var |
| Module import error | Run `pip install -e .` from project root with venv active |
| Video >400MB timeout (902MB seen) | Transcript downloads first; capture it even if video times out. Re-run with `--max-frames 10` and `--keep-temp` for large files. If timeout happens after frame extraction, storyboard files exist but wiki writes are skipped -- handle manually. |
| Vision LLM unavailable (DeepSeek rejects image_url) | Use local LLaVA:7b via Ollama REST API: `curl -s --max-time 180 -X POST http://localhost:11434/api/generate -d '{"model":"llava:7b","prompt":"analyze","images":["BASE64"],"stream":false}'` (LLaVA:7b is pre-installed) |
| Keyword store learned nothing | Check the debug log for "Learned keyword" lines. If none, the transcript may lack distinctive terms. The model still produces timestamp selections from built-in keywords. |
