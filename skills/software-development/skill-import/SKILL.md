---
name: skill-import
description: >-
  Import, verify, and install agent skills from GitHub repositories into Hermes.
  Use when bulk-importing GitHub repositories of agent skills (Anthropic, Cloudflare, Stripe, Expo, Trail of Bits, Sentry, etc.),
  batch-verifying multiple new skills for safety, or migrating skills from Claude Code / Codex / Gemini CLI format to Hermes format.
  Covers: git clone → directory scan → security scan → practical test → Hermes category placement → skill load registration.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skills, import, security, testing, migration]
    related_skills: [hermes-agent-skill-authoring, requesting-code-review]
---
# Skill Import & Verification

Import, verify, and install agent skills from GitHub into Hermes. Designed for bulk operations (6+ repos, 40+ skills per session).

## Overview

GitHub repos like `trailofbits/skills`, `getsentry/skills`, `expo/skills`, `cloudflare/skills`, `stripe/ai`, `anthropics/skills` each contain 4-60 SKILL.md files in various directory layouts. This skill covers the full pipeline: cloning → scanning for safety → testing → categorizing → registering.

## When to Use

- User asks to "add skills from GitHub" or "install popular agent skills"
- User provides a list of repos/categories to import
- Batch-verifying many new skills at once (10+)
- Converting Claude Code / Codex plugins to Hermes skill format
- Re-verifying skills after updating their source repos

## When NOT to Use

- Creating a single custom skill from scratch — use `hermes-agent-skill-authoring`
- Editing an existing installed skill — use `skill_manage(patch)`
- Just listing available skills — use `skills_list`

## Pipeline

```
GitHub clone → directory scan → security scan → practical test → categorize → copy → register → verify → clean up
```

### 1. Clone Source Repo

```bash
mkdir -p ~/temp-skill-import && cd ~/temp-skill-import
git clone --depth 1 https://github.com/<org>/<repo>.git <name>
```

Use `--depth 1` to save bandwidth — only the latest commit matters.

### 2. Directory Scan

Discover all SKILL.md files:

```bash
find <name> -name "SKILL.md" -not -path "*/\.*" | sort
```

Note the directory layout. Common patterns:

| Layout | Example | Skill Path Resolution |
|--------|---------|----------------------|
| Flat `skills/<name>/SKILL.md` | Anthropic, Cloudflare | `skills/<name>` |
| Nested `plugins/<plugin>/skills/<name>/SKILL.md` | Trail of Bits | `plugins/<plugin>/skills/<name>` |
| Multi-provider `providers/<tool>/skills/<name>/SKILL.md` | Stripe | `skills/<name>` (canonical) |
| Claude plugin format `.claude-plugin/` + `skills/` | Sentry | `skills/<name>` |

For multi-provider repos (e.g. Stripe), use the canonical `skills/` path, not the per-provider duplicates.

### 3. Security Scan

Run a systematic scan on every SKILL.md. False positives are common in security skills (they document attack patterns). Distinguish **instruction vs reference**.

```python
# Quick security scan template
import os, re
from pathlib import Path

def scan_skill_dir(base):
    results = []
    for skill_md in sorted(Path(base).rglob("SKILL.md")):
        content = skill_md.read_text()
        issues = []
        
        # 1. Prompt injection markers
        for pat in [r"ignore\s+previous\s+instructions", r"you\s+are\s+now\s+(a|an|in)", r"DAN\s+mode"]:
            if re.search(pat, content, re.I):
                issues.append(("prompt-injection", pat, "critical"))
        
        # 2. Code execution patterns
        for pat in [r"\beval\s*\(", r"\bexec\s*\(", r"shell\s*=\s*True", r"os\.system\(", r"os\.popen\("]:
            if re.search(pat, content):
                issues.append(("code-exec", pat, "high"))
        
        # 3. Network exfiltration
        for pat in [r"requests\.(get|post)\s*\(", r"curl\s+", r"wget "]:
            if re.search(pat, content):
                issues.append(("network", pat, "medium"))
        
        # 4. Secret exposure
        for pat in [r"AKIA[0-9A-Z]{16}", r"sk-[0-9a-zA-Z]{20,}", r"-----BEGIN\s+PRIVATE\s+KEY-----"]:
            if re.search(pat, content):
                issues.append(("secret", pat, "critical"))
        
        # 5. Obfuscation
        for pat in [r"[\u200b\u200c\u200d\u2060\ufeff]", r"[\u202a-\u202e]"]:
            if re.search(pat, content):
                issues.append(("obfuscation", "unicode-control-char", "high"))
        
        results.append({
            "skill": str(skill_md),
            "issues": issues,
            "issue_count": len(issues),
        })
    
    return results
```

