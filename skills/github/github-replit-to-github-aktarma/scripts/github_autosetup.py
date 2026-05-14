#!/usr/bin/env python3
"""
github_autosetup.py
────────────────────────────────────────────────
Güvenlik izolasyonu + GitHub repo kurulumu + push
otomasyonu. Her adım raporlanır; hata olursa
tam teşhis çıkarılır ve script kaldığı yerden
devam edebilecek şekilde tasarlanmıştır.
────────────────────────────────────────────────
"""

import os
import sys
import subprocess
import textwrap
from pathlib import Path
from datetime import datetime

class C:
    OK    = "\033[92m"
    WARN  = "\033[93m"
    ERR   = "\033[91m"
    INFO  = "\033[96m"
    BOLD  = "\033[1m"
    RESET = "\033[0m"

report = {
    "baslanis": datetime.now().isoformat(timespec="seconds"),
    "adimlar": [],
    "hatalar": [],
    "tamamlandi": False,
}

def log(sembol, renk, baslik, detay=""):
    zaman = datetime.now().strftime("%H:%M:%S")
    print(f"{renk}{C.BOLD}[{zaman}] {sembol}  {baslik}{C.RESET}")
    if detay:
        for satir in textwrap.wrap(detay, width=70):
            print(f"         {C.INFO}{satir}{C.RESET}")

def adim_tamam(n, ad, detay=""):
    log("✔", C.OK, f"ADIM {n} TAMAM — {ad}", detay)
    report["adimlar"].append({"adim": n, "ad": ad, "durum": "TAMAM", "detay": detay})

def adim_hata(n, ad, hata, ipucu=""):
    log("✘", C.ERR, f"ADIM {n} HATA — {ad}", hata)
    if ipucu:
        log("→", C.WARN, "İPUCU", ipucu)
    report["adimlar"].append({"adim": n, "ad": ad, "durum": "HATA", "detay": hata})
    report["hatalar"].append({"adim": n, "mesaj": hata, "ipucu": ipucu})

def adim_atlandi(n, ad, neden):
    log("⊘", C.WARN, f"ADIM {n} ATLANDI — {ad}", neden)
    report["adimlar"].append({"adim": n, "ad": ad, "durum": "ATLANDI", "detay": neden})

