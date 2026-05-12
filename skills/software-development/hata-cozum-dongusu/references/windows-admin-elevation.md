# Windows Admin Elevation (UAC) Teknikleri

## 1. ShellExecuteW ile Kendini Yükseltme (En Basit)

```python
import ctypes, sys, os

def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False

def relaunch_as_admin() -> None:
    script = os.path.abspath(sys.argv[0])
    params = " ".join(f'"{a}"' for a in sys.argv[1:])
    ret = ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{script}" {params}', None, 1
    )
    if ret <= 32:
        print("[HATA] UAC elevation basarisiz")
        sys.exit(1)
    sys.exit(0)  # eski process kapanir

def ensure_admin():
    if not is_admin():
        relaunch_as_admin()  # donmez, yeni process acilir

if __name__ == "__main__":
    ensure_admin()
    # admin kodlari buraya
```

## 2. Background Process + Admin Uyarısı

UAC gereken script'leri **background ile başlatma** çünkü UAC penceresi terminal session'ına bağlanamaz. Bunun yerine:
- Script'i direkt `terminal` aracıyla foreground çalıştır
- Veya PowerShell'i admin olarak açıp manuel çalıştırmasını söyle

## 3. Hata Kodları

- `[WinError 740]` → Yönetici yetkisi gerekli
- Installer exit code 1638 → zaten kurulu
- Installer exit code 3010 → yeniden başlatma gerekiyor (başarılı say)

## 4. Docker Desktop Sessiz Kurulum İçin Tipik Döngü

```
1. Docker CLI scoop'tan yüklü mü? → docker --version
2. Docker Desktop yüklü mü? → C:\Program Files\Docker\Docker\Docker Desktop.exe
3. Engine çalışıyor mu? → docker ps
4. İndir: https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe
5. Kur: installer.exe install --quiet (admin gerek)
6. Başlat + docker ps hazır olana kadar bekle
```
