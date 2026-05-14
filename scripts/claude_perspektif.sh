#!/bin/bash
# Claude Code perspektifi - Qwen2.5-coder
MODEL="qwen2.5-coder:7b"
API_URL="http://localhost:11434/api/generate"

# Dokumani oku - sadece ilk 6000 karakter
DOC=$(head -c 6000 /c/Users/eymen/Desktop/python_ogrenim/tum_dokumanlar_8video.md)

PROMPT="Sen CLAUDE CODE'sun - Anthropic'in AI kodlama araci. 
Sana 8 YouTube videosundan cikarilmis AI agent skill'leri veriliyor.

SKILL LISTESI:
$DOC

ISTENEN:
1. AI Agent Kullanim Seviyeleri degerlendirmesi
2. AI Kodlama Araclari Karsilastirmasi - Hermes vs Codex vs OpenClaw vs Cursor vs Windsurf
3. AIOS konsepti hakkinda ne dusunuyorsun
4. Voice AI Agents ve Vapi degerlendirmesi
5. Skills Sistemi ve Self-Learning hakkinda gorusun
6. Prompt Muhendisligi onerileri

Claude Code olarak:
- Hangi skill'leri begendin, hangilerini eksik buldun?
- Hermes Agent, Codex, Cursor, Windsurf hakkinda ne dusunuyorsun?
- AIOS felsefesi hakkinda gorusun nedir?

Turkce yaz. MAX 1200 kelime."

python -c "
import json
print(json.dumps({'model':'$MODEL','prompt':'''$PROMPT''','stream':False,'options':{'num_predict':2048}}))
" > /tmp/claude_payload.json

RESPONSE=$(curl -s --max-time 180 -X POST "$API_URL" -d @/tmp/claude_payload.json 2>&1)
echo "$RESPONSE" | python -c "
import sys,json
try:
    d=json.load(sys.stdin)
    print(d.get('response',''))
except Exception as e:
    print(f'HATA: {e}')
" > /c/Users/eymen/Desktop/python_ogrenim/claude_code_skill_cikti.md

echo "=== CLAUDE CODE CIKTISI YAZILDI ==="
cat /c/Users/eymen/Desktop/python_ogrenim/claude_code_skill_cikti.md
