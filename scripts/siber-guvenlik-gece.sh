#!/bin/bash
# SIBER GUVENLIK GECE OTURUMU
# Parantez kullanilmadi - bash syntax hatasi riski yok

MODEL="gemma4:latest"
MAX_RETRY=3
RETRY_FILE="/tmp/siber_retry_count.txt"

if [ -f "$RETRY_FILE" ]; then
  RETRY_COUNT=$(cat "$RETRY_FILE")
else
  RETRY_COUNT=0
fi

run_safe() {
  local question="$1"
  local label="$2"
  local retry=0
  
  while [ $retry -lt $MAX_RETRY ]; do
    echo "$question" | ollama run $MODEL 2>/dev/null
    local result=$?
    if [ $result -eq 0 ]; then
      echo 0 > "$RETRY_FILE"
      return 0
    fi
    retry=$((retry + 1))
    sleep 5
  done
  
  RETRY_COUNT=$(cat "$RETRY_FILE" 2>/dev/null || echo 0)
  RETRY_COUNT=$((RETRY_COUNT + 1))
  echo "$RETRY_COUNT" > "$RETRY_FILE"
  
  if [ $RETRY_COUNT -ge 3 ]; then
    ollama serve 2>/dev/null &
    sleep 10
    echo 0 > "$RETRY_FILE"
  fi
  
  echo "$question" | ollama run $MODEL 2>/dev/null
}

SAAT=$(date '+%H:%M')
echo "=== SIBER GUVENLIK — Devam $SAAT ==="
echo "Model: $MODEL"
echo ""

# KONU 1: Agentic AI -- 1.1 tamam, 1.2'den devam
echo "=== KONU 1/15: Agentic AI ==="
run_safe "1.2 AI destekli saldirilar geleneksel savunmalari nasil asiyor? 2026'da hangi yeni vektorler ortaya cikti?" "K1.2"
run_safe "1.3 Agentic AI ile SOC otomasyonu nasil calisir? AI tehdit avciliginda insanin yerini alabilir mi?" "K1.3"
run_safe "1.4 Prompt injection saldirilari nedir? LLM'lere karsi hangi savunmalar gelistirildi?" "K1.4"
run_safe "1.5 Otonom AI ajanlari kesif yapip sizabilir mi? Saldiri zincirini tamamlama senaryolari." "K1.5"
run_safe "1.6 Shadow AI nedir? Calisanlarin izinsiz AI araclari hangi veri sizintilarina yol acar?" "K1.6"
sleep 3

# KONU 2: Deepfake
echo "=== KONU 2/15: Deepfake ve Kimlik Aldatmaca ==="
run_safe "2.1 Gercek zamanli deepfake 2026'da hangi seviyede? Video ve ses nasil klonlaniyor?" "K2.1"
run_safe "2.2 Deepfake ile ise alim dolandiriciligi nasil yapiliyor?" "K2.2"
run_safe "2.3 Deepfake tespit yontemleri ve CP2A standardi nedir?" "K2.3"
run_safe "2.4 Biyometrik dogrulama ve liveness detection deepfake'i yenebilir mi?" "K2.4"
run_safe "2.5 Guven kodu sistemi ile yonetici kimligine burunme nasil onlenir?" "K2.5"
sleep 3

# KONU 3: Zero Trust
echo "=== KONU 3/15: Zero Trust ==="
run_safe "3.1 Zero Trust prensipleri neler? Asla guvenme her zaman dogrula nasil uygulanir?" "K3.1"
run_safe "3.2 Identity-first security nedir? Kimlik neden yeni guvenlik duvari?" "K3.2"
run_safe "3.3 Mikro segmentasyon ag icinde yanal hareketi nasil engeller? Gercek dunya ornegi." "K3.3"
run_safe "3.4 Zero Trust'da surekli dogrulama nasil calisir? Cihaz sagligi ve davranis analizi." "K3.4"
run_safe "3.5 Zero Trust adaptasyonundaki en buyuk engeller neler?" "K3.5"
run_safe "3.6 ZTNA ile VPN arasindaki farklar neler?" "K3.6"
sleep 3

# KONU 4: Tedarik Zinciri
echo "=== KONU 4/15: Tedarik Zinciri ==="
run_safe "4.1 Tedarik zinciri saldirilari neden 2026'nin en buyuk tehdidi? SolarWinds benzeri saldirilar." "K4.1"
run_safe "4.2 SBOM nedir ve neden her sirket dijital malzeme listesi cikarmali?" "K4.2"
run_safe "4.3 Acik kaynak guvenligi: Log4j benzeri zafiyetlerde ne yapilmali?" "K4.3"
run_safe "4.4 Tedarikci denetim sozlesmeleri 2026'da nasil degisti?" "K4.4"
run_safe "4.5 API tedarik zinciri saldirilari: yuzde 97 tek istekle nasil gerceklesiyor?" "K4.5"
run_safe "4.6 Kucuk tedarikci zafiyeti buyuk sirketi nasil cokertir?" "K4.6"
sleep 3

