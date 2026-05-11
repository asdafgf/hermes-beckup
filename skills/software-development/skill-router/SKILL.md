---
name: skill-router
description: "Use this skill when the user's task is complex, multi-step, or spans multiple domains and you need to figure out which combination of available skills to use, in what order, and how to pass data between them. Triggers when a task would benefit from chaining multiple skills together. For example: research and create presentation, scrape and visualize, review code and file GitHub issue, analyze image and add to Notion. Also triggers when user asks about skill combinations or best workflow. Use before individual skills on any multi-step workflow."
version: 1.2
author: Eymen
license: MIT
metadata:
  hermes:
    tags: [router, workflow, orchestration, multi-step, chain, conflict]
    related_skills: [plan, nexus-core, writing-plans]
---

# Skill Router — Yonlendirme Algoritmasi

Gorev analizi yaparak mevcut skill'lerden optimal zincir kurar ve aralarindaki veri akisini yonetir.

## Ne Zaman Devreye Girer

- Gorev birden fazla adim iceriyorsa
- Birden fazla domain'e yayiliyorsa (arastirma + uretim, veri + gorsel, kod + dokumantasyon)
- Kullanici bilesik bir gorev istiyorsa
- Tek skill yeterliyse direkt o skill'e gec, router'i atla

## Yonlendirme Algoritmasi (4 Adim)

### Adim 1: Gorevi Ayristir

Gorevi atomik alt gorevlere bol. Her alt gorev tek bir skill ile yapilabilir olmali.

**Ornek:** "Arxiv'den makale arastir, bulgularini Notion'a ekle ve PowerPoint hazirla"

**Alt gorevler:**
1. [arastirma] -> arxiv
2. [kayit] -> notion
3. [sunum] -> powerpoint

### Adim 2: Bagimlilik Grafigi Kur

Her alt gorevin girdisi ve ciktisini esle:

```
arxiv.cikti -> notion.girdi (makale ozeti)
notion.cikti -> powerpoint.girdi (yapilandirilmis icerik)
```

**Paralel calisabilecekleri tespit et:**
- Bagimliligi olmayan gorevler -> paralel
- Onceki ciktiya bagimli -> sirali

### Adim 3: Veri Aktarim Formatini Belirle

| Kaynak Skill Ciktisi | Hedef Skill Girdisi | Aktarim Yontemi |
|---|---|---|
| Metin/ozet | Herhangi | Dogrudan string |
| Dosya (PDF, gorsel) | OCR/gorsel skill | Dosya yolu |
| Yapilandirilmis veri | Veritabani skill | JSON |
| Kod | Debug/test skill | Dosya yolu + dil |

### Adim 4: Zincirleme Plani Uret

Format:

```
PLAN:
========================================
ADIM 1  [skill-adi]
  Girdi:  ...
  Cikti:  ...
  |
ADIM 2  [skill-adi]
  Girdi:  ADIM-1.cikti
  Cikti:  ...
  |
ADIM 3  [skill-adi] || ADIM 4 [skill-adi]  <- paralel
  Girdi:  ADIM-2.cikti
  Cikti:  ...
========================================
Tahmini adim sayisi: N
Kritik yol: ADIM-1 -> ADIM-2 -> ADIM-3
```

## Ornek Zincirler

### Kod Gelistirme -> Review -> Issue
```
plan
  -> kod-yaz-calistir-hata-ayikla-dongusu
    -> python-mock-test-harness
      -> github-code-review
        -> github-issues (hata bulunursa)
```

### Web Veri -> ML Pipeline
```
apify-ultimate-scraper
  -> jupyter-live-kernel (veri temizleme)
    -> huggingface-hub / weights-and-biases
      -> llama-cpp (yerel test)
```

### Arastirma -> Sunum
```
arxiv / blogwatcher
  -> document-research-compilation
    -> powerpoint / baoyu-infographic
```

