#!/bin/bash
# ===================================================================
# qwen_api_wrapper.sh — Qwen2.5-coder REST API çağrısı
# ===================================================================
# Kullanım:
#   bash qwen_api_wrapper.sh "prompt metni" [model_adı] [max_timeout]
#
# Örnekler:
#   bash qwen_api_wrapper.sh "Python port taraması nedir?"
#   bash qwen_api_wrapper.sh "Uzun analiz" qwen2.5-coder:7b 180
#
# Bu script `ollama run`'ın PTY gerektirme sorununu çözer.
# REST API (http://localhost:11434/api/generate) kullanır.
# ===================================================================

PROMPT="${1:-Merhaba}"
MODEL="${2:-qwen2.5-coder:7b}"
TIMEOUT="${3:-120}"

# JSON payload oluştur (Python ile, güvenli kaçış için)
PAYLOAD=$(python -c "
import json
prompt = '''$PROMPT'''
print(json.dumps({'model': '$MODEL', 'prompt': prompt, 'stream': False}))
")

# API çağrısı
RESPONSE=$(curl -s --max-time "$TIMEOUT" -X POST http://localhost:11434/api/generate -d "$PAYLOAD" 2>&1)
CURL_EXIT=$?

if [ $CURL_EXIT -ne 0 ] || [ -z "$RESPONSE" ]; then
  echo "[HATA] Qwen API yanıt vermedi (exit: $CURL_EXIT)"
  
  # Deadlock kontrolü — Ollama stopping state'inde olabilir
  OLLAMA_STATUS=$(ollama ps 2>/dev/null | grep "Stopping")
  if [ -n "$OLLAMA_STATUS" ]; then
    echo "[HATA] Ollama Stopping state'inde — yeniden başlatılıyor..."
    taskkill //F //IM ollama.exe 2>/dev/null
    sleep 2
    ollama serve 2>/dev/null &
    sleep 3
    echo "[HATA] Tekrar deneniyor..."
    RESPONSE=$(curl -s --max-time "$TIMEOUT" -X POST http://localhost:11434/api/generate -d "$PAYLOAD" 2>&1)
  fi
fi

# JSON'dan response çıkar
echo "$RESPONSE" | python -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('response', ''))
except:
    sys.exit(1)
" 2>/dev/null
