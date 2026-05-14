#!/bin/bash
# RootOfTheNull Transcript Çekme Yöneticisi
# 412 öncelikli videoyu 25'erli batch'ler halinde çeker
# YouTube rate limit korumalı

cd /c/Users/eymen/Desktop/rootofthenull_arsiv/transcriptler
YTDLP="/c/Users/eymen/temp-watch-youtube/Watch_Youtube_Skill/.venv/Scripts/yt-dlp"
BATCH="batch_oncelikli.txt"
TOPLAM=412
BATCH_SIZE=25
LOG="cekme_log.txt"

echo "=== TRANSCRIPT ÇEKME BAŞLADI $(date) ===" > "$LOG"
echo "Toplam: $TOPLAM video, $BATCH_SIZE'şer batch" >> "$LOG"

for ((start=1; start<=TOPLAM; start+=BATCH_SIZE)); do
  end=$((start + BATCH_SIZE - 1))
  [ $end -gt $TOPLAM ] && end=$TOPLAM
  
  batch_no=$(( (start - 1) / BATCH_SIZE + 1 ))
  total_batches=$(( (TOPLAM + BATCH_SIZE - 1) / BATCH_SIZE ))
  
  echo "=== Batch $batch_no/$total_batches ($start-$end) ==="
  
  "$YTDLP" --write-auto-sub --sub-lang en --skip-download --convert-subs srt \
    -o "%(id)s" \
    --batch-file "$BATCH" \
    --playlist-start "$start" --playlist-end "$end" \
    --sleep-requests 2 \
    --min-sleep-interval 3 \
    --max-sleep-interval 5 \
    2>&1 | tee -a "$LOG" | tail -5
  
  echo "Batch $batch_no/$total_batches tamam $(date)" >> "$LOG"
  sleep 5
done

echo "=== TAMAM $(date) ===" >> "$LOG"
echo "Çekilen dosyalar: $(ls *.srt 2>/dev/null | wc -l)"
echo "Toplam boyut: $(du -sh *.srt 2>/dev/null | cut -f1)"
