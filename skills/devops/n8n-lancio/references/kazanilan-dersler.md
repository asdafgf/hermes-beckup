# Kazanılan Dersler (2026-05-11)

## n8n Öğrenme Süreci

### Kullanıcı Preferansı: Terminal değil, GUI'de adım adım
- Kullanıcı "n8n'de döngü yap" dediğinde, terminalde kod yazmak yerine Chrome'da n8n GUI'sini açıp adım adım anlat
- "Yap, terminalde gör" yerine "Chrome'da aç, şu adımları takip et" yaklaşımı

### Kullanıcı Preferansı: Otomatik durum tespiti
- "n8n çalışır" dediğinde: direkt çalışıyor mu kontrol et
- "Bana sorma, öğren" dediğinde: bu kalıcı kuraldır, skill'e ekle
- Sorulması gerekenler: sadece karar gerektirenler (reset, yeni workflow türü, şifre sıfırlama)

### n8n API Kullanımı
- Login: POST /rest/login (email + password) -> cookie
- Cookie ile işlem: --cookie-jar ile kaydet
- Workflow oluşturma: POST /rest/workflows (JSON body)
- Workflow aktifleştirme: POST /rest/workflows/{id}/activate (versionId gerekli)
- Execution listeleme: GET /rest/executions?workflowId={id}
- Örnek workflow JSON'u references/n8n-api-workflow.md'de

## Kamera Bulma (XCLYCM)
- IP: 192.168.0.17
- Portlar: 80 (HTTP), 554 (RTSP), 443 (HTTPS) açık
- MAC: E0:BA:AD:17:B1:84 (Hangzhou Hikvision üretimi)
- RTSP için auth gerekli (kullanıcı kurulumda şifre belirlemiş)
- HTTP snapshot: /onvif/snapshot (401 döndü -> auth gerekli)
- ONVIF: destekliyor ama auth required
- RTSP path: bilinmiyor (tüm standart yollar + auth denenemedi)
- Çözüm: reset düğmesine bas (ataçla 10sn)
