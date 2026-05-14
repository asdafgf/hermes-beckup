#!/bin/bash
# YouTube Kanal Transcript Çekme Yöneticisi
# Kullanım:
#   1. tum_linkler.txt oluştur (her satırda bir YouTube linki: https://youtu.be/ID)
#   2. Bu script'i transcriptler/ klasörüne koy
#   3. bash cekme_yoneticisi.sh
#
# Özellikler:
#   - 25'şerli batch'ler halinde çeker (YouTube rate limit koruması)
#   - Her istek arası 2-5 sn bekleme
#   - Log dosyası tutar (cekme_log.txt)

cd "$(dirname "$0")"

YTDLP="/c/Users/eymen/temp-watch-youtube/Watch_Youtube_Skill/.venv/Scripts/yt-dlp"
BATCH="tum_linkler.txt"
LOG="cekme_log.txt"

# yt-dlp kontrol
if [ ! -f "$YTDLP" ]; then
  echo "HATA: yt-dlp bulunamadı: $YTDLP"
  echo "PATH'te ara: which yt-dlp"
  exit 1
fi

# Batch dosyası kontrol
if [ ! -f "$BATCH" ]; then
  echo "HATA: $BATCH dosyası bulunamadı!"
  echo "Önce videoların linklerini bu dosyaya yaz (her satırda https://youtu.be/ID)"
  exit 1
fi

TOPLAM=$(wc -l < "$BATCH")
echo "=== YouTube Transcript Çekimi ===" > "$LOG"
echo "Toplam: $TOPLAM video" >> "$LOG"
date >> "$LOG"

for ((start=1; start<=TOPLAM; start+=25)); do
  end=$((start + 24))
  [ $end -gt $TOPLAM ] && end=$TOPLAM
  batch_no=$(( (start - 1) / 25 + 1 ))
  total_batches=$(( (TOPLAM + 24) / 25 ))

  echo "=== Batch $batch_no/$total_batches ($start-$end) ===" >> "$LOG"

  "$YTDLP" --write-auto-sub --sub-lang en --skip-download --convert-subs srt \
    -o "%(id)s" \
    --batch-file "$BATCH" \
    --playlist-start "$start" --playlist-end "$end" \
    --sleep-requests 2 --min-sleep-interval 3 --max-sleep-interval 5 \
    2>&1 | tail -3 >> "$LOG"

  echo "Batch $batch_no OK" >> "$LOG"
  echo "Bekleniyor..." >> "$LOG"
  sleep 3
done

echo "" >> "$LOG"
echo "TAMAM — $(ls *.srt 2>/dev/null | wc -l) transcript çekildi" >> "$LOG"
date >> "$LOG"