#### False Positive Handling

**Security skills** (Trail of Bits, Sentry security-review) document attack patterns as educational references. Their SKILL.md will match `eval(`, `exec(`, `shell=True`, `os.system(`. These are NOT dangerous — the skill teaches the agent to *recognize* these patterns, not execute them.

**Classification rule:**
- Pattern in a *code block* or *table* → likely reference → ✅ Safe
- Pattern in an *instruction* ("run this: eval(...)") → actual executable → ❌ Investigate
- Pattern by a major org (Anthropic, Stripe, Cloudflare, Trail of Bits, Sentry) → ✅ Presumed safe (vetted)
- Pattern in an unknown/community repo → ❌ Investigate thoroughly

#### Script File Scan

Scan `.py`, `.sh`, `.js` scripts for:
- Data exfiltration (requests.post to unknown hosts, curl/wget with data payloads)
- Credential access (~/.ssh, ~/.aws, ~/.gnupg paths)
- System config modification (.bashrc, .git/hooks, .claude/ files)
- npm lifecycle hooks (preinstall, postinstall in package.json)
- Symlinks pointing outside the skill directory

Trusted domains (safe for URL references): `github.com`, `raw.githubusercontent.com`, `pypi.org`, `npmjs.com`, `docs.sentry.io`, `docs.python.org`, and the skill author's own domain.

### 4. Practical Test

For each skill, verify:
- **SKILL.md exists**: file is present and readable
- **Frontmatter valid**: starts with `---`, has `name` field, has `description`
- **Hermes registration check**: `skills_list` shows the skill after copy

### 5. Categorize & Copy

Hermes skills live under `~/.hermes/skills/<category>/<name>/SKILL.md`.

Mapping guildines for common repos:

| Source | Category | Notes |
|--------|----------|-------|
| `trailofbits/skills` (security) | `security/` | Create if not exists |
| `getsentry/skills` | `sentry/` | Create if not exists |
| `expo/skills` | `expo/` | Create if not exists |
| `cloudflare/skills` | `cloudflare/` | Create if not exists |
| `stripe/ai` (skills/) | `stripe/` | Create if not exists |
| `anthropics/skills` (docx/pptx/xlsx/pdf) | `anthropic/` | Create if not exists |

```bash
mkdir -p ~/.hermes/skills/<category>/<name>
cp <source>/path/to/SKILL.md ~/.hermes/skills/<category>/<name>/
# Also copy references/, scripts/, templates/ if they exist
[ -d <source>/path/to/references ] && cp -r <source>/path/to/references ~/.hermes/skills/<category>/<name>/
[ -d <source>/path/to/scripts ] && cp -r <source>/path/to/scripts ~/.hermes/skills/<category>/<name>/
```

**Important**: `cp -r` can timeout on large script directories (Anthropic doc skills have O(100) schema files). For large transfers, copy one skill at a time rather than a glob loop.

### 6. Verify Registration

After copying all skills, verify Hermes sees them:

```python
# Hermes lazily scans ~/.hermes/skills/ at skills_list() call
# Call skills_list() to trigger re-scan
```

Hermes scans directories and auto-registers any new `SKILL.md` it finds under `~/.hermes/skills/`. No manual registration needed.

### 7. Clean Up

```bash
rm -rf ~/temp-skill-import/<name>
```

### 8. Report

Format results as:

