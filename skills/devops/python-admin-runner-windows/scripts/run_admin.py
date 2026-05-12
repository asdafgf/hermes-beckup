"""
run_admin.py — Zincirleme UAC Yükseltme Scripti
Strateji: 4 farklı yöntem sırayla denenir, ilk başarılı olan kullanılır.
Kullanım: python run_admin.py
Hedef script: TARGET_SCRIPT değişkeninden okunur (içinde tanımlı)
"""

import sys
import os
import subprocess
import ctypes
import tempfile
import time
import logging
from pathlib import Path
from datetime import datetime

LOG_PATH = Path(os.environ.get("USERPROFILE", "C:/Users/eymen")) / "kiralog" / "run_admin.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("run_admin")

TARGET_SCRIPT = r"C:\Users\eymen\kiralog\docker_kurulum_final.py"

def find_real_python() -> str:
    candidates = [
        r"C:\Python313\python.exe", r"C:\Python312\python.exe",
        r"C:\Python311\python.exe", r"C:\Python310\python.exe",
        r"C:\Python39\python.exe",
        r"C:\Program Files\Python313\python.exe",
        r"C:\Program Files\Python312\python.exe",
    ]
    try:
        result = subprocess.run(["where", "python"], capture_output=True, text=True, timeout=5)
        for line in result.stdout.strip().splitlines():
            line = line.strip()
            if line and "WindowsApps" not in line and os.path.isfile(line):
                candidates.insert(0, line)
    except Exception:
        pass
    for c in candidates:
        if os.path.isfile(c):
            return c
    return sys.executable

PYTHON_EXE = find_real_python()
PS_EXE = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"

def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False

# Yöntem 1: ShellExecuteW runas -> powershell -> python zinciri
def method_shellexecute_chain() -> bool:
    ps_cmd = f"Start-Process -FilePath '{PYTHON_EXE}' -ArgumentList '\"{TARGET_SCRIPT}\"' -Verb RunAs -Wait"
    try:
        ret = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", PS_EXE,
            f'-NoProfile -ExecutionPolicy Bypass -Command "{ps_cmd}"',
            None, 1)
        return ret > 32
    except Exception:
        return False

# Yöntem 2: Scheduled Task
def method_scheduled_task() -> bool:
    task_name = "RunAdminPythonTemp"
    cmd = f'"{PYTHON_EXE}" "{TARGET_SCRIPT}"'
    subprocess.run(["schtasks", "/delete", "/tn", task_name, "/f"], capture_output=True, timeout=10)
    create = subprocess.run(
        ["schtasks", "/create", "/tn", task_name, "/tr", cmd, "/sc", "ONCE", "/st", "00:00", "/rl", "HIGHEST", "/f"],
        capture_output=True, text=True, timeout=15)
    if create.returncode != 0:
        return False
    run = subprocess.run(["schtasks", "/run", "/tn", task_name], capture_output=True, text=True, timeout=15)
    subprocess.run(["schtasks", "/delete", "/tn", task_name, "/f"], capture_output=True, timeout=10)
    return run.returncode == 0

# Yöntem 3: VBScript
def method_vbscript() -> bool:
    vbs = f'Set objShell = CreateObject("Shell.Application")\nobjShell.ShellExecute "{PYTHON_EXE}", Chr(34) & "{TARGET_SCRIPT}" & Chr(34), "", "runas", 1\nWScript.Sleep 2000\n'
    vbs_path = Path(tempfile.gettempdir()) / "run_admin_bridge.vbs"
    try:
        vbs_path.write_text(vbs, encoding="utf-8")
        r = subprocess.run(["cscript", "//Nologo", str(vbs_path)], capture_output=True, text=True, timeout=15)
        vbs_path.unlink(missing_ok=True)
        return r.returncode == 0
    except Exception:
        return False

# Yöntem 4: PowerShell Start-Process doğrudan
def method_powershell_direct() -> bool:
    ps_cmd = f"Start-Process -FilePath '{PYTHON_EXE}' -ArgumentList '\"{TARGET_SCRIPT}\"' -Verb RunAs -Wait"
    try:
        p = subprocess.Popen([PS_EXE, "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(4)
        return p.poll() is None or p.returncode == 0
    except Exception:
        return False

def main():
    log.info("=" * 60)
    log.info(f"run_admin.py baslatildi — {datetime.now().isoformat()}")
    log.info(f"Hedef script: {TARGET_SCRIPT}")
    log.info(f"Python exe: {PYTHON_EXE}")
    log.info(f"Admin: {is_admin()}")

    if not os.path.isfile(TARGET_SCRIPT):
        log.error(f"HEDEF BULUNAMADI: {TARGET_SCRIPT}")
        sys.exit(1)
    if is_admin():
        os.execv(PYTHON_EXE, [PYTHON_EXE, TARGET_SCRIPT])

    methods = [
        ("ShellExecuteW Zinciri", method_shellexecute_chain),
        ("Scheduled Task", method_scheduled_task),
        ("VBScript Koprusu", method_vbscript),
        ("PowerShell Dogrudan", method_powershell_direct),
    ]
    for name, fn in methods:
        log.info(f"--- Deneniyor: {name} ---")
        try:
            if fn():
                log.info(f"OK: {name}")
                sys.exit(0)
        except Exception as e:
            log.error(f"Hata ({name}): {e}")

    log.critical("TUM YONTEMLER BASARISIZ. Elle Yonetici PowerShell kullan.")
    sys.exit(1)

if __name__ == "__main__":
    main()
