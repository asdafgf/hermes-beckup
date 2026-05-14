---
name: scheduled-agent-learning
title: "Scheduled LLM Learning with Cronjob + Progress Tracking"
description: "Set up cronjob-based scheduled learning sessions where an LLM (local via Ollama API) works through a curriculum of topics, saves results as .md files, tracks progress via JSON state, and the cronjob's deliver prompt produces periodic reports."
version: 1.0
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [cronjob, learning, ollama, qwen, automation, progress-tracking, scheduled]
    category: devops
    related_skills: [ollama-sohbet, python-oto-debug-dongusu]
---

# Scheduled Agent Learning (Cronjob + Script Pattern)

## Overview

Pattern for setting up an **autonomous scheduled LLM learning session**: a bash/Python script runs periodically, queries a local LLM (via Ollama REST API), saves results to disk with progress tracking, and a cronjob deliver prompt handles human-readable reporting.

This is **not** the `ollama-sohbet` interactive chat pattern — here the script runs headless, manages its own state, and the agent only appears at reporting time.

## Architecture

```
cronjob trigger ──→ script.sh ──→ Ollama (curl REST API)
                     │                  │
                     │                  ▼
                     │           response (JSON)
                     │                  │
                     ▼                  ▼
              progress.json       konu_N_HHMM.md
              (state tracking)    (saved content)
                     │
                     ▼
              cronjob deliver prompt
              (reads files, formats report → Telegram)
```

## Components

### 1. The Script (`~/.hermes/scripts/<name>.sh`)

The script handles the actual LLM interaction. Key patterns:

#### Ollama REST API call (curl, NOT `ollama run`)
```bash
MODEL="qwen2.5-coder:7b"
API_URL="http://localhost:11434/api/generate"

qwen_sor() {
  local prompt="$1"
  local payload
  payload=$(python -c "import json; print(json.dumps({'model':'$MODEL','prompt':'''$prompt''','stream':False}))" 2>/dev/null)

  local response=""
  for attempt in 1 2 3; do
    response=$(curl -s --max-time 120 -X POST "$API_URL" -d "$payload" 2>&1)
    if [ -n "$response" ] && echo "$response" | python -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
      break
    fi
    sleep 3
  done

  echo "$response" | python -c "import sys,json; print(json.load(sys.stdin).get('response',''))" 2>/dev/null
}
```

#### Lock file (prevent double-run within same hour)
```bash
LOCK_FILE="/tmp/<name>_lock.txt"
if [ -f "$LOCK_FILE" ] && [ "$(cat "$LOCK_FILE")" = "$(date '+%H')" ]; then
  exit 0  # already ran this hour
fi
echo "$(date '+%H')" > "$LOCK_FILE"
```

#### Progress state file
```bash
PROGRESS_FILE="$OUTPUT_DIR/progress.json"
echo "{\"son_konu\":$SIRKAT,\"toplam\":$TOTAL,\"tarih\":\"$TARIH\",\"konu\":\"${KONU:0:50}\"}" > "$PROGRESS_FILE"
```

### 2. The Cronjob

```bash
cronjob(action="create",
  name="<name>",
  schedule="0 * * * *",
  repeat=24,
  script="<script_name>.sh",
  prompt="Read progress.json and latest .md, format report."
)
```

**Critical:** The `--script` parameter runs **before** the deliver prompt. The script does the actual work (LLM call, file writes). Then the deliver prompt's agent run reads the files and formats a human report.

**Windows-specific:** Script path MUST be just the filename (e.g. `python_ogrenim.sh`). Keep the script in `~/.hermes/scripts/`.

### 3. The Deliver Prompt

The deliver prompt should:
1. Read `progress.json` for current state
2. Find the latest `.md` file (by timestamp)
3. Read and summarize it
4. Format as a clean report for the user

## State Management

- **progress.json** — JSON with `son_konu`, `toplam`, `tarih`, `konu` fields
- **konu_N_HHMM.md** — each session's full output (markdown)
- **konu_sirasi.txt** — simple counter file (next topic index)

Use `mkdir -p` on the output directory at script start.

## Topic Curriculum Pattern

