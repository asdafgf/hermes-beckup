#!/bin/bash
# Python Ogrenim Oturumu - qwen2.5-coder:7b ile saatlik ogrenim
# Her saat basi bir Python konusu islenir, rapor hazirlanir

MODEL="qwen2.5-coder:7b"
API_URL="http://localhost:11434/api/generate"
RAPOR_DIZINI="/c/Users/eymen/Desktop/python_ogrenim"
LOCK_FILE="/tmp/python_ogrenim_lock.txt"
KONU_DOSYASI="$RAPOR_DIZINI/konu_sirasi.txt"
PROGRESS_FILE="$RAPOR_DIZINI/progress.json"
SAAT=$(date '+%H:%M')
TARIH=$(date '+%Y-%m-%d %H:%M')

mkdir -p "$RAPOR_DIZINI"

# Lock kontrolu - ayni anda calismasin
if [ -f "$LOCK_FILE" ]; then
    LOCK_SAAT=$(cat "$LOCK_FILE" 2>/dev/null)
    if [ "$LOCK_SAAT" = "$(date '+%H')" ]; then
        echo "[$TARIH] Bu saat zaten islenmis, atliyorum."
        exit 0
    fi
fi
echo "$(date '+%H')" > "$LOCK_FILE"

# Python konulari sirasi
KONULAR=(
    "Python decorators: nedir, nasil calisir, real-world kullanim ornekleri. Detayli acikla ve kod ornegi ver."
    "Python generators ve yield: iterator protocol, generator expressions, memory avantajlari. Orneklerle anlat."
    "Python context managers: with statement, __enter__/__exit__, contextlib, real-world kullanim. Kod ornegi ver."
    "Python metaprogramming: type(), metaclasses, __new__ vs __init__, orneklerle acikla."
    "Python asyncio: event loop, coroutines, tasks, await/async, ornek uygulama."
    "Python multiprocessing vs threading: GIL, Process/Thread pools, Queue, Pipe, ornekler."
    "Python data classes ve attrs: @dataclass, field, __post_init__, frozen, ornekler."
    "Python __slots__: memory optimization, nasil calisir, ne zaman kullanilir. Ornek kod."
    "Python functools: lru_cache, partial, wraps, reduce, singledispatch. Kapsamli ornek."
    "Python typing ve type hints: Union, Optional, Literal, TypedDict, Protocol, ornekler."
    "Python itertools: chain, cycle, permutations, combinations, groupby, product. Ornek."
    "Python descriptors: __get__, __set__, __delete__, property altinda yatan mekanizma."
)

# Kacinci konuda oldugumuzu bul
SIRKAT=1
if [ -f "$KONU_DOSYASI" ]; then
    SIRKAT=$(cat "$KONU_DOSYASI")
fi

TOP_KONU=${#KONULAR[@]}

if [ $SIRKAT -gt $TOP_KONU ]; then
    SIRKAT=1  # Basa don
fi

KONU_ADI="Konu $SIRKAT/$TOP_KONU"
KONU_ICERIK="${KONULAR[$((SIRKAT-1))]}"

# qwen'e sor - curl REST API
qwen_sor() {
    local prompt="$1"
    local payload
    payload=$(python -c "import json; print(json.dumps({'model':'$MODEL','prompt':'''$prompt''','stream':False,'options':{'num_predict':1024}}))" 2>/dev/null)

    local response=""
    for attempt in 1 2 3; do
        response=$(curl -s --max-time 120 -X POST "$API_URL" -d "$payload" 2>&1)
        if [ -n "$response" ] && echo "$response" | python -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
            break
        fi
        if [ $attempt -lt 3 ]; then
            sleep 5
        fi
    done

    echo "$response" | python -c "
import sys,json
try:
    d=json.load(sys.stdin)
    print(d.get('response',''))
except:
    print('HATA: Yanit alinamadi')
" 2>/dev/null
}

# Prompt'u hazirla
PROMPT="Sen bir Python egitmenisin. Su konuyu detayli, egitici ve orneklerle anlat:

$KONU_ICERIK

Kesinlikle:
- Kod ornekleri ver
- Neden ve nasil calistigini acikla
- Best practices belirt
- Yaygin hatalardan bahset
- Gercek hayat kullanim senaryosu ekle

Turkce cevap ver. Kisa ve oz ol. MAX 500 kelime."

echo "[$TARIH] $KONU_ADI basladi: ${KONU_ICERIK:0:50}..."

# Qwen'e sor
CEVAP=$(qwen_sor "$PROMPT")

# Kaydet
DOSYA="$RAPOR_DIZINI/konu_${SIRKAT}_$(date '+%H%M').md"
cat > "$DOSYA" << EOF
# $KONU_ADI: ${KONU_ICERIK:0:80}
**Tarih:** $TARIH

## Konu
$KONU_ICERIK

## Ogrenilenler
$CEVAP
EOF

# Progress guncelle
echo "{\"son_konu\":$SIRKAT,\"toplam\":$TOP_KONU,\"tarih\":\"$TARIH\",\"konu\":\"${KONU_ICERIK:0:50}\"}" > "$PROGRESS_FILE"

# Konu sirasini bir artir
echo $((SIRKAT + 1)) > "$KONU_DOSYASI"

echo "[$TARIH] $KONU_ADI tamamlandi."

# Lock temizle
rm -f "$LOCK_FILE"
