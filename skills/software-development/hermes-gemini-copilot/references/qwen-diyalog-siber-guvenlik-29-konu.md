# Hermes ↔ Qwen2.5-coder Karşılıklı Diyalog Eğitim Protokolü
## 29 Konulu Siber Güvenlik Oturumu — 13 Mayıs 2026

Bu doküman, Hermes (ana agent) ile qwen2.5-coder:7b (Ollama yerel model) arasında
29 konuluk karşılıklı eğitim oturumunun protokolünü belgeler.

## Mimari

```
HERMES (ben) ↔ QWEN2.5-CODER (Ollama) → Skill kaydı → Telegram raporu
```

Her konu için 2 turlu diyalog:
1. **Hermes Açılış:** Konuyu açar, bağlam verir, spesifik soru sorar
2. **Qwen Yanıt 1:** Detaylı cevap üretir
3. **Hermes Derinleştirme:** Cevabı analiz eder, ek soru sorar
4. **Qwen Yanıt 2:** Derinlemesine cevap verir

## Konu Havuzu (6 Kategori, 29 Konu)

### Temel (SIB-001~002)
- SIB-001: CIA Triad, STRIDE, DREAD — güvenlik temel kavramları
- SIB-002: Nmap port tarama, Wireshark sniffing, ARP spoofing, MITM

### Python (PYT-001~006)
- PYT-001: socket port tarama, Scapy paket oluşturma
- PYT-002: scapy sniff(), BPF filtreleri, HTTP/DNS yakalama
- PYT-003: requests + BeautifulSoup, XSS/SQLi tespiti, OWASP ZAP API
- PYT-004: threading brute force, credential stuffing, proxy rotasyonu
- PYT-005: cryptography (Fernet, AES, RSA), hashlib, dijital imzalar
- PYT-006: pandas log analizi, regex anomali, ELK entegrasyonu

### WiFi (WIF-001~005)
- WIF-001: WPA2/3 4-way handshake, PMKID, KRACK, evil twin
- WIF-002: ARP tablosu, MAC OUI fingerprint, Bettercap net.probe
- WIF-003: Rogue AP tespiti, RSSI takibi, DHCP log analizi
- WIF-004: SSLstrip, HSTS bypass, session hijacking
- WIF-005: airodump-ng kanal tarama, 2.4/5/6GHz karşılaştırması

### Android (AND-001~005)
- AND-001: ADB, bootloader, Stagefright, BlueBorne, Dirty COW
- AND-002: GPS/IMEI/Cell ID/WiFi triangulation
- AND-003: scrcpy, VNC, Accessibility Service keylogging
- AND-004: adb TCP/IP, Termux SSH, MDM
- AND-005: appops, NetGuard, AFWall+, izin yönetimi

### Saldırı (SAL-001~005)
- SAL-001: Spear phishing, SPF/DKIM/DMARC, SET toolkit
- SAL-002: netcat reverse shell, msfvenom, persistence
- SAL-003: SQLi, NoSQLi, command injection
- SAL-004: Stack BOF, ASLR/DEP bypass, ROP
- SAL-005: SYN/UDP/HTTP flood, Slowloris, WAF

### İleri (ILR-001~006)
- ILR-001: Statik/dinamik malware analiz, YARA
- ILR-002: dd/FTK Imager, volatility, chain of custody
- ILR-003: OpenVAS, Metasploit, CVSS, PTES metodolojisi
- ILR-004: iptables, Snort/Suricata, Zeek, SIEM
- ILR-005: Zero-day, bug bounty, APT, MISP/OpenCTI
- ILR-006: Bluetooth BlueBorne, IoT MQTT/CoAP, Mirai

## Zorunlu Mekanizmalar

### 1. Lock File
```bash
if [ -f "$LOCK" ]; then
  lock_age=$(($(date +%s) - $(stat -c %Y "$LOCK")))
  if [ $lock_age -lt 600 ]; then exit 1; fi
fi
echo $$ > "$LOCK"
```

### 2. Registry (Tekrar Kontrolü)
```bash
if grep -q "^$KONU_ID|" "$REGISTRY"; then
  echo "⏭️ TEKRAR — atlandı"
fi
echo "$KONU_ID|$SKILL_NAME|$zaman" >> "$REGISTRY"
```

### 3. 2-dk Timeout + Retry
```bash
qwen_sor() {
  local prompt="$1"
  local max_wait=120
  
  echo "$prompt" | ollama run qwen2.5-coder:7b &
  local pid=$!
  
  # 2 dk bekle, gelmezse kill + retry
  # ...
}
```

### 4. Saat Kontrolü
```bash
saat=$((10#$(date '+%H')))
if [ "$saat" -ge 8 ] && [ "$saat" -lt 23 ]; then
  break  # 08:00-22:59 arası dur
fi
# 23:00-07:59 arası çalış
```

### 5. Progress Yüzdesi
```bash
YUZDE=$((ISLENEN * 100 / TOTAL))
echo "İlerleme: $ISLENEN/$TOTAL (%$YUZDE)"
```

## Skill Çıktı Yapısı

```
~/.hermes/skills/security/<skill-adi>/
├── SKILL.md
│   ├── name, description, version
│   ├── metadata: source=qwen2.5-coder:7b
│   ├── Diyalog özeti (özet+uyarı)
│   └── ⚠️ EĞİTİM AMAÇLIDIR uyarısı
│
└── references/
    └── diyalog.txt
        ├── HERMES AÇILIŞ → [tam metin]
        ├── QWEN YANIT 1 → [tam metin]
        ├── HERMES DERİNLEŞTİRME → [tam metin]
        └── QWEN YANIT 2 → [tam metin]
```

## Sabah Raporu (08:10 Telegram)

Cronjob `qwen-diyalog-sabah-raporu` saat 08:10'da tetiklenir:
1. `.qwen_report.final` dosyasını okur
2. Skill listesini tarrer
3. Telegram formatında özet gönderir:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌙 HERMES ↔ QWEN KARŞILIKLI DİYALOG
──── EĞİTİM RAPORU ────
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ [tarih] 📊 Toplam: X konu

[id] [skill-adi] → [başlık]
...
```

## Bilinen Hatalar ve Çözümleri

| Hata | Belirti | Çözüm |
|------|---------|-------|
| Lock kilitli | "Başka oturum çalışıyor" | `rm -f .qwen_lock` |
| Sed pipe hatası | `unknown option to s` | `grep -v + mv` kullan, sed değil |
| grep boş integer | `integer expression expected` | `${VAR:-0}` varsayılan |
| mkdir eksik | `No such file or directory` | `mkdir -p path/references` |
| Saat string karşılaştırma | 23:00'de durur | `$((10#h))` integer çevrimi |
| PTY yarıda kesilme | `[Command interrupted]` | Normal modda retry veya background |