# KONU 5: Regulasyon
echo "=== KONU 5/15: Regulasyon ve Uyum ==="
run_safe "5.1 2026'da siber regulasyonlardaki en buyuk degisiklikler neler? CISO'lar neden kisisel sorumlu?" "K5.1"
run_safe "5.2 GDPR HIPAA PCI DSS 2026'da nasil evrildi?" "K5.2"
run_safe "5.3 Yonetici kurulu uyeleri siber ihlallerden dava edilebilir mi?" "K5.3"
run_safe "5.4 Siber sigorta 2026'da hangi kosullari zorunlu kiliyor?" "K5.4"
run_safe "5.5 KVKK ve Turkiye'de CISO'larin yasal sorumluluklari neler?" "K5.5"
sleep 3

# KONU 6: Ransomware
echo "=== KONU 6/15: Ransomware ==="
run_safe "6.1 Ransomware 2026'da nasil evrildi? Cifte ve uclu santaj yontemleri." "K6.1"
run_safe "6.2 Onlemeden kurtulmaya gecis: Dayaniklilik stratejileri." "K6.2"
run_safe "6.3 3-2-1 yedekleme kurali ve ransomware korumasi nasil olmali?" "K6.3"
run_safe "6.4 Fidye odenmeli mi? Hukumetlerin tutumu nedir?" "K6.4"
run_safe "6.5 RaaS: Ransomware hizmet olarak nasil isliyor?" "K6.5"
run_safe "6.6 Saglik sektorunde ransomware: Hastaneler neden hedef?" "K6.6"
sleep 3

# KONU 7: API
echo "=== KONU 7/15: API Guvenligi ==="
run_safe "7.1 API guvenligi neden kritik? BOLA nedir?" "K7.1"
run_safe "7.2 AI ajanlari API'leri nasil tarar ve somurur?" "K7.2"
run_safe "7.3 Runtime behavioral monitoring neden statik WAF'tan daha etkili?" "K7.3"
run_safe "7.4 WAF ve API Gateway farki nedir?" "K7.4"
run_safe "7.5 GraphQL API guvenligi: REST'ten farkli tehditler neler?" "K7.5"
sleep 3

# KONU 8: Kuantum
echo "=== KONU 8/15: Kuantum Guvenligi ==="
run_safe "8.1 Kuantum bilgisayarlar sifrelemeyi ne zaman kirabilir? Topla simdi coz sonra stratejisi." "K8.1"
run_safe "8.2 PQC: NIST hangi algoritmalari onayladi?" "K8.2"
run_safe "8.3 RSA ve ECC'nin yerini hangi yontemler alacak?" "K8.3"
run_safe "8.4 Kripto envanteri: Hangi sistemler oncelikli?" "K8.4"
run_safe "8.5 Hibrit kuantum gecis yaklasimi nasil calisir?" "K8.5"
sleep 3

# KONU 9: CTEM
echo "=== KONU 9/15: CTEM ==="
run_safe "9.1 CTEM nedir? Geleneksel zafiyet taramasindan farki ne?" "K9.1"
run_safe "9.2 ASM: Dis saldiri yuzeyi yonetimi nasil calisir?" "K9.2"
run_safe "9.3 Dark web izleme ve tehdit istihbarati nasil calisir?" "K9.3"
run_safe "9.4 Shadow IT: Calisanlarin izinsiz bulut hizmetleri hangi riskleri tasir?" "K9.4"
run_safe "9.5 Binlerce zafiyetten kritik olanlar nasil onceliklendirilir?" "K9.5"
run_safe "9.6 Sertifika ve TLS yonetimi neden onemli?" "K9.6"
sleep 3

# KONU 10: Kariyer
echo "=== KONU 10/15: Kariyer ==="
run_safe "10.1 2026'da siber guvenlik is gucu acigi ne durumda?" "K10.1"
run_safe "10.2 SOC Analisti, Pentest, Bulut: Hangi kariyer yolu one cikiyor?" "K10.2"
run_safe "10.3 AI guvenlik uzmanligi yeni bir alan mi?" "K10.3"
run_safe "10.4 Kuantum guvenlik uzmanina talep var mi?" "K10.4"
run_safe "10.5 Kadinlar siber guvenlikte oran artiyor mu?" "K10.5"
run_safe "10.6 Hangi sertifikalar en degerli? CISSP CEH OSCP karsilastirmasi." "K10.6"
run_safe "10.7 AGI siber guvenligi nasil degistirecek?" "K10.7"
sleep 3

