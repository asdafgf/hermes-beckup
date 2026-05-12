"""
docker_kurulum_final.py
Windows 11'de Docker Desktop sessiz kurulumu.
Admin gerektirir — Yönetici PowerShell'de çalıştırılmalı.

Yapısı:
1/5 Admin kontrolü (değilse hata + çıkış)
2/5 WSL2 güncelle + Ubuntu başlat (~2 dk)
3/5 Installer bul/indir + sessiz kurulum (~10-12 dk)
4/5 Docker Desktop'ı başlat
5/5 docker ps hazır olana kadar bekle (~1-3 dk)

Kullanım (Yönetici PowerShell):
  cd C:\Users\eymen\kiralog
  python docker_kurulum_final.py
"""

import ctypes, os, subprocess, sys, time, urllib.request
from pathlib import Path

INSTALLER_PATH = Path(r"C:\Users\eymen\AppData\Local\Temp\DockerDesktopInstaller.exe")
INSTALLER_URL  = "https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe"
DOCKER_EXE     = Path(r"C:\Program Files\Docker\Docker\Docker Desktop.exe")
INSTALL_TIMEOUT  = 720
DOCKER_READY_MAX = 180
POLL_INTERVAL    = 10

def log(tag, msg): print(f"[{tag}] {msg}", flush=True)
def info(m): log("INFO", m)
def ok(m):   log("OK", m)
def err(m):  log("HATA", m)
def sep(n, total, t):
    print(flush=True)
    print(f"[{n}/{total}] {t}", flush=True)
    print("-" * 50, flush=True)

def check_admin():
    try: return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except: return False

def step_1_admin():
    sep(1, 5, "Admin Yetkisi Kontrolu")
    if check_admin():
        ok("Admin yetkisi mevcut.")
        return
    err("ADMIN GEREKIR. Yonetici PowerShell'de calistirin:")
    err(f"  python \"{os.path.abspath(sys.argv[0])}\"")
    sys.exit(1)

def _run(cmd, timeout=120):
    return subprocess.run(cmd, timeout=timeout, capture_output=True, text=True)

def step_2_wsl2():
    sep(2, 5, "WSL2 Hazirligi")
    info("WSL guncelleniyor...")
    try:
        r = _run(["wsl", "--update"], timeout=120)
        ok("WSL guncellendi.") if r.returncode == 0 else err(f"wsl --update uyari: {r.stderr.strip()[:200]}")
    except: err("wsl --update hatasi, devam.")
    info("Ubuntu baslatiliyor...")
    try:
        r = _run(["wsl", "-d", "Ubuntu", "echo", "ok"], timeout=60)
        ok("Ubuntu aktif.") if r.returncode == 0 else err(f"Ubuntu uyari: {r.stderr.strip()[:200]}")
    except: err("Ubuntu baslatma hatasi, devam.")

class _Progress:
    def __init__(self): self._last = -1
    def __call__(self, blocks, bsize, total):
        if total <= 0: return
        pct = min(int(blocks * bsize * 100 / total), 100)
        if pct - self._last >= 5: info(f"  {pct}% ({blocks*bsize/1048576:.0f}/{total/1048576:.0f} MB)"); self._last = pct

GOOD = {0: "Basarili", 1638: "Zaten kurulu", 3010: "Yeniden baslat gerekebilir"}

def step_3_install():
    sep(3, 5, "Docker Desktop Sessiz Kurulum")
    if INSTALLER_PATH.exists() and INSTALLER_PATH.stat().st_size > 400*1048576:
        ok(f"Mevcut installer: {INSTALLER_PATH.stat().st_size/1048576:.0f} MB")
    else:
        info("Indiriliyor...")
        INSTALLER_PATH.parent.mkdir(parents=True, exist_ok=True)
        try: urllib.request.urlretrieve(INSTALLER_URL, INSTALLER_PATH, reporthook=_Progress())
        except Exception as e: err(f"Indirme hatasi: {e}"); return False
    info(f"Kurulum basliyor (max {INSTALL_TIMEOUT//60} dk)...")
    try:
        r = subprocess.run([str(INSTALLER_PATH), "install", "--quiet"], timeout=INSTALL_TIMEOUT, capture_output=True, text=True)
    except subprocess.TimeoutExpired: err("Zaman asimi."); return False
    except Exception as e: err(f"Hata: {e}"); return False
    if r.returncode in GOOD: ok(f"Exit {r.returncode}: {GOOD[r.returncode]}"); return True
    err(f"Exit code: {r.returncode}"); return False

def step_4_start():
    sep(4, 5, "Docker Desktop Baslatma")
    for c in [DOCKER_EXE, Path(os.environ.get("PROGRAMFILES", "C:\\Program Files")) / "Docker" / "Docker" / "Docker Desktop.exe"]:
        if c.exists(): target = c; break
    else: err("Docker Desktop.exe bulunamadi."); return False
    try:
        subprocess.Popen([str(target)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
        ok("Baslatildi."); return True
    except Exception as e: err(f"Hata: {e}"); return False

def _docker_ps():
    try:
        r = subprocess.run(["docker", "ps"], timeout=15, capture_output=True, text=True)
        return r.returncode == 0, r.stderr.strip()[:120] or f"exit {r.returncode}"
    except FileNotFoundError: return False, "docker PATH'te yok"
    except: return False, "hata"

def step_5_wait():
    sep(5, 5, "Engine Bekleme")
    time.sleep(20); elapsed, attempt = 20, 0
    while elapsed < DOCKER_READY_MAX:
        attempt += 1; ready, msg = _docker_ps()
        if ready: ok(f"docker ps basarili (#{attempt}, {elapsed}s)"); return True
        info(f"  #{attempt} ({elapsed}s): {msg}")
        time.sleep(POLL_INTERVAL); elapsed += POLL_INTERVAL
    err(f"Engine {DOCKER_READY_MAX}s icinde hazir olmadi."); return False

def main():
    print("=" * 50); print("  Docker Desktop - Kurulum"); print("=" * 50)
    results = {}
    step_1_admin(); results["admin"] = True
    step_2_wsl2(); results["wsl2"] = True
    results["install"] = step_3_install()
    results["start"] = step_4_start()
    results["engine"] = step_5_wait() if results["start"] else (err("Baslatma yok, bekleme atlandi."), False)[1]
    print(); print("=" * 50); print("  OZET"); print("=" * 50)
    for k, l in [("admin","Admin"),("wsl2","WSL2"),("install","Kurulum"),("start","Baslatma"),("engine","Engine")]:
        print(f"  [{'OK' if results.get(k) else 'HATA'}] {l}")
    print("=" * 50)
    if results.get("engine"): ok("Hazir. Test: docker run --rm hello-world"); sys.exit(0)
    else: err("Bazi adimlar basarisiz."); sys.exit(1)

if __name__ == "__main__": main()
