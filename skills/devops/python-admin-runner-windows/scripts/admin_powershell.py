"""
admin_powershell.py
───────────────────
Windows 11'de herhangi bir Python script'ini Yönetici PowerShell üzerinden
çalıştırır. venv / git-bash kaynaklı "Access Denied (kod 5)" sorununu
sys.executable yerine system-level python/powershell kullanarak aşar.

Kullanım:
    python admin_powershell.py C:\path\to\hedef_script.py [arg1 arg2 ...]

Strateji:
    1. Önce PowerShell ile dener  (en güvenilir UAC yolu)
    2. Başarısız olursa cmd.exe /c ile dener
    3. O da başarısız olursa doğrudan ShellExecuteW dener
    Her strateji stdout/stderr'i bir log dosyasına yönlendirir.
"""

import sys
import os
import ctypes
import subprocess
import tempfile
import textwrap
import time
from pathlib import Path
from ctypes import wintypes

# ── Sabitler ─────────────────────────────────────────────────────────────────
SW_SHOWNORMAL   = 1
SEE_MASK_NOCLOSEPROCESS = 0x00000040
ERROR_CANCELLED = 1223   # kullanıcı UAC'yi iptal etti


# ── Yardımcılar ──────────────────────────────────────────────────────────────

def find_system_python() -> str:
    """
    venv dışında, sistem genelinde kullanılabilir bir python.exe bulur.
    py launcher → PATH'teki python → son çare sabit yollar sırasıyla dener.
    """
    candidates = []

    # 1) py.exe launcher (Windows'ta en güvenilir)
    py_launcher = Path(os.environ.get("SystemRoot", "C:\\Windows")) / "py.exe"
    if py_launcher.exists():
        candidates.append(str(py_launcher))

    # 2) PATH üzerindeki python — ama venv değilse
    for p in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(p) / "python.exe"
        if candidate.exists() and "venv" not in str(candidate).lower() and \
                ".venv" not in str(candidate).lower():
            candidates.append(str(candidate))

    # 3) Sabit konumlar
    for drive in ["C", "D"]:
        for pattern in [
            rf"{drive}:\Python3*\python.exe",
            rf"{drive}:\Program Files\Python3*\python.exe",
            rf"{drive}:\Users\*\AppData\Local\Programs\Python\Python3*\python.exe",
        ]:
            import glob
            candidates.extend(glob.glob(pattern))

    if not candidates:
        raise FileNotFoundError(
            "Sistem Python bulunamadı. py.exe veya PATH'te python.exe olduğundan emin ol."
        )
    return candidates[0]


def make_log_path(target_script: str) -> str:
    """Log dosyası yolunu oluşturur — target script yanında veya TEMP'te."""
    try:
        log_dir = Path(target_script).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / (Path(target_script).stem + "_admin_run.log")
        # Yazma testi
        log_path.touch()
        return str(log_path)
    except PermissionError:
        return str(Path(tempfile.gettempdir()) / (Path(target_script).stem + "_admin_run.log"))


def build_ps_command(python_exe: str, target_script: str,
                     extra_args: list, log_path: str) -> str:
    """
    PowerShell -Command string'i oluşturur.
    stdout + stderr'i log dosyasına yönlendirir; exit code'u da yazar.
    """
    # Yolları tek-tırnak içine al (PS injection'a karşı)
    py   = python_exe.replace("'", "''")
    scr  = target_script.replace("'", "''")
    log  = log_path.replace("'", "''")
    args = " ".join(f"'{a.replace(chr(39), chr(39)*2)}'" for a in extra_args)

    return textwrap.dedent(f"""
        $ErrorActionPreference = 'Continue'
        $ts = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
        "[$ts] === Admin run started ===" | Out-File -FilePath '{log}' -Encoding UTF8
        "Python  : {py}"  | Out-File -FilePath '{log}' -Append
        "Script  : {scr}" | Out-File -FilePath '{log}' -Append
        "Args    : {args if args else '(none)'}" | Out-File -FilePath '{log}' -Append
        ""            | Out-File -FilePath '{log}' -Append
        try {{
            & '{py}' '{scr}' {args} 2>&1 | Tee-Object -FilePath '{log}' -Append
            $ec = $LASTEXITCODE
        }} catch {{
            $_ | Out-File -FilePath '{log}' -Append
            $ec = 1
        }}
        "" | Out-File -FilePath '{log}' -Append
        "[Exit Code: $ec]" | Out-File -FilePath '{log}' -Append
        exit $ec
    """).strip()