### Web Scraping -> Veritabani -> Analiz
```
apify-ultimate-scraper
  -> notion / airtable
    -> jupyter-live-kernel
```

### Gorsel Analiz -> Rapor -> E-posta
```
gorsel-analiz-protokolu
  -> powerpoint / notion
    -> himalaya
```

### Haber -> Ozet -> Bildirim
```
gunluk-haber-ozeti-cronjob
  -> document-research-compilation
    -> himalaya / notion
```

## Cakisma ve Alternatif Kurallari

Ayni isi yapan birden fazla skill varsa su oncelik sirasi gecerli:

| Is | Oncelik Siralamasi |
|---|---|
| Kod uretimi | kod-yaz-calistir-hata-ayikla-dongusu > claude-code > codex > opencode |
| Scraping | apify-ultimate-scraper > apify-actorization > manuel |
| Debug | systematic-debugging > node-inspect-debugger > python-vscode-claude-debug-loop |
| Gorsel uretim | claude-design > comfyui > pixel-art / sketch |
| Dokuman kayit | notion > obsidian > airtable > google-workspace |

## Yurutme Sirasinda

- **Her adimdan once:** o adimin girdisi hazir mi kontrol et
- **Hata olusursa:** zinciri durdur, kullaniciya hangi adimda hangi skill'de hata oldugunu raporla
- **Adim atlanabilirse:** kullaniciya sor, zorla yurutme
- **Cikti formati uyumsuzsa:** ara donusum adimi ekle (genelde metin -> JSON veya JSON -> metin)

## Cikti Formati

Her zincir planini kullaniciya sunmadan once su formatta goster:

```
SKILL ZINCIRI PLANI
========================================
Gorev: [kullanicinin gorevi]
Toplam adim: N
Paralel adim: M

[1] skill-adi
    <- Girdi: ...
    -> Cikti: ...

[2] skill-adi
    <- Girdi: [1].cikti
    -> Cikti: ...
...
========================================
Onayliyor musun? (evet / duzenle)
```

Kullanici onaylarsa zinciri baslat. "Duzenle" derse hangi adimi degistirmek istedigini sor.

## Skill Katalogu

### Otonom AI Ajanlar
| Skill | Ne Yapar | Cikti |
|---|---|---|
| claude-code | Kod yazar, calistirir, hata ayiklar | Calisan kod |
| codex | OpenAI Codex kod uretimi | Kod |
| hermes-agent | Genel orkestrasyon | Gorev sonucu |
| opencode | Acik kaynak kod ajani | Kod |

### YARATICI
| Skill | Ne Yapar | Cikti |
|---|---|---|
| architecture-diagram | Sistem mimarisi diyagrami | Diyagram |
| ascii-art | ASCII gorsel | ASCII metin |
| baoyu-comic | Cizgi roman | Gorsel seri |
| baoyu-infographic | Infografik | Gorsel |
| claude-design | UI/UX tasarim | Tasarim |
| comfyui | Gorsel uretimi | Gorsel |
| excalidraw | El cizimi diyagram | Excalidraw |
| humanizer | Metin insansilastirma | Metin |
| ideation | Fikir uretimi | Fikir listesi |
| manim-video | Matematik animasyon | Video |
| p5js | interaktif gorsel | JS kodu |
| pixel-art | Pixel art | Gorsel |
| sketch | Taslak | Gorsel |

### Veri Bilimi
| Skill | Ne Yapar | Cikti |
|---|---|---|
| jupyter-live-kernel | Jupyter notebook | Notebook |

### DevOps
| Skill | Ne Yapar | Cikti |
|---|---|---|
| kanban-orchestrator | Kanban is akisi | Board |
| kanban-worker | Kanban gorev | Guncelleme |
| webhook-subscriptions | Webhook | Abonelik |

### E-posta
| Skill | Ne Yapar | Cikti |
|---|---|---|
| himalaya | E-posta istemcisi | E-posta |

