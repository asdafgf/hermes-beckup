#!/usr/bin/env python3
"""
Yerel CI/CD Betiği — Her güncellemede test harness'ı otomatik tetikler.
Kullanım:
  python ci/run_tests.py              # Tüm testleri çalıştır
  python ci/run_tests.py --watch      # Dosya değişikliklerini izle
  python ci/run_tests.py --coverage   # Kod kapsamı raporu
  python ci/run_tests.py tests/test_module.py  # Tek dosyayı test et
"""
import subprocess, sys, os, time, hashlib
from pathlib import Path
from datetime import datetime

GREEN = "\033[92m"; RED = "\033[91m"; YELLOW = "\033[93m"; CYAN = "\033[96m"; RESET = "\033[0m"
PROJE_KOKU = Path(__file__).resolve().parent.parent
TEST_DIR = PROJE_KOKU / "tests"
SRC_DIR = PROJE_KOKU / "src"

def log(renk, mesaj):
    print(f"{renk}[{datetime.now().strftime('%H:%M:%S')}] {mesaj}{RESET}")

def testleri_calistir(hedef=None, coverage=False):
    log(CYAN, "Test baslatiliyor...")
    komut = [sys.executable, "-m", "pytest"]
    komut.append(str(hedef or TEST_DIR))
    komut.extend(["-v", "--tb=short"])
    if coverage:
        komut.extend(["--cov=src", "--cov-report=term-missing"])
    basla = time.time()
    result = subprocess.run(komut, cwd=PROJE_KOKU, capture_output=False)
    gecen = time.time() - basla
    if result.returncode == 0:
        log(GREEN, f"TUM TESTLER BASARILI ({gecen:.1f} sn)")
    else:
        log(RED, f"TEST HATASI ({gecen:.1f} sn)")
    return result.returncode

def izleme_modu():
    log(CYAN, "Izleme modu. Cikmak icin Ctrl+C")
    dosya_ozetleri = {}
    try:
        while True:
            degisti = False
            for dosya in list(SRC_DIR.rglob("*.py")) + list(TEST_DIR.rglob("*.py")):
                with open(dosya, "rb") as f:
                    ozet = hashlib.md5(f.read()).hexdigest()
                if dosya not in dosya_ozetleri:
                    dosya_ozetleri[dosya] = ozet
                elif dosya_ozetleri[dosya] != ozet:
                    log(CYAN, f"Degisiklik: {dosya.name}")
                    dosya_ozetleri[dosya] = ozet
                    degisti = True
            if degisti:
                testleri_calistir()
            time.sleep(2)
    except KeyboardInterrupt:
        log(YELLOW, "Izleme sonlandirildi.")

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--watch" in args:
        izleme_modu()
    elif "--coverage" in args:
        testleri_calistir(coverage=True)
    elif args and args[0] not in ("--help",):
        testleri_calistir(args[0])
    else:
        testleri_calistir()