# ── Strateji 1: PowerShell runas ─────────────────────────────────────────────

def strategy_powershell(python_exe: str, target_script: str,
                        extra_args: list, log_path: str) -> int:
    """ShellExecuteExW ile powershell.exe'yi runas verb'üyle başlatır."""

    ps_script = build_ps_command(python_exe, target_script, extra_args, log_path)

    # PS komutunu geçici bir .ps1 dosyasına yaz (uzun argüman sorununu önler)
    ps1_file = Path(tempfile.gettempdir()) / "admin_run_tmp.ps1"
    ps1_file.write_text(ps_script, encoding="utf-8")

    powershell = str(
        Path(os.environ.get("SystemRoot", "C:\\Windows"))
        / "System32" / "WindowsPowerShell" / "v1.0" / "powershell.exe"
    )
    if not Path(powershell).exists():
        # pwsh (PowerShell 7+)
        powershell = "pwsh.exe"

    params = f'-NoProfile -ExecutionPolicy Bypass -File "{ps1_file}"'

    return _shell_execute(powershell, params)


# ── Strateji 2: cmd.exe /c ───────────────────────────────────────────────────

def strategy_cmd(python_exe: str, target_script: str,
                 extra_args: list, log_path: str) -> int:
    """cmd.exe /c ile çalıştırır; UAC diyaloğu yine de açılır."""

    args_str = " ".join(f'"{a}"' for a in extra_args)
    cmd_line  = (
        f'/c "{python_exe}" "{target_script}" {args_str} '
        f'>> "{log_path}" 2>&1'
    )
    cmd_exe = str(
        Path(os.environ.get("SystemRoot", "C:\\Windows")) / "System32" / "cmd.exe"
    )
    return _shell_execute(cmd_exe, cmd_line)


# ── Strateji 3: Doğrudan python.exe runas ────────────────────────────────────

def strategy_direct(python_exe: str, target_script: str,
                    extra_args: list, log_path: str) -> int:
    """python.exe'yi doğrudan runas ile başlatır (log yok — son çare)."""
    args_str = f'"{target_script}"' + (
        " " + " ".join(f'"{a}"' for a in extra_args) if extra_args else ""
    )
    print("⚠  Bu stratejide log çıktısı alınamaz. Konsol ekranında görünür.")
    return _shell_execute(python_exe, args_str)


# ── ShellExecuteEx çekirdek çağrısı ──────────────────────────────────────────

class SHELLEXECUTEINFOW(ctypes.Structure):
    _fields_ = [
        ("cbSize",       wintypes.DWORD),
        ("fMask",        wintypes.ULONG),
        ("hwnd",         wintypes.HWND),
        ("lpVerb",       wintypes.LPCWSTR),
        ("lpFile",       wintypes.LPCWSTR),
        ("lpParameters", wintypes.LPCWSTR),
        ("lpDirectory",  wintypes.LPCWSTR),
        ("nShow",        ctypes.c_int),
        ("hInstApp",     wintypes.HINSTANCE),
        ("lpIDList",     ctypes.c_void_p),
        ("lpClass",      wintypes.LPCWSTR),
        ("hkeyClass",    wintypes.HKEY),
        ("dwHotKey",     wintypes.DWORD),
        ("hIconOrMonitor", ctypes.c_void_p),
        ("hProcess",     wintypes.HANDLE),
    ]