### GitHub
| Skill | Ne Yapar | Cikti |
|---|---|---|
| codebase-inspection | Kod analizi | Rapor |
| github-auth | Kimlik dogrulama | Token |
| github-code-review | Kod inceleme | Yorum |
| github-issues | Issue yonetimi | Issue |
| github-pr-workflow | PR is akisi | PR |
| github-repo-management | Repo yonetimi | Repo |

### MLOps
| Skill | Ne Yapar | Cikti |
|---|---|---|
| dspy | DSPy pipeline | Pipeline |
| huggingface-hub | HF model | Model |
| llama-cpp | Yerel LLM | Model |
| segment-anything-model | SAM segmentasyon | Maske |
| weights-and-biases | Deney takibi | Log |

### Not Alma
| Skill | Ne Yapar | Cikti |
|---|---|---|
| obsidian | Obsidian vault | Not |

### Web Scraping
| Skill | Ne Yapar | Cikti |
|---|---|---|
| apify-ultimate-scraper | Genel scraper | Veri |

### Verimlilik
| Skill | Ne Yapar | Cikti |
|---|---|---|
| airtable | Airtable | Kayit |
| document-research-compilation | Arastirma + derleme | Dokuman |
| gorsel-analiz-protokolu | Gorsel analiz | Rapor |
| gunluk-haber-ozeti-cronjob | Haber ozeti | Ozet |
| google-workspace | Google Docs/Sheets | Dosya |
| linear | Linear yonetim | Issue |
| maps | Harita | Harita |
| nano-pdf | PDF islem | PDF |
| notion | Notion | Sayfa |
| ocr-and-documents | OCR | Metin |
| powerpoint | PowerPoint | PPTX |

### Arastirma
| Skill | Ne Yapar | Cikti |
|---|---|---|
| arxiv | Akademik makale | Ozet |
| blogwatcher | Blog takibi | Icerik |
| llm-wiki | LLM bilgi | Bilgi |
| polymarket | Tahmin piyasasi | Veri |

### Yazilim Gelistirme
| Skill | Ne Yapar | Cikti |
|---|---|---|
| kod-yaz-calistir-hata-ayikla-dongusu | Kod dongusu | Kod |
| nexus-core | OMEGA protokolu | Yanit |
| plan | Gorev plani | Plan |
| python-dosya-organizasyonu | Dosya duzenleme | Dosyalar |
| python-mock-test-harness | Test sistemi | Sonuc |
| python-vscode-claude-debug-loop | VS Code debug | Debug |
| requesting-code-review | Kod inceleme | Review |
| spike | Prototip | Prototip |
| subagent-driven-development | Alt ajan | Kod |
| systematic-debugging | Hata ayiklama | Bug raporu |
| test-driven-development | TDD | Test + kod |
| writing-plans | Plani | Plan |

## Pitfalls
1. Gereksiz routing - tek skill yeterliyken zincirleme
2. Veri uyumsuzlugu - cikti ile sonraki girdi uyusmazsa ara donusum adimi ekle
3. Yanlis sira - once arastirma sonra uretim
4. Eksik adim - son adimi (kaydetme/gonderme) atlama
5. Paralel adimda veri kirliligi - bagimsiz gorevlerin ciktilarini karistirma

## HIRE-PROMPT Skill Improvement Loop

Bu skill scripts/ altyapisi ile kendi kendini iyilestirebilir:

### scripts/ dosyalari
- run_loop.py -> Ana dongu: eval -> improve -> repeat (max 5)
- improve_description.py -> Claude ile description optimize
- package_skill.py -> .skill zip paketi
- utils.py -> Frontmatter parser
- run_eval.py -> Tekil eval
- quick_validate.py -> Validasyon

### Kullanim
```bash
python -m scripts.run_loop \
  --eval-set evals/evals.json \
  --skill-path ./my-skill \
  --model claude-sonnet-4-20250514 \
  --max-iterations 5 \
  --verbose
```
