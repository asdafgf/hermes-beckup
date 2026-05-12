# n8n API ile Workflow Oluşturma

Bu referans, n8n'in REST API'sini kullanarak programatik olarak workflow oluşturma, aktifleştirme ve execution'ları izleme adımlarını içerir.

## Kimlik Doğrulama

n8n'de cookie/session-based auth kullanılır:

```bash
# Login
curl -s -c /tmp/n8n-cookies.txt -X POST http://localhost:5678/rest/login \
  -H "Content-Type: application/json" \
  -d '{"email":"markopasa_@hotmail.com","password":"123456"}'
```

Not: n8n'in farklı versiyonlarında field adı değişebilir. 2.19.5'te `emailOrLdapLoginId` ek alanı da istenebilir.

## Workflow Oluşturma

```bash
curl -s -b /tmp/n8n-cookies.txt -X POST http://localhost:5678/rest/workflows \
  -H "Content-Type: application/json" \
  -d '{
  "name": "Workflow Adı",
  "nodes": [
    {
      "id": "uuid-node-1",
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.1,
      "position": [250, 300],
      "parameters": {
        "rule": {
          "interval": [{"field": "seconds", "secondsInterval": 5}]
        }
      }
    },
    {
      "id": "uuid-node-2",
      "name": "Set",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [450, 300],
      "parameters": {
        "values": {
          "string": [
            {"name": "mesaj", "value": "Merhaba!"},
            {"name": "zaman", "value": "={{ $now.format(\"HH:mm:ss\") }}"}
          ]
        },
        "options": {}
      }
    },
    {
      "id": "uuid-node-3",
      "name": "NoOp",
      "type": "n8n-nodes-base.noOp",
      "typeVersion": 1,
      "position": [650, 300],
      "parameters": {}
    }
  ],
  "connections": {
    "Schedule Trigger": {
      "main": [[{"node": "Set", "type": "main", "index": 0}]]
    },
    "Set": {
      "main": [[{"node": "NoOp", "type": "main", "index": 0}]]
    }
  },
  "active": false,
  "settings": {
    "executionOrder": "v1"
  }
}'
```

## Workflow'u Aktifleştirme

```bash
# ID'yi al (response'daki data.id)
WORKFLOW_ID="B6Seavaq4A4x4LJg"

# Önce versionId'yi al
VERSION=$(curl -s -b /tmp/n8n-cookies.txt "http://localhost:5678/rest/workflows/$WORKFLOW_ID" | \
  python -c "import sys,json; print(json.load(sys.stdin)['data']['versionId'])")

# Aktif et
curl -s -b /tmp/n8n-cookies.txt -X POST \
  "http://localhost:5678/rest/workflows/$WORKFLOW_ID/activate" \
  -H "Content-Type: application/json" \
  -d "{\"versionId\":\"$VERSION\"}"
```

## Execution'ları İzleme

```bash
curl -s -b /tmp/n8n-cookies.txt \
  "http://localhost:5678/rest/executions?workflowId=$WORKFLOW_ID&limit=5" | \
  python -c "import sys,json; data=json.load(sys.stdin)
for e in data['data']['results'][:5]:
  print(f\"  [{e['status']}] {e['startedAt']}\")"
```

## Schedule Trigger Konfigürasyonu

Her 5 saniye:
```json
{"rule": {"interval": [{"field": "seconds", "secondsInterval": 5}]}}
```

Her dakika:
```json
{"rule": {"interval": [{"field": "minutes", "minutesInterval": 1}]}}
```

Her gün saat 09:00:
```json
{"rule": {"hour": 9, "minute": 0}}
```

## Notlar
- n8n 2.19.5'te `PATCH /rest/workflows/:id` ile `active:true` göndermek çalışmaz — `/activate` endpoint'i kullanılmalı
- `versionId` zorunlu — güncel versionId'yi GET ile al
- Cookie'ler `/tmp/n8n-cookies.txt`'de saklanır, `-b` ile her istekte gönderilir
- Chrome'da açmak için: `http://localhost:5678/workflow/<WORKFLOW_ID>`
