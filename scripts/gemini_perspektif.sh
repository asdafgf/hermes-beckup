#!/bin/bash
# Gemini perspektifi - Qwen2.5-coder
MODEL="qwen2.5-coder:7b"
API_URL="http://localhost:11434/api/generate"

# Dokumanin ikinci yarisini oku
tail -c +6001 /c/Users/eymen/Desktop/python_ogrenim/tum_dokumanlar_8video.md | head -c 6000 > /tmp/doc_part2.txt
DOC2=$(cat /tmp/doc_part2.txt)

PROMPT="Sen GEMINI'sin - Google'in AI modeli.
Sana 8 YouTube videosundan cikarilmis AI agent skill'leri veriliyor.

SKILL LISTESI:
$DOC2

ISTENEN:
1. AI Agent Kullanim Seviyeleri degerlendirmesi
2. AI Kodlama Araclari Karsilastirmasi
3. AIOS konsepti degerlendirmesi
4. Voice AI Agents ve Vapi
5. Skills Sistemi ve Self-Learning
6. Prompt Muhendisligi

Gemini olarak:
- Bu skill'leri nasil buluyorsun?
- Hangi yaklasimlari begendin, hangilerini eksik buluyorsun?
- Kendi yeteneklerinle karsilastirir misin?
- AI agent ekosistemi hakkinda genel degerlendirmen nedir?

Turkce yaz. MAX 1200 kelime."

python -c "
import json
print(json.dumps({'model':'$MODEL','prompt':'''$PROMPT''','stream':False,'options':{'num_predict':2048}}))
" > /tmp/gemini_payload.json

RESPONSE=$(curl -s --max-time 180 -X POST "$API_URL" -d @/tmp/gemini_payload.json 2>&1)
echo "$RESPONSE" | python -c "
import sys,json
try:
    d=json.load(sys.stdin)
    print(d.get('response',''))
except Exception as e:
    print(f'HATA: {e}')
" > /c/Users/eymen/Desktop/python_ogrenim/gemini_skill_cikti.md

echo "=== GEMINI CIKTISI YAZILDI ==="
cat /c/Users/eymen/Desktop/python_ogrenim/gemini_skill_cikti.md