# YENI KONU 11: Sosyal Muhendislik
echo "=== KONU 11/15: Sosyal Muhendislik ==="
run_safe "11.1 AI destekli sosyal muhendislik: En basarili ihlaller neden guveni somuruyor?" "K11.1"
run_safe "11.2 AI ile hiper-kisisellestirilmis phishing e-postalari nasil calisir?" "K11.2"
run_safe "11.3 Vishing ve AI ses sentezi: CEO sesi nasil klonlanir?" "K11.3"
run_safe "11.4 Smishing ve QR kod saldirilari quishing nedir?" "K11.4"
run_safe "11.5 Calisan egitimi ve simule saldiri tatbikatlari nasil olmali?" "K11.5"
run_safe "11.6 En populer sosyal muhendislik senaryolari neler?" "K11.6"
sleep 3

# YENI KONU 12: SIEM SOAR XDR
echo "=== KONU 12/15: SIEM SOAR XDR ==="
run_safe "12.1 SIEM nedir ve nasil calisir?" "K12.1"
run_safe "12.2 SOAR nedir? Playbook ve otomasyon nasil isler?" "K12.2"
run_safe "12.3 XDR nedir? SIEM ve SOAR'dan farki ne?" "K12.3"
run_safe "12.4 SIEM vs SOAR vs XDR vs AI SOC Agent karsilastirmasi." "K12.4"
run_safe "12.1 SOC yapisi: Tier 1-2-3 nasil isler?" "K12.5"  # sic: K12.5
run_safe "12.6 2026'da SOC verimliligi nasil artirilir?" "K12.6"
sleep 3

# YENI KONU 13: Bulut
echo "=== KONU 13/15: Bulut Guvenligi ==="
run_safe "13.1 Paylasilan sorumluluk modeli: Saglayiciya ve musteriye ait guvenlik onlemleri." "K13.1"
run_safe "13.2 CASB nedir? Bulut hizmetlerini izleme ve veri kaybini onleme." "K13.2"
run_safe "13.3 CSPM: Yanlis yapilandirilmis bulut kaynaklari nasil tespit edilir?" "K13.3"
run_safe "13.4 CWPP: Container ve serverless guvenligi nasil saglanir?" "K13.4"
run_safe "13.5 Multi-cloud guvenlik: AWS Azure GCP'de tutarli politika." "K13.5"
run_safe "13.6 DevSecOps: CI/CD pipeline'inda guvenlik nasil entegre edilir?" "K13.6"
sleep 3

# YENI KONU 14: IoT OT
echo "=== KONU 14/15: IoT ve OT ==="
run_safe "14.1 IoT guvenligi: 30 milyar cihaz en yaygin zafiyetler neler?" "K14.1"
run_safe "14.2 OT guvenligi: SCADA ve PLC'ler neden kritik?" "K14.2"
run_safe "14.3 IT-OT yakinsamasi hangi riskleri getirir?" "K14.3"
run_safe "14.4 Akilli sebekeler ve kritik altyapi saldirilari." "K14.4"
run_safe "14.5 IoT botnetleri DDoS saldirilarinda nasil kullanilir?" "K14.5"
run_safe "14.6 5G ve edge computing guvenligi nasil saglanir?" "K14.6"
sleep 3

# YENI KONU 15: Mobil
echo "=== KONU 15/15: Mobil Guvenlik ==="
run_safe "15.1 Mobil tehditler 2026: Zararli uygulamalar ve Wi-Fi tuzaklari." "K15.1"
run_safe "15.2 MDM ve UEM ile sirket cihazlari nasil yonetilir?" "K15.2"
run_safe "15.3 EDR: Endpoint tespit ve mudahale nasil calisir?" "K15.3"
run_safe "15.4 BYOD politikalari ve riskleri neler?" "K15.4"
run_safe "15.5 Mobil uygulama guvenligi: OWASP Mobile Top 10." "K15.5"
run_safe "15.6 Uc nokta sifreleme: BitLocker FileVault mobil sifreleme." "K15.6"

BITIS=$(date '+%H:%M')
echo ""
echo "=== TAMAMLANDI $BITIS ==="
echo "15 konu yaklasik 90 soru islendi."
echo 0 > "$RETRY_FILE"
