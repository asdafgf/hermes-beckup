#!/bin/bash
# OTONOM ÖĞRENME — İnternetten bulunan konuyu qwen'e sor, skill kaydet
# Kullanım: bash qwen_otonomegitim.sh "BASLIK" "ID" "KATEGORI" "PROMPT"
# Detay: skill_view('hermes-gemini-copilot')

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_BASE="$HOME/.hermes/skills/security"
REGISTRY="$SCRIPT_DIR/.qwen_registry_v2"
LOCK="$SCRIPT_DIR/.qwen_lock"

mkdir -p "$SKILLS_BASE"
touch "$REGISTRY"

# Lock kontrolü
if [ -f "$LOCK" ]; then
  lock_age=$(($(date +%s) - $(stat -c %Y "$LOCK" 2>/dev/null || echo 0)))
  if [ $lock_age -lt 600 ]; then exit 1; fi
fi
echo $$ > "$LOCK"

# Saat kontrolü
h=$(date '+%H'); hn=$((10#$h))
if [ "$hn" -ge 8 ] && [ "$hn" -lt 23 ]; then rm -f "$LOCK"; exit 0; fi

# Parametre kontrolü
if [ $# -lt 4 ]; then rm -f "$LOCK"; exit 1; fi

BASLIK="$1"; KONU_ID="$2"; KATEGORI="$3"; PROMPT="$4"
SAD=$(echo "$BASLIK" | sed 's/ş/s/g;s/ğ/g/g;s/ü/u/g;s/ö/o/g;s/ı/i/g;s/ç/c/g;s/ /-/g;s/[^a-zA-Z0-9_-]//g' | tr '[:upper:]' '[:lower:]' | cut -c1-50)

# Tekrar kontrolü
grep -q "^$KONU_ID|" "$REGISTRY" 2>/dev/null && { echo "⏭️ TEKRAR"; rm -f "$LOCK"; exit 0; }

# Qwen'e sor (REST API, PTY gerekmez)
QWEN=$(python -c "import json; print(json.dumps({'model':'qwen2.5-coder:7b','prompt':'''$PROMPT''','stream':False}))" | curl -s --max-time 120 -X POST http://localhost:11434/api/generate -d @- | python -c "import sys,json; print(json.load(sys.stdin).get('response',''))")

# Skill kaydet
SKILL_DIR="$SKILLS_BASE/$SAD"; mkdir -p "$SKILL_DIR/references"
echo "$QWEN" > "$SKILL_DIR/references/qwen_yanit.txt"

cat > "$SKILL_DIR/SKILL.md" <<EOF
---
name: $SAD
description: "Otonom öğrenme: $BASLIK"
version: 1.0.0
author: Hermes + qwen2.5-coder
metadata:
  hermes:
    tags: [security, otonom-ogrenme, $KATEGORI]
    source: internet + qwen2.5-coder:7b
    konu_id: $KONU_ID
---
# $BASLIK
## Qwen2.5-coder Yanıtı
\`\`\`
$(echo "$QWEN" | head -10)
\`\`\`
⚠️ **EĞİTİM AMAÇLIDIR**
EOF

echo "$KONU_ID|$SAD|$KATEGORI" >> "$REGISTRY"
echo "$KONU_ID|✅|$KATEGORI|$SAD|$(date '+%H:%M')|$BASLIK" >> "$SCRIPT_DIR/.qwen_report_v2"
echo "✅ SKILL #$(wc -l < "$REGISTRY") → $SAD"
rm -f "$LOCK"