```
## ✅ TAMAM — N ADIM BAŞARIYLA BİTTİ

Her adımda kod güvenlik taraması yapıldı

### Eklenen Skill'ler (Toplam: X yeni skill)

| # | Kategori | Kimden | Adet |
|---|---|---|---|
| 1 | 🔒 Security | Trail of Bits | N |
| 2 | ... | ... | ... |

### Hybrid Pip Package + Skill Import

Bazı GitHub repoları (örn. `Watch_Youtube_Skill`) hem Python pip paketi (`setup.py`) hem de Claude Code skill'i (`.claude/skills/`) içerir. Bu durumda:

1. Venv kur + `pip install -r requirements.txt && pip install -e .`
2. Skill'leri ayrıca Hermes'e kopyala (`cp .claude/skills/<name>/SKILL.md ~/.hermes/skills/<cat>/<name>/`)
3. CLI'ı `--help` ile test et

→ Detaylı rehber: `skill_view('skill-import', 'references/hybrid-pip-skill-import-windows.md')`

### false-positive notes (if any)
- <skill-name>: eval/exec patterns are educational references, safe
```

## Common Pitfalls

1. **read_file path double-slash.** `pathlib.Path` resolved paths with trailing `//` may cause `read_file` to report "file not found". Always verify paths with `ls` before reading.

2. **cp -r timeout on large O(100) file trees.** The Anthropic `pptx/scripts/office/schemas/` directory contains ~50 XSD files. Copy slow skills individually, not in a for-loop.

3. **Memory full during reporting.** Hermes memory is ~2200 chars. A detailed import report (~660 chars) may not fit. Keep memory entries compact or don't save if a more important entry takes priority.

4. **Self-referencing binary during pip install.** Hermes is running from its own venv binary. `pip install --force-reinstall` will fail with `os error 32` because the binary is in use. Workaround: move old binary aside, then install.

5. **False positives in security skills.** Security skills from Trail of Bits, Sentry, etc. contain attack pattern documentation. Always distinguish *reference* (code blocks, tables) from *instruction* (run this command). Don't flag reference patterns as dangerous.

6. **Overwriting existing categories.** If `~/.hermes/skills/<category>/` already exists, don't remove it — just add new subdirectories alongside existing ones.

7. **GitHub repo not found.** Not all orgs have a `skills` repo. Stripe's skills live at `github.com/stripe/ai` (not `stripe/skills`). Check the actual URL before cloning.

8. **Windows `execute_code` path separator.** On Windows, `shutil.copytree()` and `Path.rglob()` work with `\\` or `/`. Always use `Path(os.path.expanduser("~/..."))` — hardcoded `C:\` paths break when the HOME drive letter changes.

9. **Strip duplicates from multi-provider repos.** Stripe's `providers/` directory contains identical skill copies under each provider. When importing, check `skill.name` in `skills_list()` after copy — duplicates get the same folder name and Hermes merges them, but you still waste clone time on them. Run a dedup pass: collect all SKILL.md contents into a `{md5: name}` dict before copying.

10. **Bash parantez syntax hatası.** `echo` ve yorum satırlarında `(parantez)` kullanma — bash alt-shell olarak yorumlar ve `syntax error near unexpected token` hatası verir. Script yazarken `# (açıklama)` yerine `# -- aciklama --` kullan.

11. **Python string'de tek tırnak içinde apostrof.** `'Claude Code'sun'` gibi ifadeler Python syntax hatası verir. Ya çift tırnak kullan (`"Claude Code'sun"`) ya da escape et (`'Claude Code\'sun'`). Payload oluştururken hep `json.dumps()` kullan, asla manuel string concatenation yapma.

## Verification Checklist

- [ ] All source repos cloned successfully
- [ ] Security scan completed on every SKILL.md
- [ ] False positives identified and documented
- [ ] Script files scanned for dangerous patterns
- [ ] Skills copied to correct category directories
- [ ] `skills_list()` reflects all new skills
- [ ] Audit for duplicates: md5 hash compare, folder-name vs frontmatter-name mismatch (see `hermes-agent` → Curator → Deduplication audit)
- [ ] Cleanup completed (temp dirs removed)
- [ ] Report delivered with per-category counts and any risk notes