def calistir(komut, cwd=None):
    proc = subprocess.run(komut, cwd=cwd, capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()

def rapor_yazdir():
    print()
    print(f"{C.BOLD}{'─'*55}{C.RESET}")
    print(f"{C.BOLD}  📋  ÇALIŞMA RAPORU  —  {report['baslanis']}{C.RESET}")
    print(f"{C.BOLD}{'─'*55}{C.RESET}")
    for a in report["adimlar"]:
        renk = C.OK if a["durum"] == "TAMAM" else (C.ERR if a["durum"] == "HATA" else C.WARN)
        isaret = "✔" if a["durum"] == "TAMAM" else ("✘" if a["durum"] == "HATA" else "⊘")
        print(f"  {renk}{isaret}  Adım {a['adim']:02d}  │  {a['durum']:<8}  │  {a['ad']}{C.RESET}")
        if a["detay"] and a["durum"] != "TAMAM":
            for s in textwrap.wrap(a["detay"], width=50):
                print(f"              {C.INFO}↳ {s}{C.RESET}")
    print(f"{C.BOLD}{'─'*55}{C.RESET}")
    if report["hatalar"]:
        print(f"\n{C.ERR}{C.BOLD}  ⚠  BULUNAN HATALAR ({len(report['hatalar'])} adet){C.RESET}")
        for h in report["hatalar"]:
            print(f"  • Adım {h['adim']}: {h['mesaj']}")
            if h["ipucu"]:
                print(f"    → {C.WARN}{h['ipucu']}{C.RESET}")
    else:
        print(f"\n{C.OK}{C.BOLD}  ✔  Hata tespit edilmedi.{C.RESET}")
    durum = f"{C.OK}BAŞARILI{C.RESET}" if report["tamamlandi"] else f"{C.ERR}YARIM KALDI{C.RESET}"
    print(f"\n  Genel Durum: {durum}\n")

def adim1_git_kontrol():
    log("○", C.INFO, "ADIM 1 — Git kurulum kontrolü")
    kod, out, err = calistir(["git", "--version"])
    if kod != 0:
        adim_hata(1, "Git kurulum kontrolü", err, "sudo apt install git  YA DA  https://git-scm.com")
        return False
    adim_tamam(1, "Git kurulum kontrolü", out)
    return True

def adim2_dizin_belirle():
    log("○", C.INFO, "ADIM 2 — Proje dizini belirleniyor")
    hedef = os.environ.get("PROJE_DIZIN", os.getcwd())
    yol = Path(hedef).resolve()
    if not yol.exists():
        adim_hata(2, "Proje dizini", f"Dizin bulunamadı: {yol}",
                  "PROJE_DIZIN ortam değişkenini ayarla veya scripti proje klasöründe çalıştır.")
        return None
    adim_tamam(2, "Proje dizini", str(yol))
    return yol

GITIGNORE_ZORUNLU = [
    ".env", ".env.*", "*.key", "*.pem", "__pycache__/",
    "*.pyc", ".DS_Store", "node_modules/", "venv/", ".venv/",
]

def adim3_gitignore(dizin):
    log("○", C.INFO, "ADIM 3 — .gitignore güvenlik izolasyonu")
    gi_yol = dizin / ".gitignore"
    mevcut = set()
    if gi_yol.exists():
        mevcut = {s.strip() for s in gi_yol.read_text().splitlines() if s.strip()}
        log("→", C.WARN, ".gitignore mevcut, eksikler eklenecek")
    eksikler = [s for s in GITIGNORE_ZORUNLU if s not in mevcut]
    try:
        with gi_yol.open("a", encoding="utf-8") as f:
            if eksikler:
                f.write("\n# --- otomatik eklendi ---\n")
                for s in eksikler:
                    f.write(s + "\n")
        adim_tamam(3, ".gitignore güvenlik izolasyonu",
                   f"Eklenen satırlar: {eksikler or 'yok (zaten tamam)'}")
        return True
    except OSError as e:
        adim_hata(3, ".gitignore yazma", str(e))
        return False

def adim4_env_kontrol(dizin):
    log("○", C.INFO, "ADIM 4 — .env dosya güvenlik taraması")
    env_yol = dizin / ".env"
    if not env_yol.exists():
        adim_atlandi(4, ".env güvenlik taraması", ".env dosyası yok; oluşturulduğunda .gitignore zaten koruyacak.")
        return True
    gi_yol = dizin / ".gitignore"
    if gi_yol.exists() and ".env" in gi_yol.read_text():
        adim_tamam(4, ".env güvenlik taraması", ".env mevcut ve .gitignore tarafından korunuyor.")
        return True
    adim_hata(4, ".env güvenlik taraması",
              ".env var ama .gitignore'da bulunamadı — commit tehlikesi!",
              "Adım 3'ü yeniden kontrol et veya .gitignore'u manuel düzenle.")
    return False

def adim5_git_init(dizin):
    log("○", C.INFO, "ADIM 5 — Git repo başlatma")
    git_dir = dizin / ".git"
    if git_dir.exists():
        adim_atlandi(5, "Git repo başlatma", "Zaten bir git reposu mevcut.")
        return True
    kod, out, err = calistir(["git", "init"], cwd=str(dizin))
    if kod != 0:
        adim_hata(5, "git init", err)
        return False
    # Fix: default branch master → main
    calistir(["git", "branch", "-m", "main"], cwd=str(dizin))
    adim_tamam(5, "git init", f"{out}\n  (branch → main)")
    return True

def adim6_git_config(dizin):
    log("○", C.INFO, "ADIM 6 — Git kullanıcı yapılandırması")
    ad = os.environ.get("GIT_KULLANICI_AD", "")
    eposta = os.environ.get("GIT_KULLANICI_EPOSTA", "")
    if not ad or not eposta:
        _, g_ad, _ = calistir(["git", "config", "--global", "user.name"])
        _, g_ep, _ = calistir(["git", "config", "--global", "user.email"])
        if g_ad and g_ep:
            adim_tamam(6, "Git kullanıcı yapılandırması",
                       f"{g_ad} <{g_ep}> (global config'den alındı)")
            return True
        adim_hata(6, "Git kullanıcı yapılandırması",
                  "Ad/eposta bulunamadı.",
                  "GIT_KULLANICI_AD ve GIT_KULLANICI_EPOSTA ortam değişkenlerini ayarla.")
        return False
    for key, val in [("user.name", ad), ("user.email", eposta)]:
        kod, _, err = calistir(["git", "config", key, val], cwd=str(dizin))
        if kod != 0:
            adim_hata(6, f"git config {key}", err)
            return False
    adim_tamam(6, "Git kullanıcı yapılandırması", f"{ad} <{eposta}>")
    return True

def adim7_git_add(dizin):
    log("○", C.INFO, "ADIM 7 — Dosyalar stage'e alınıyor")
    kod, out, err = calistir(["git", "add", "."], cwd=str(dizin))
    if kod != 0:
        adim_hata(7, "git add", err)
        return False
    _, staged, _ = calistir(["git", "diff", "--cached", "--name-only"], cwd=str(dizin))
    sayi = len(staged.splitlines()) if staged else 0
    adim_tamam(7, "Dosyalar stage'e alındı", f"{sayi} dosya eklendi.")
    return True

def adim8_commit(dizin):
    log("○", C.INFO, "ADIM 8 — Commit oluşturuluyor")
    _, staged, _ = calistir(["git", "diff", "--cached", "--name-only"], cwd=str(dizin))
    if not staged:
        adim_atlandi(8, "Commit", "Stage boş; commit edilecek değişiklik yok.")
        return True
    mesaj = os.environ.get("COMMIT_MESAJI", "chore: güvenlik izolasyonu ve proje altyapısı kuruldu")
    kod, out, err = calistir(["git", "commit", "-m", mesaj], cwd=str(dizin))
    if kod != 0:
        adim_hata(8, "git commit", err, "git config user.email ve user.name ayarlanmış mı? (Adım 6)")
        return False
    adim_tamam(8, "Commit", f"Mesaj: '{mesaj}'")
    return True

def adim9_remote(dizin):
    log("○", C.INFO, "ADIM 9 — GitHub remote yapılandırması")
    remote_url = os.environ.get("GITHUB_REMOTE_URL", "")
    kod, mevcut_remote, _ = calistir(["git", "remote", "get-url", "origin"], cwd=str(dizin))
    if kod == 0:
        adim_atlandi(9, "Remote yapılandırması", f"'origin' zaten mevcut: {mevcut_remote}")
        return True
    if not remote_url:
        adim_hata(9, "GitHub remote URL",
                  "GITHUB_REMOTE_URL ortam değişkeni tanımlanmamış.",
                  "Örn: export GITHUB_REMOTE_URL=https://github.com/KULLANICI/REPO.git")
        return False
    kod, out, err = calistir(["git", "remote", "add", "origin", remote_url], cwd=str(dizin))
    if kod != 0:
        adim_hata(9, "git remote add", err)
        return False
    adim_tamam(9, "Remote eklendi", remote_url)
    return True

def adim10_push(dizin):
    log("○", C.INFO, "ADIM 10 — GitHub'a push")
    branch = os.environ.get("GIT_BRANCH", "main")
    kod, out, err = calistir(["git", "push", "-u", "origin", branch], cwd=str(dizin))
    if kod != 0:
        adim_hata(10, "git push", err,
                  "Token/SSH yetkisi eksik olabilir. "
                  "https://docs.github.com/en/authentication adresini kontrol et.")
        return False
    adim_tamam(10, "Push tamamlandı", f"Branch: {branch}\n{out}")
    return True

def main():
    print(f"\n{C.BOLD}{'═'*55}{C.RESET}")
    print(f"{C.BOLD}  🚀  github_autosetup.py  —  başlatılıyor{C.RESET}")
    print(f"{C.BOLD}{'═'*55}{C.RESET}\n")

    if not adim1_git_kontrol():
        rapor_yazdir(); sys.exit(1)

    dizin = adim2_dizin_belirle()
    if not dizin:
        rapor_yazdir(); sys.exit(1)

    sirali = [
        lambda: adim3_gitignore(dizin),
        lambda: adim4_env_kontrol(dizin),
        lambda: adim5_git_init(dizin),
        lambda: adim6_git_config(dizin),
        lambda: adim7_git_add(dizin),
        lambda: adim8_commit(dizin),
        lambda: adim9_remote(dizin),
        lambda: adim10_push(dizin),
    ]

    for i, fn in enumerate(sirali, start=3):
        if not fn():
            log("!", C.ERR, f"Adım {i} başarısız — script durduruluyor")
            rapor_yazdir()
            sys.exit(1)

    report["tamamlandi"] = True
    rapor_yazdir()

if __name__ == "__main__":
    main()
