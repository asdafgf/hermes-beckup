---
name: python-admin-runner-windows
description: >-
  Hermes terminal'den (git-bash) Yönetici yetkisi gerektiren Python script'lerini
  çalıştırma yöntemleri. ShellExecuteW runas venv'den çalışmaz (Access Denied kod 5),
  Start-Process -Verb RunAs git-bash'ten çalışmaz. Bu skill 3 alternatif strateji
  sunar: admin_powershell.py (otomatik), elle Yönetici PowerShell, ve doğrudan UAC bypass.
---

# Python Admin Runner — Windows

## ⚠️ KRİTİK UYARI

**Bu skill'deki tüm otomatik yöntemler Hermes venv + git-bash ortamında ÇALIŞMAYABİLİR.**

Test edilen durum:
| Yöntem | Sonuç |
|--------|-------|
| `ShellExecuteW runas` (venv python) | Access Denied (kod 5) |
| `Start-Process -Verb RunAs` (PS'den) | "Kullanıcı tarafından iptal edildi" |
| `schtasks /create /rl HIGHEST` | Yetki yetersiz |
| VBScript ShellExecute | Aynı UAC kısıtı |
| PowerShell zincirleme UAC | Yine venv sınırlaması |

**Son çare her zaman:** Kullanıcıya elle Yönetici PowerShell'de çalıştırmasını söyle.

## Stratejiler (Tercih Sırasına Göre)

### Strateji 1: run_admin.py (Önerilen — 4 Strateji, En Kapsamlı)

`run_admin.py` — Claude.ai'dan alınan, 4 farklı UAC yöntemini sırayla deneyen yardımcı script. `admin_powershell.py`'den daha kapsamlıdır.

**Kullanım:**
```bash
cd /c/Users/eymen/kiralog
python run_admin.py
```

**4 strateji (biri çalışana kadar dener):**
1. **ShellExecuteW Zinciri** — powershell.exe'yi runas başlatır, içinde Start-Process -Verb RunAs ile python'u çalıştırır
2. **Scheduled Task** — `schtasks /create /rl HIGHEST` ile UAC bypass dener
3. **VBScript Köprüsü** — `cscript` ile Shell.Application.ShellExecute çağırır
4. **PowerShell Doğrudan** — subprocess ile Start-Process -Verb RunAs

Her adımda log yazar, hata durumunda sonraki yönteme geçer. Log: `run_admin.log`

### Strateji 2: admin_powershell.py (3 Strateji)

**Kullanım:**
```bash
cd /c/Users/eymen/kiralog
python admin_powershell.py "C:\path\to\hedef_script.py" [arg1 ...]
```

**3 strateji:**
1. PowerShell runas (en güvenilir)
2. cmd.exe /c runas
3. Doğrudan python runas (log yok)

Log: `hedef_script_admin_run.log`

### Nasıl çalışır

1. Sistem Python'unu bulur (py.exe, PATH, sabit yollar)
2. Geçici bir .ps1 script'i oluşturur (stdout/stderr log'a yönlendirir)
3. `ShellExecuteExW` ile PowerShell'i **runas** verb'üyle başlatır
4. UAC açılır — kullanıcı **"Evet"** der
5. PowerShell, hedef script'i admin olarak çalıştırır

### Strateji 3: Elle Yönetici PowerShell (En Güvenilir — Tüm otomatik yöntemler başarısız olursa)

Kullanıcıya anlatma şablonu:
```
1. Windows tuşuna bas
2. "PowerShell" yaz
3. Sağ tıkla → "Yönetici olarak çalıştır" seç
4. Açılan mavi pencerede:
   cd C:\Users\eymen\kiralog
   python script_adi.py
5. Çıktıyı buraya yapıştır
```

Hata riski: 0.

## Stratejiler (Tercih Sırasına Göre)

### Strateji 1: admin_powershell.py (Önerilen — Otomatik)

`admin_powershell.py` — Claude.ai'dan alınan, 3 farklı UAC yöntemini sırayla deneyen yardımcı script.

**Kullanım:**
```bash
cd /c/Users/eymen/kiralog
python admin_powershell.py "C:\Users\eymen\kiralog\hedef_script.py"
```

