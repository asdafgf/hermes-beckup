#!/bin/bash
# Yazilim Gelistirme Ogrenim - qwen2.5-coder:7b ile saatlik ogrenim
# Her saat basi bir yazilim gelistirme konusu islenir, rapor hazirlanir

MODEL="qwen2.5-coder:7b"
API_URL="http://localhost:11434/api/generate"
RAPOR_DIZINI="/c/Users/eymen/Desktop/yazilim_ogrenim"
LOCK_FILE="/tmp/yazilim_lock.txt"
KONU_DOSYASI="$RAPOR_DIZINI/konu_sirasi.txt"
PROGRESS_FILE="$RAPOR_DIZINI/progress.json"
SAAT=$(date '+%H:%M')
TARIH=$(date '+%Y-%m-%d %H:%M')

mkdir -p "$RAPOR_DIZINI"

# Lock kontrolu
if [ -f "$LOCK_FILE" ]; then
    LOCK_SAAT=$(cat "$LOCK_FILE" 2>/dev/null)
    if [ "$LOCK_SAAT" = "$(date '+%H')" ]; then
        echo "[$TARIH] Bu saat zaten islenmis, atliyorum."
        exit 0
    fi
fi
echo "$(date '+%H')" > "$LOCK_FILE"

# Yazilim gelistirme konulari - pratik ve egitici
KONULAR=(
    "SOLID prensipleri: Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion. Her birini Python ornegiyle anlat."
    "Git branching stratejileri: Git Flow, GitHub Flow, Trunk-Based Development. Hangi durumda hangisi kullanilir, orneklerle anlat."
    "Clean Code: Anlamli isimlendirme, kucuk fonksiyonlar, YAGNI, DRY, KISS prensipleri. Kotu ve iyi kod karsilastirmasi yap."
    "Test stratejileri: Unit test, Integration test, End-to-End test. PyTest ile Mock nedir, ne zaman kullanilir. Ornek kod ver."
    "REST API tasarimi: HTTP metodlari, status code'lar, versioning, pagination, HATEOAS. Flask ile ornek API yaz."
    "Veritabani normalizasyonu: 1NF, 2NF, 3NF, BCNF. Ornek bir e-ticaret veritabani uzerinden anlat. SQL sorgulari goster."
    "Design Patterns: Singleton, Factory, Observer, Strategy, Decorator. Her birini Python ornegiyle anlat. Ne zaman kullanilmali?"
    "Microservices mimarisi: Monolith vs Microservices, Service mesh, API Gateway, Event-driven architecture. Ne zaman microservices gecmeli?"
    "Docker ve Containerization: Dockerfile, docker-compose, multi-stage build, volume, network. Bir web uygulamasi Dockerize etme ornegi."
    "CI/CD pipeline: Continuous Integration, Continuous Delivery/Deployment. GitHub Actions ile ornek pipeline yaz. Test, build, deploy asamalari."
    "GraphQL vs REST: GraphQL'in avantajlari ve dezavantajlari. Query, Mutation, Subscription. Hangi durumda GraphQL kullanilmali?"
    "Concurrency ve Parallelism: Threading, Multiprocessing, AsyncIO. Python'da GIL nedir, ne zaman hangisini kullanmaliyiz?"
    "API Security: Authentication vs Authorization, JWT, OAuth2, API Keys, Rate Limiting. Guvenli bir API nasil yazilir?"
    "Cod Review en iyi uygulamalari: Ne aranmali, nasil feedback verilmeli, kod standartlari, security review checklist. Ornek review yap."
    "Veri yapilari: Array, Linked List, Stack, Queue, Tree, Hash Table. Her birinin zaman karmasikligi ve Python ornegi."
    "System Design: Bir sosyal medya platformu nasil tasarlanir? Scaling, caching, database sharding, CDN, load balancing."
    "Agile ve Scrum: Sprint planlama, daily standup, retrospective, hikaye puanlama. Bir sprint nasil yonetilir?"
)

SIRKAT=1
if [ -f "$KONU_DOSYASI" ]; then
    SIRKAT=$(cat "$KONU_DOSYASI")
fi

TOP_KONU=${#KONULAR[@]}

if [ $SIRKAT -gt $TOP_KONU ]; then
    SIRKAT=1
fi

KONU_ADI="Konu $SIRKAT/$TOP_KONU"
KONU_ICERIK="${KONULAR[$((SIRKAT-1))]}"

PROMPT="Sen bir yazilim gelistirme egitmenisin. Su konuyu detayli, egitici ve orneklerle anlat:

$KONU_ICERIK

Kesinlikle:
- Kod ornekleri ver Python ile
- Neden ve nasil calistigini acikla
- Best practices belirt
- Yaygin hatalardan bahset
- Gercek hayat kullanim senaryosu ekle

Turkce cevap ver. Kisa ve oz ol. MAX 400 kelime."

python -c "
import json
print(json.dumps({'model':'$MODEL','prompt':'''$PROMPT''','stream':False,'options':{'num_predict':1024}}))
" > /tmp/yazilim_payload.json

CEVAP=$(curl -s --max-time 120 -X POST "$API_URL" -d @/tmp/yazilim_payload.json 2>&1)
CEVAP=$(echo "$CEVAP" | python -c "
import sys,json
try:
    d=json.load(sys.stdin)
    print(d.get('response',''))
except:
    print('HATA: Yanit alinamadi - model busy olabilir')
")

DOSYA="$RAPOR_DIZINI/konu_${SIRKAT}_$(date '+%H%M').md"
cat > "$DOSYA" << EOF
# $KONU_ADI
**Tarih:** $TARIH

## Konu
$KONU_ICERIK

## Ogrenilenler
$CEVAP
EOF

echo "{\"son_konu\":$SIRKAT,\"toplam\":$TOP_KONU,\"tarih\":\"$TARIH\",\"konu\":\"${KONU_ICERIK:0:50}\"}" > "$PROGRESS_FILE"
echo $((SIRKAT + 1)) > "$KONU_DOSYASI"

echo "[$TARIH] $KONU_ADI tamamlandi. Konular bitti: $((SIRKAT * 100 / TOP_KONU))%"
rm -f "$LOCK_FILE"
rm -f /tmp/yazilim_payload.json