def _shell_execute(exe: str, params: str) -> int:
    """
    ShellExecuteExW ile verilen exe'yi 'runas' verb'üyle çalıştırır.
    Process handle'ı bekler; exit code'u döner.
    -1 → UAC iptal, -2 → başka hata.
    """
    sei = SHELLEXECUTEINFOW()
    sei.cbSize      = ctypes.sizeof(SHELLEXECUTEINFOW)
    sei.fMask       = SEE_MASK_NOCLOSEPROCESS
    sei.lpVerb      = "runas"
    sei.lpFile      = exe
    sei.lpParameters = params
    sei.lpDirectory  = str(Path(exe).parent) if Path(exe).exists() else None
    sei.nShow       = SW_SHOWNORMAL

    shell32 = ctypes.windll.shell32
    ok = shell32.ShellExecuteExW(ctypes.byref(sei))

    if not ok:
        err = ctypes.GetLastError()
        if err == ERROR_CANCELLED:
            return -1   # kullanıcı iptal
        return -2       # başka hata

    # Process'i bekle
    if sei.hProcess:
        kernel32 = ctypes.windll.kernel32
        kernel32.WaitForSingleObject(sei.hProcess, 0xFFFFFFFF)  # INFINITE
        exit_code = wintypes.DWORD()
        kernel32.GetExitCodeProcess(sei.hProcess, ctypes.byref(exit_code))
        kernel32.CloseHandle(sei.hProcess)
        return exit_code.value

    return 0


# ── Ana akış ─────────────────────────────────────────────────────────────────

def run(target_script: str, extra_args: list) -> None:
    target = Path(target_script).resolve()
    if not target.exists():
        print(f"✗ Script bulunamadı: {target}")
        sys.exit(1)

    try:
        python_exe = find_system_python()
    except FileNotFoundError as e:
        print(f"✗ {e}")
        sys.exit(1)

    log_path = make_log_path(str(target))

    print(f"► Hedef script : {target}")
    print(f"► Python       : {python_exe}")
    print(f"► Log dosyası  : {log_path}")
    print()

    strategies = [
        ("PowerShell runas",    strategy_powershell),
        ("cmd.exe /c runas",    strategy_cmd),
        ("Doğrudan python runas", strategy_direct),
    ]

    for name, fn in strategies:
        print(f"[*] Strateji deneniyor: {name} ...", end=" ", flush=True)
        try:
            rc = fn(python_exe, str(target), extra_args, log_path)
        except Exception as exc:
            print(f"HATA → {exc}")
            continue

        if rc == -1:
            print("UAC iptal edildi — kullanıcı reddetti.")
            print("  → Başka strateji deneniyor...")
            continue
        elif rc == -2:
            print(f"ShellExecute hatası (WinErr: {ctypes.GetLastError()})")
            continue
        else:
            print(f"TAMAMLANDI (exit code: {rc})")
            break
    else:
        print("\n✗ Tüm stratejiler başarısız. UAC devre dışı olabilir veya")
        print("  Windows politikası tüm yükseltmeleri engelliyor.")
        sys.exit(1)

    # Log varsa göster
    time.sleep(0.5)
    log = Path(log_path)
    if log.exists() and log.stat().st_size > 0:
        print(f"\n{'─'*60}")
        print(f"LOG ({log_path}):")
        print('─'*60)
        try:
            print(log.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            print(f"Log okunamadı; elle aç: {log_path}")
    else:
        print(f"\nLog dosyası boş veya oluşturulamadı: {log_path}")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if sys.platform != "win32":
        print("✗ Bu script yalnızca Windows'ta çalışır.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print(__doc__)
        print("\nKullanım: python admin_powershell.py <script.py> [arg1 arg2 ...]")
        sys.exit(0)

    run(sys.argv[1], sys.argv[2:])
