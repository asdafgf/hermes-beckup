---
name: anthony-sottile-markdown-git-tricks
description: "Anthony Sottile (anthonywritescode) — Markdown dosyalarında Git diff okunabilirliği için satır sonu ve listeleme ipuçları"
version: 1.0
category: software-development
source: "Anthony Sottile YouTube"
tags: [python, markdown, git, diff, pre-commit, code-quality]
platforms: [linux, macos, windows]
---

# Markdown + Git Tricks

Kaynak: Anthony Sottile (anthonywritescode)

## Problem

Markdown dosyalarinda numbered list ve code block kullanirken Git diff okumasi zorlasir.

### Cozum: Her satiri ayri commit et, degisiklikleri kucuk tut

```markdown
1. Item A
2. Item B
3. Item C
```

vs eski numbered list yeniden numaralandirilinca diff karmasiklasir.

### Anthony'nin Yaklasimi

```bash
# Her degisikligi ayri commit
git add -p  # interactive staging
git commit -m "add item to list"
```

## pre-commit ve Markdown

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.0
    hooks:
      - id: prettier
        types: [markdown]
```

pre-commit ile markdown dosyalarini otomatik formatla. Degisiklikler standart olsun.

## Ipuclari

- Numbered list'lerde `1.` kullan (numaralandirma otomatik)
- Her paragrafi ayri satir
- Code block'larda language belirt
- Git diff okunabilirligi icin satir basina bir cumle

```markdown
<!-- IYI -->
1. Ilk madde
1. Ikinci madde  <!-- Markdown otomatik numaralandirir -->
1. Ucuncu madde

<!-- Kotu - elle numaralandirinca diff karmasik -->
1. Ilk
2. Ikinci
3. Ucuncu
```
