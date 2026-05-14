# Siber Güvenlik Gece Oturumu — 14 Mayıs 2026

## Özet
- 15 konu, ~90 soru
- Model: gemma4:latest
- Çalışma süresi: 6+ saat
- Skill'ler: 15 adet security/ kategorisinde

## Script Anatomisi
```bash
#!/bin/bash
MODEL="gemma4:latest"
MAX_RETRY=3
RETRY_FILE="/tmp/siber_retry_count.txt"

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
```

## Çıkarılan Dersler

1. **Parantez kullanma** — yorum satırlarında bile syntax hatası
2. **Background PTY** — uzun süreli işlemler için en iyi yöntem
3. **Cronjob + PTY** — dual mekanizma en güvenilir
4. **`sed` ile onarım tehlikeli** — fonksiyon adlarını da kırar
5. **`$[komut]` yerine `$(komut)`** — eski syntax çalışmaz

## 15 Konu Başlığı
1. Agentic AI ve Otonom Saldırılar
2. Deepfake ve Kimlik Aldatmacası
3. Zero Trust Mimarisi
4. Tedarik Zinciri Güvenliği
5. Regülasyon ve Uyum
6. Ransomware
7. API Güvenliği
8. Kuantum Güvenliği
9. CTEM
10. Kariyer
11. Sosyal Mühendislik
12. SIEM/SOAR/XDR
13. Bulut Güvenliği
14. IoT/OT Güvenliği
15. Mobil Güvenlik
