# qwen2.5-coder:7b Gece Öğrenme Oturumu — 13 Mayıs 2026

## Setup
- **Model:** qwen2.5-coder:7b-instruct-q4_K_M (4.7 GB, Ollama)
- **Host:** Windows 11, Hermes Agent (deepseek-chat)
- **Zaman:** 23:14 → 08:00 (~8.5 saat)
- **Kullanıcı:** Eymen

## Mimari (İkili Sistem)

### 1. Background PTY Süreci
- **Session:** `proc_4ab5b60db4cd` (PID 21884)
- **Script:** `~/.hermes/scripts/qwen_gece_oturumu.sh`
- **Aralık:** Her konu arası 45 dk (sleep 2700)
- **Mod:** PTY canlı (kullanıcı terminalde izleyebilir)
- **Notif:** `notify_on_complete=true`

### 2. Cronjob Yedek Tetikleme
- **Job ID:** `669f1fd8ddae`
- **Schedule:** `0 0,1,2,3,4,5,6,7 * * *` (saat başı)
- **Repeat:** 8 kez
- **Deliver:** origin (bu sohbete)
- **Amac:** Background PTY bir konuda takılırsa/kırılırsa cronjob devralır

## Konu Listesi (7 konu)

1. ✅ Yapay zeka ve yazılım geliştirmede son trendler (2025-2026) — **canlı çalıştı**
2. ✅ Küçük dil modellerinin (SLM) büyük modellere karşı avantajları — **canlı çalıştı**
3. ✅ Kod üretiminde AI asistanların geleceği — **canlı çalıştı**
4. ⏳ Açık kaynak vs kapalı kaynak modellerin karşılaştırması
5. ⏳ Edge computing ve local AI'nın yükselişi
6. ⏳ Yazılım mühendisliğinde AI'ın rolü - yardımcı mı yoksa ikame mi?
7. ⏳ Kendi yeteneklerin ve sınırlamaların hakkında meta-bir değerlendirme

## Script İçeriği (özet)

```bash
KONULAR=(
  "3. Kod üretiminde AI asistanların geleceği. ..."
  "4. Açık kaynak vs kapalı kaynak modellerin karşılaştırması. ..."
  "5. Edge computing ve local AI'nın yükselişi. ..."
  "6. Yazılım mühendisliğinde AI'ın rolü ..."
  "7. Kendi yeteneklerin ve sınırlamaların hakkında meta-değerlendirme ..."
)

for i in "${!KONULAR[@]}"; do
  echo "${KONULAR[$i]}" | ollama run qwen2.5-coder:7b 2>&1
  if [ $i -lt $((${#KONULAR[@]} - 1)) ]; then sleep 2700; fi
done
```

## Gözlemler

- qwen2.5-coder:7b PTY'de 60sn'den kısa sürede yanıt veriyor (7B model, hızlı)
- Türkçe prompt'u anlıyor ama cevaplar İngilizce ağırlıklı
- `[DEVAM]` işareti ile konu bittiğini belirtiyor — ama her turda aynı konuyu tekrar edebiliyor (loop riski)
- 7B model derin analizde 4-5 paragraftan sonra tekrara düşüyor
- Cronjob zaten hazır olduğu için hızlı kurulum (yedek cronjob'lar mevcuttu)
