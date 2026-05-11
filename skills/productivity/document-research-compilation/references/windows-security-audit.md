# Windows Güvenlik Taraması — Hızlı Referans

Kullanıcı "bilgisayarımda hangi uygulamalar çalışıyor, güvenlik ihlali var mı" gibi bir soru sorduğunda kullanılacak adımlar.

## 1. Çalışan İşlemleri Listele

```bash
# Tüm işlemler (sayısal sıralı)
tasklist 2>/dev/null | tail -n +4 | awk '{print $1}' | sort | uniq -c | sort -rn

# Tek bir PID'in hangi uygulamaya ait olduğunu bul
tasklist /FI "PID eq <PID>" 2>/dev/null | tail -n +4 | awk '{print $1}'
```

## 2. Ağ Bağlantılarını Kontrol Et

```bash
# Dışarıya açık ESTABLISHED bağlantılar (127.0.0.1/localhost hariç)
netstat -ano 2>/dev/null | grep ESTABLISHED | grep -v "127.0.0.1" | grep -v "::1"

# Dinlemedeki portlar (hangi servisler dışarıya açık)
netstat -ano 2>/dev/null | grep LISTEN
```

## 3. Bağlantıları Uygulamalarla Eşleştir

netstat çıktısındaki PID'leri `tasklist` ile eşle:

```bash
netstat -ano 2>/dev/null | grep ESTABLISHED | grep -v "127.0.0.1" | while read line; do
    pid=$(echo $line | awk '{print $5}')
    app=$(tasklist /FI "PID eq $pid" 2>/dev/null | tail -n +4 | awk '{print $1}')
    echo "$line   [$app]"
done
```

## 4. Antivirüs Durumunu Kontrol Et

```bash
# Windows Defender durumu
powershell.exe -Command "Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled, LastQuickScanTime, LastFullScanTime"

# Son tespit edilen tehditler
powershell.exe -Command "Get-MpThreatDetection | Select-Object -First 5 Resources,ThreatName,DetectionTime"
```

## 5. Sistem Kaynakları

```bash
# CPU yükü
echo "CPU: $(powershell.exe -Command "Get-CimInstance Win32_Processor | Select-Object -Exp LoadPercentage" 2>/dev/null)%"

# Boş RAM (MB)
echo "RAM: $(powershell.exe -Command "Get-CimInstance Win32_OperatingSystem | Select-Object @{Name='Free';E={[math]::Round(\$_.FreePhysicalMemory/1024,1)}}" 2>/dev/null) MB boş"
```

## 6. Yorumlama Kılavuzu

| Bulgu | Anlamı | Risk |
|-------|--------|------|
| `msedge.exe × 26` | Çok sayıda Edge sekmeleri | RAM tüketimi, güvenlik sorunu değil |
| `steam.exe` + `steamwebhelper.exe` | Steam oyun platformu açık | Normal |
| `TeamViewer_Service.exe` | Uzaktan erişim yazılımı | Kullanıcı izin verdiyse normal |
| `Overwolf.exe` | Oyun içi overlay | Normal |
| `python.exe` / `python3.12.exe` | Python yorumlayıcı | Normal (Hermes, Claude vs.) |
| `ollama.exe` | Yerel AI model sunucusu | Normal |
| `WhatsApp.Root.exe` | WhatsApp masaüstü | Normal |
| `AdobeCollabSync.exe` | Adobe bulut senkronizasyonu | Normal |
| `bash.exe × 6` | Git Bash açık | Normal |
| `svchost.exe → 98.66.133.185:443` | Windows Update | ✅ Güvenli |
| `MpDefenderCoreService.exe → 52.x:443` | Windows Defender güncelleme | ✅ Güvenli |
| `python3.12.exe → 149.154.166.110:443` | Telegram API (Hermes) | ✅ Güvenli |
| Bilinmeyen IP'ye bağlı exe | Şüpheli | ⚠️ Araştırılmalı |
| Defender devre dışı | Antivirüs kapalı | 🔴 Acil |

## 7. Hızlı Özet Formatı

```markdown
## 🖥️ Bilgisayar Durumu

**Sistem:** Windows 11
**CPU:** %X (düşük/normal/yüksek)
**RAM:** X GB boş
**Antivirüs:** Windows Defender Aktif/Devre Dışı ✅/❌

## 📋 Çalışan Uygulamalar
| Uygulama | Ne İş Yapar? |
|----------|-------------|
| msedge.exe (26) | Edge tarayıcı |

## 🔒 Güvenlik: ✅ GÜVENLİ / ⚠️ UYARI / 🔴 RİSKLİ

- ✅ Tüm bağlantılar bilinen servislere
- ✅ Antivirüs aktif
- ⚠️ [varsa uyarılar]
```