Define topics as a bash array:
```bash
KONULAR=(
  "Topic 1 description. What to ask model."
  "Topic 2 description. What to ask model."
  ...
)
```

Total count: `TOP_KONU=${#KONULAR[@]}`. When counter exceeds array length, wrap back to 1 (loop).

## Handling Incomplete Skills (Empty LLM Responses)

During scheduled verification of previously-generated skills, you may encounter skills where the Qwen2.5-coder responses are completely blank (empty `[]` in the dialog). This is a structural defect — the skill has questions but no answers.

### Detection
1. Read the skill's `references/diyalog.txt` file
2. Check for patterns like `Qwen2.5-coder (Yanıt 1):` followed immediately by `Hermes` (no content between) or explicitly `[BOŞ]`
3. Note this in the verification report as a "TAMAMLAMASI GEREKEN" item

### Handling in Verification
When the Qwen response is empty, your `qwen2.5-coder:7b` verification prompt should:
1. Generate the missing content as part of the verification (ask the model to "doldur")
2. Flag the empty response as a defect in the "DUZELTILMESI GEREKENLER" section
3. Set the overall result to "KISMEN GECERLI" even if the topic itself is valid

### Follow-up Action
After verification, the incomplete skill should be flagged for rebuild. The skill's SKILL.md and references need regeneration to include actual Qwen content.

## Long Prompts with Ollama (JSON File Technique)

For prompts longer than ~500 chars, **always use a temp JSON file** instead of inline JSON to avoid bash escaping issues on Windows (git-bash):

```bash
# BAD — syntax errors with long Turkish/unicode prompts:
curl -s -X POST http://localhost:11434/api/generate \
  -d '{"model":"qwen2.5-coder:7b","prompt":"Uzun Turkce prompt...","stream":false}'

# GOOD — write payload to file, use -d @file:
echo '{"model":"qwen2.5-coder:7b","prompt":"Uzun Turkce prompt...","stream":false}' > /tmp/ollama_prompt.json
curl -s --max-time 180 -X POST http://localhost:11434/api/generate -d @/tmp/ollama_prompt.json
```

The `@` syntax avoids bash parsing of the JSON body entirely. The shell reads the file and passes it as stdin to curl. Clean up temp files after use.

## Pitfalls

### Ollama-specific
- **Never use `ollama run` in a script** — it requires PTY and doesn't work in background. Always use `curl -X POST http://localhost:11434/api/generate`
- **Python `json.dumps` uses `False` not `false`** — `{'stream':False}` is correct, `{'stream':false}` gives NameError
- **Timeout:** set `--max-time 120` on curl; larger models may need 180-300s
- **Long prompts break on bash:** use `-d @/tmp/file.json` instead of inline JSON to avoid quoting/escaping issues with Turkish characters, parentheses, and line breaks
- **Response extraction from JSON:** pipe through `python3 -c "import sys,json; print(json.load(sys.stdin)['response'])"` — NOT shell text processing
- **Ollama deadlock:** if model hangs in "Stopping...", use `taskkill //F //IM ollama.exe` + `ollama serve &`
- **Lock cleanup:** delete lock file at script end to prevent stale locks

### Bash-specific
- **No parentheses in comments or echo** — `# (comment)` is parsed as subshell and causes syntax error. Use `# - comment` or `# / comment`
- **$((10#var))** for safe integer arithmetic from date values
- **`$SAAT=$(date '+%H:%M')`** — use `$()` not `$[]` (deprecated syntax)

### Cronjob-specific
- **Script path must be relative** — pass just the filename, keep script in `~/.hermes/scripts/`
- **Script runs before deliver prompt** — the deliver prompt must read files, not re-run the LLM
- **Repeat count** — `--repeat 24` for full day of hourly runs; `--repeat 8` for overnight (00-07)

## Related Skills

- `ollama-sohbet` — interactive multi-turn chat with Ollama models (complementary; for live sessions)
- `python-oto-debug-dongusu` — auto code debug loop (uses same curl REST API pattern)
- `webhook-subscriptions` — event-driven (not scheduled) agent runs

## Reference Scripts

- `scripts/python_ogrenim.sh` — Full example: hourly Python learning with qwen2.5-coder:7b, 12 topics, progress tracking to Desktop/python_ogrenim/
