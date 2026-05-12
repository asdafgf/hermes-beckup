---
name: wsl-allow-once-cozumu
description: >-
  WSL komutlarında çıkan "Allow Once" onay penceresini kapatmak için
  Windows Defender Firewall veya Güvenlik ayarlarından WSL'ye kalıcı izin verir.
---

# WSL Allow Once Çözümü

## Ne Zaman Kullanılır
- WSL komutları çalıştırılırken "Allow Once" (İzin Ver) penceresi çıkıyor
- Her WSL çağrısında onay gerekiyor
- `wsl -d Ubuntu -e bash -c "..."` komutları kesintisiz çalışmıyor

## Allow Once Seçeneği Geldiğinde Ne Yapmalıyım

Allow Once seçeneği, WSL'nin Windows güvenlik duvarından geçişine izin vermek için Windows tarafından sorulan bir onaydır.

### Seçenekler ve Karar

| Seçenek | Etkisi | Ne Zaman Seçilmeli |
|---------|--------|-------------------|
| **İzin Ver (Allow)** | Sadece o anki işlem | Geçici çözüm |
| **Allow + Private networks** | Ev/iş ağında her sefer | ✅ **EN İYİSİ — kullanıcıya sor: "Private networks seçili, Allow'a tıklayın"** |
| **Allow + Public networks** | Her ağda izin verir | Genel WiFi'lerde |
| **İptal** | Hiç izin vermez | ❌ Kullanma |

### Kullanıcıya Ne Söylenir
**"Allow Once diye bir pencere açıldı. 'Private networks' seçili olduğundan emin olun ve 'İzin Ver'e tıklayın."**

Eğer kullanıcı "sorma halledin / siz yapın" derse → **kalıcı çözüm uygulanır** (aşağıdaki firewall kuralı).

### Kalıcı Çözüm (Kullanıcı "sorma" derse)
Allow Once'i tamamen kaldırmak için WSL'ye Windows Firewall'da kalıcı izin verilir.

## Çözüm: Windows Güvenlik Ayarları

### 1. Windows Güvenlik Duvarı (Firewall)
1. **Windows + R** → `wf.msc` yaz → Enter
2. Sol panelden **"Gelen Kuralları"** seç
3. Sağ panelden **"Yeni Kural..."** tıkla
4. **"Program"** seç → İleri
5. Program yolu: `C:\Windows\System32\wsl.exe`
6. **"Bağlantıya izin ver"** seç → İleri
7. Tüm profiller seçili (Domain, Özel, Genel) → İleri
8. Ad: "WSL Allow All" → Bitir

Aynı adımları **"Giden Kuralları"** için de tekrarla.

### 2. Alternatif: PowerShell ile Hızlı Çözüm
```powershell
# WSL için gelen ve giden tüm trafiğe izin ver
New-NetFirewallRule -DisplayName "WSL Allow All In" -Direction Inbound -Program "C:\Windows\System32\wsl.exe" -Action Allow -Profile Any
New-NetFirewallRule -DisplayName "WSL Allow All Out" -Direction Outbound -Program "C:\Windows\System32\wsl.exe" -Action Allow -Profile Any
```

### 3. WPFD Python ile Otomatik Çözüm
Eğer kullanıcı hiç uğraşmak istemezse, bir Python script'i yazılır:
- `subprocess.run` ile `netsh advfirewall firewall add rule` komutunu çalıştırır
- Veya bir VBScript ile Shell.Application.ShellExecute kullanır

## Doğrulama
```bash
wsl -d Ubuntu -e bash -c "echo ALLOW_ONCE_COZULDU"
```
Onay penceresi çıkmamalı.

## Bu Skill Ne Zaman Devreye Girer
Hermes terminal'den WSL komutları çalıştırılırken "Allow Once" onayı alınırsa hemen bu skill yüklenir.

## Kullanıcı Tercihi (Öğrenilmiş)
Bu kullanıcı için:
- "Allow Once" sorma, kalıcı çözüm uygula
- Kullanıcı onay istemiyor, işlem otomatik yapılsın istiyor
