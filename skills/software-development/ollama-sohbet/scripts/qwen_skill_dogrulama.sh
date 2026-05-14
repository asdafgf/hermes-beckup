#!/bin/bash
# qwen_skill_dogrulama.sh — Tüm skill'leri qwen2.5-coder ile doğrula
# Kullanım: bash qwen_skill_dogrulama.sh
#
# Her skill'in qwen_yanit.txt içeriğini qwen'e gönderip doğrulatır.
# Doğruysa "DOGRU", hatalıysa "HATALI + düzeltme" kaydeder.
# 14 May 2026: curl REST API kullanır (ollama run DEĞİL)

SKILLS_DIR="$HOME/.hermes/skills/security"
REPORT="$HOME/.hermes/scripts/.verify_report.txt"
rm -f "$REPORT"

TOTAL=0; DOGRU=0; HATA=0

for skill_dir in "$SKILLS_DIR"/*/; do
  [ ! -d "$skill_dir" ] && continue
  SKILL_NAME=$(basename "$skill_dir")
  TOTAL=$((TOTAL + 1))
  
  BASLIK=$(grep "^# " "$skill_dir/SKILL.md" 2>/dev/null | head -1 | sed 's/^# //')
  [ -z "$BASLIK" ] && BASLIK="$SKILL_NAME"
  
  echo "  [$TOTAL] $BASLIK"
  
  PAYLOAD=$(python -c "import json; prompt='Şu konuyu doğrula: \"$BASLIK\". Doğruysa \"DOGRU\", hatalıysa \"HATALI: ...\" yaz.'; print(json.dumps({'model':'qwen2.5-coder:7b','prompt':prompt,'stream':False}))")
  CEVAP=$(curl -s --max-time 120 -X POST http://localhost:11434/api/generate -d "$PAYLOAD" 2>&1)
  SONUC=$(echo "$CEVAP" | python -c "import sys,json; d=json.load(sys.stdin); r=d.get('response',''); print(r[:150])" 2>/dev/null)
  
  if echo "$SONUC" | grep -qi "dogru"; then
    echo "    $SONUC"; DOGRU=$((DOGRU + 1))
    echo "$SKILL_NAME||$BASLIK" >> "$REPORT"
  else
    echo "    $SONUC"; HATA=$((HATA + 1))
    echo "$SKILL_NAME||$BASLIK" >> "$REPORT"
    # Düzeltme iste
    DUZELT_PAYLOAD=$(python -c "import json; prompt='Şu konuyu düzelt: \"$BASLIK\". 3-4 cümle.'; print(json.dumps({'model':'qwen2.5-coder:7b','prompt':prompt,'stream':False}))")
    DUZELT_CEVAP=$(curl -s --max-time 120 -X POST http://localhost:11434/api/generate -d "$DUZELT_PAYLOAD" 2>&1)
    DUZELT=$(echo "$DUZELT_CEVAP" | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('response',''))" 2>/dev/null)
    [ -n "$DUZELT" ] && echo "$DUZELT" > "$skill_dir/references/qwen_yanit_dogrulanmis.txt"
  fi
  sleep 4
done

echo "OZET: $TOTAL skill | Dogru: $DOGRU | Hatali: $HATA"
