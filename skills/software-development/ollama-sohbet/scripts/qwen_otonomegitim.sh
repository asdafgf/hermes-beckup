#!/bin/bash
# qwen_otonomegitim.sh — Otonom öğrenme: İnternetten konu bul, qwen'e sor, skill kaydet
# Kullanım: bash qwen_otonomegitim.sh "BASLIK" "KONU_ID" "KATEGORI" "PROMPT"
#
# Bu script:
# 1. Qwen API'ye (curl ile REST) prompt'u gönderir
# 2. Yanıtı ~/.hermes/skills/security/<skill>/references/qwen_yanit.txt kaydeder
# 3. SKILL.md oluşturur
# 4. Registry'ye kaydeder (tekrar kontrolü)
# 5. Rapor dosyasına ekler
#
# 14 May 2026: ollama run yerine curl REST API kullanır (PTY gerektirmez)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_BASE="$HOME/.hermes/skills/security"
REGISTRY="$SCRIPT_DIR/.qwen_registry_v2"
LOCK="$SCRIPT_DIR/.qwen_lock"

mkdir -p "$SKILLS_BASE"
touch "$REGISTRY"

gece_mi() {
  local h=$(date '+%H')
  local hn=$((10#$h))
  [ "$hn" -ge 23 ] || [ "$hn" -lt 8 ]
}

skill_adi() {
  echo "$1" | sed 's/ş/s/g;s/Ş/S/g;s/ğ/g/g;s/Ğ/G/g;s/ü/u/g;s/Ü/U/g;s/ö/o/g;s/Ö/O/g;s/ı/i/g;s/İ/I/g;s/ç/c/g;s/Ç/C/g' | sed 's/ /-/g;s/[^a-zA-Z0-9_-]//g' | tr '[:upper:]' '[:lower:]' | cut -c1-50
}

qwen_sor() {
  local prompt="$1"
  local payload=$(python -c "import json; print(json.dumps({'model':'qwen2.5-coder:7b','prompt':'''$prompt''','stream':False}))" 2>/dev/null)
  local response=""
  for attempt in 1 2; do
    response=$(curl -s --max-time 120 -X POST http://localhost:11434/api/generate -d "$payload" 2>&1)
    if [ -n "$response" ]; then break; fi
    sleep 3
  done
  echo "$response" | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('response',''))" 2>/dev/null
}

# Lock kontrol
if [ -f "$LOCK" ]; then
  lock_age=$(($(date +%s) - $(stat -c %Y "$LOCK" 2>/dev/null || echo 0)))
  [ $lock_age -lt 600 ] && exit 1
fi
echo $$ > "$LOCK"

# Argüman kontrolü
if [ $# -lt 4 ]; then echo "[HATA] Kullanim: $0 BASLIK ID KATEGORI PROMPT"; rm -f "$LOCK"; exit 1; fi

BASLIK="$1"; KONU_ID="$2"; KATEGORI="$3"; PROMPT="$4"
SAD=$(skill_adi "$BASLIK")

# Tekrar kontrolü
if grep -q "^$KONU_ID|" "$REGISTRY" 2>/dev/null; then
  echo "TEKRAR — atlandi"; rm -f "$LOCK"; exit 0
fi

echo "--- [$KONU_ID] $BASLIK ---"
QWEN_CEVAP=$(qwen_sor "$PROMPT")

# Skill kaydet
SKILL_DIR="$SKILLS_BASE/$SAD"
mkdir -p "$SKILL_DIR/references"
echo "$QWEN_CEVAP" > "$SKILL_DIR/references/qwen_yanit.txt"

cat > "$SKILL_DIR/SKILL.md" << EOF
---
name: $SAD
description: "Otonom ogrenme: $BASLIK"
version: 1.0.0
author: Hermes + qwen2.5-coder
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [security, otonom-ogrenme, $KATEGORI]
    source: internet + qwen2.5-coder:7b
    konu_id: $KONU_ID
---
# $BASLIK

## Kaynak
Internetten bulunan konu, qwen2.5-coder:7b ile islenmistir.

## Qwen2.5-coder Yaniti
\`\`\`
$(echo "$QWEN_CEVAP" | head -20)
\`\`\`

## Onemli Uyari
**EGITIM AMACLIDIR** — Bu skill'deki tum bilgiler teoriktir.
- Qwen2.5-coder tamamen yerel (localhost) calisir, internete erisimi YOKTUR
- Hicbir bilgi disari sizmaz, tum islem local GPU'dadir
- Anlatilan teknikler KESINLIKLE izinsiz sistemlerde denenmemelidir
- Sadece kendi sistemlerinizde ve etik sinirlar icinde kullanin
EOF

echo "$KONU_ID|$SAD|$KATEGORI" >> "$REGISTRY"
echo "SKILL KAYDEDILDI: $SAD"
rm -f "$LOCK"