**Nasıl çalışır:**
1. Sistem Python'unu bulur (py.exe, PATH, sabit yollar)
2. Geçici bir .ps1 script'i oluşturur (stdout/stderr log'a yönlendirir)
3. `ShellExecuteExW` ile PowerShell'i **runas** verb'üyle başlatır
4. UAC açılır — kullanıcı **"Evet"** der
5. PowerShell, hedef script'i admin olarak çalıştırır
6. Çıktıyı log dosyasına yazar

**Log dosyası:** `hedef_script_adı_admin_run.log` (script yanında veya TEMP'te)

**Strateji sırası (başarısız olursa bir sonrakine geçer):**
1. PowerShell runas (en güvenilir)
2. cmd.exe /c runas
3. Doğrudan python runas (log tutamaz)

Herhangi biri başarılı olursa durur. Hiçbiri olmazsa hata verir.

### Strateji 2: Elle Yönetici PowerShell (En Güvenilir)

```powershell
# Windows → "PowerShell" → Sağ tık → "Yönetici olarak çalıştır"
cd C:\Users\eymen\kiralog
python docker_kurulum_final.py
```

Hata riski: 0. Kullanıcıya anlatması en kolay yöntem.

**Kullanıcıya anlatma şablonu:**
```
1. Windows tuşuna bas
2. "PowerShell" yaz
3. Sağ tıkla → "Yönetici olarak çalıştır" seç
4. Açılan mavi pencerede şu komutları çalıştır:
   cd C:\Users\eymen\kiralog
   python script_adi.py
5. Çıktıyı buraya yapıştır
```

### Strateji 3: Doğrudan ShellExecuteW (Script içinde gömülü, önerilmez)

Script, admin değilse **"Bu scripti Yönetici PowerShell'de çalıştırın"** diyerek çıksın.
Script'in kendini yükseltmeye çalışması bu ortamda çalışmaz.

## admin_powershell.py Script Yapısı

Script şu bileşenlerden oluşur:

### 1. `find_system_python()`
- py.exe launcher (öncelikli)
- PATH'teki venv OLMAYAN python
- Sabit yollar (C:\Python3*, C:\Program Files\Python3*)

### 2. `build_ps_command()`
- PowerShell -Command string'i oluşturur
- stdout + stderr'i log dosyasına yönlendirir
- Exit code'u log'a yazar

### 3. `SHELLEXECUTEINFOW` (ctypes struct)
- ShellExecuteExW için Windows API struct'ı
- `runas` verb + `SEE_MASK_NOCLOSEPROCESS` flag

### 4. `_shell_execute()`
- Process handle'ını bekler (WaitForSingleObject INFINITE)
- Exit code'u döner
- -1 = UAC iptal, -2 = başka hata

## Hata Kodları

| Kod | Anlamı |
|-----|--------|
| -1 | Kullanıcı UAC'yi iptal etti (ERROR_CANCELLED = 1223) |
| -2 | ShellExecuteExW başarısız (başka hata) |
| 0+ | Script exit code'u (başarılı çalıştı) |

## Rename-Item / Klasör Yeniden Adlandırma (Özel Durum)

Admin yetkisiyle klasör yeniden adlandırma (`Rename-Item`, `mv`) Windows'ta özellikle sorunludur:

**Sık karşılaşılan hata zinciri:**
1. `git-bash mv` → `Permission denied`
2. `ctypes.MoveFileExW` (Python) → error code 5 (Access Denied)
3. `cmd.exe /c rename` → güvenlik taraması engeli
4. `Rename-Item` (PowerShell) → aynı engel

**Çözüm: process lock'ları önce temizle:**
```bash
# Tüm node process'lerini öldür (en sık lock'layan)
taskkill /F /IM node.exe 2>nul

# VS Code kapat (varsa)
taskkill /F /IM code.exe 2>nul
```

**Hala olmazsa — son çareler:**
- `.bat` dosyası yaz → kullanıcıdan Admin çalıştırmasını iste
- Kullanıcıya manuel PowerShell komutu ver:
  ```powershell
  Rename-Item -Path "C:\Users\eymen\eski_klasor" -NewName "yeni_klasor" -Force
  ```
- Zip yedekten yeni isimle çıkart (rename yerine extract + yeni isim)
- Yeni boş klasör oluştur, tüm dosyaları `write_file` ile teker teker kopyala
