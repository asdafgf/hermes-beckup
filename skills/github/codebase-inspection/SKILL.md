---
name: codebase-inspection
description: "Inspect codebases w/ pygount: LOC, languages, ratios."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [LOC, Code Analysis, pygount, Codebase, Metrics, Repository]
    related_skills: [github-repo-management]
prerequisites:
  commands: [pygount]
---

# Codebase Inspection (headless — no IDE)

Analyze any codebase without opening VS Code using CLI tools only. Two phases: (1) structural overview, (2) deep-dive into models, APIs, dependencies, cost status.

## When to Use

- User wants to understand a project's structure, technology, and modules
- User wants a headless (no VS Code) inspection — find + read_file + grep
- User asks for LOC, language breakdown, file counts, ratios
- User wants to assess whether a project is production-ready or costs money
- General "what does this project do" questions

## Phase 1: Structural Overview

### File Tree + Size

```bash
find /path/to/project -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.py" \) ! -path "*/node_modules/*" ! -path "*/.git/*" 2>/dev/null | sort
find /path/to/project -type f \( -name "*.ts" -o -name "*.tsx" \) ! -path "*/node_modules/*" ! -path "*/.git/*" -exec wc -l {} + | tail -1
```

### Directory Structure

```bash
find /path/to/project -maxdepth 3 -type d ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/__pycache__/*" 2>/dev/null
```

### Key Config Files

```bash
ls package.json 2>/dev/null   # Dependencies, scripts
ls tsconfig.json 2>/dev/null  # TypeScript config
ls app.json 2>/dev/null       # Expo config
ls .env 2>/dev/null           # Environment variables
```

### Technology + Cost Assessment

Read key files to determine:
- **Tech stack**: framework, database, auth, storage, hosting
- **Cost status**: is it using free tiers (Supabase free, mock payments) or paid services?
- **Completion state**: is there a git repo? Are there test files? Is there build output?

## Phase 2: Deep Dive (per user's direction)

The user may say "VS Code açmadan bakabiliyorsan kod derinlemesine incele". In that case:

### Read Models First

```python
from hermes_tools import read_file
# Read all model/schema files to understand data structure
files = ["models/Contract.ts", "models/schema.ts", "models/User.ts", "models/Payment.ts"]
```

### Then Read Core Utils

```python
# Read critical utility files
files = ["utils/supabase.ts", "utils/auth.ts", "utils/payment.ts", "utils/mediaUpload.ts"]
```

### Then Read Edge Functions / APIs

```python
# Read serverless functions
files = ["supabase/functions/contracts/create/index.ts", "supabase/functions/contracts/sign/index.ts"]
```

### Then Read Views/Screens

```python
# Read main app screens
files = ["app/(owner)/owner/dashboard.tsx", "app/(owner)/owner/contracts/list.tsx"]
```

### Report Structure

For each file group, report:
1. What it does (one-line summary)
2. Key interfaces/types (param types, return types)
3. Dependencies (imports)
4. Cost implications (free tier vs paid API calls)
5. Completion status (mock vs real implementation, todos, commented code)

## Line Count (pygount)

```bash
pygount --format=summary --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,vendor,third_party" .
```

## Prerequisites

```bash
pip install --break-system-packages pygount 2>/dev/null || pip install pygount
```

## 1. Basic Summary (Most Common)

Get a full language breakdown with file counts, code lines, and comment lines:

```bash
cd /path/to/repo
pygount --format=summary \
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,.eggs,*.egg-info" \
  .
```

**IMPORTANT:** Always use `--folders-to-skip` to exclude dependency/build directories, otherwise pygount will crawl them and take a very long time or hang.

## 2. Common Folder Exclusions

Adjust based on the project type:

```bash
# Python projects
--folders-to-skip=".git,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,.mypy_cache"

# JavaScript/TypeScript projects
--folders-to-skip=".git,node_modules,dist,build,.next,.cache,.turbo,coverage"

# General catch-all
--folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,vendor,third_party"
```

## 3. Filter by Specific Language

```bash
# Only count Python files
pygount --suffix=py --format=summary .

# Only count Python and YAML
pygount --suffix=py,yaml,yml --format=summary .
```

## 4. Detailed File-by-File Output

```bash
# Default format shows per-file breakdown
pygount --folders-to-skip=".git,node_modules,venv" .

# Sort by code lines (pipe through sort)
pygount --folders-to-skip=".git,node_modules,venv" . | sort -t$'\t' -k1 -nr | head -20
```

## 5. Output Formats

```bash
# Summary table (default recommendation)
pygount --format=summary .

# JSON output for programmatic use
pygount --format=json .

# Pipe-friendly: Language, file count, code, docs, empty, string
pygount --format=summary . 2>/dev/null
```

## 6. Interpreting Results

The summary table columns:
- **Language** — detected programming language
- **Files** — number of files of that language
- **Code** — lines of actual code (executable/declarative)
- **Comment** — lines that are comments or documentation
- **%** — percentage of total

Special pseudo-languages:
- `__empty__` — empty files
- `__binary__` — binary files (images, compiled, etc.)
- `__generated__` — auto-generated files (detected heuristically)
- `__duplicate__` — files with identical content
- `__unknown__` — unrecognized file types

## Pitfalls

1. **Always exclude .git, node_modules, venv** — without `--folders-to-skip`, pygount will crawl everything and may take minutes or hang on large dependency trees.
2. **Markdown shows 0 code lines** — pygount classifies all Markdown content as comments, not code. This is expected behavior.
3. **JSON files show low code counts** — pygount may count JSON lines conservatively. For accurate JSON line counts, use `wc -l` directly.
4. **Large monorepos** — for very large repos, consider using `--suffix` to target specific languages rather than scanning everything.
