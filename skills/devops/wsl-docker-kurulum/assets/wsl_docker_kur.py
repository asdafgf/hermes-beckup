"""
wsl_docker_kur.py
WSL Ubuntu içine Docker kurar. Admin gerekmez.
Çalıştır: python wsl_docker_kur.py
"""

import subprocess
import time
import sys

# ─── RENK ──────────────────────────────────────────────────────────────────────
G = "\033[92m"   # yeşil
Y = "\033[93m"   # sarı
R = "\033[91m"   # kırmızı
B = "\033[94m"   # mavi
S = "\033[0m"    # sıfırla

def ok(msg):   print(f"{G}✓ {msg}{S}")
def info(msg): print(f"{B}→ {msg}{S}")
def warn(msg): print(f"{Y}⚠ {msg}{S}")
def err(msg):  print(f"{R}✗ {msg}{S}")

def bekle(sn=10):
    for i in range(sn, 0, -1):
        print(f"\r  {Y}{i}s bekleniyor...{S}", end="", flush=True)
        time.sleep(1)
    print()

def calistir(aciklama, komut, hata_kritik=True):
    info(aciklama)
    sonuc = subprocess.run(
        ["wsl", "-e", "bash", "-c", komut],
        capture_output=False,
        text=True,
    )
    if sonuc.returncode != 0 and hata_kritik:
        err(f"BASARISIZ: {aciklama} (kod {sonuc.returncode})")
        sys.exit(1)
    elif sonuc.returncode == 0:
        ok(f"Tamamlandi: {aciklama}")
    return sonuc.returncode

# 10 ADIM: #################################################################
print(f"\n{B}{'='*55}")
print("  WSL Ubuntu — Docker Otomatik Kurulum")
print(f"{'='*55}{S}\n")

# 1. WSL erisim kontrolu
info("WSL erisimi kontrol ediliyor...")
test = subprocess.run(["wsl", "echo", "OK"], capture_output=True, text=True)
if test.returncode != 0 or "OK" not in test.stdout:
    err("WSL erisilemiyor. 'wsl --list --running' ciktisini kontrol et.")
    sys.exit(1)
ok("WSL erisilebilir.")
bekle(3)

# 2. Eski Docker artiklarini temizle
calistir(
    "Eski Docker paketleri temizleniyor",
    "sudo apt-get remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true",
    hata_kritik=False
)
bekle(5)

# 3. Paket listesi guncelle
calistir(
    "apt-get update calistiriliyor",
    "sudo apt-get update -y"
)
bekle(10)

# 4. Gerekli bagimliliklar
calistir(
    "Bagimliliklar kuruluyor (ca-certificates, curl, gnupg)",
    "sudo apt-get install -y ca-certificates curl gnupg lsb-release"
)
bekle(5)

# 5. Docker GPG anahtari
calistir(
    "Docker GPG anahtari ekleniyor",
    "sudo install -m 0755 -d /etc/apt/keyrings && "
    "curl -fsSL https://download.docker.com/linux/ubuntu/gpg "
    "| sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg && "
    "sudo chmod a+r /etc/apt/keyrings/docker.gpg"
)
bekle(5)

# 6. Docker repo ekle
calistir(
    "Docker deposu ekleniyor",
    'echo "deb [arch=$(dpkg --print-architecture) '
    'signed-by=/etc/apt/keyrings/docker.gpg] '
    'https://download.docker.com/linux/ubuntu '
    '$(. /etc/os-release && echo "$VERSION_CODENAME") stable" '
    '| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null'
)
bekle(5)

# 7. Guncel paket listesi (repo eklendi)
calistir(
    "apt-get update (Docker reposuyla)",
    "sudo apt-get update -y"
)
bekle(10)

# 8. Docker Engine kur
calistir(
    "Docker Engine, CLI ve Compose kuruluyor",
    "sudo apt-get install -y "
    "docker-ce docker-ce-cli containerd.io "
    "docker-buildx-plugin docker-compose-plugin"
)
bekle(10)

# 9. Docker servisini baslat
calistir(
    "Docker servisi baslatiliyor",
    "sudo service docker start"
)
bekle(5)

# 10. Kullaniciyi docker grubuna ekle + test
import os
linux_user = subprocess.run(
    ["wsl", "whoami"], capture_output=True, text=True
).stdout.strip()
calistir(
    f"'{linux_user}' kullanicisi docker grubuna ekleniyor",
    f"sudo usermod -aG docker {linux_user}"
)
bekle(5)

info("Docker kurulumu test ediliyor (hello-world)...")
test_sonuc = subprocess.run(
    ["wsl", "-e", "bash", "-c", "sudo docker run --rm hello-world"],
    capture_output=False, text=True
)
bekle(10)

# ─── OZET ──────────────────────────────────────────────────────────────────────
print(f"\n{G}{'='*55}")
print("  KURULUM TAMAMLANDI")
print(f"{'='*55}{S}")
print()
print("Kullanim:")
print(f"  {Y}wsl{S}                          -> WSL terminalini ac")
print(f"  {Y}docker ps{S}                    -> calisan container'lar")
print(f"  {Y}docker compose up -d{S}         -> proje baslat")
print()
warn("Ilk seferinde 'sudo docker ...' kullan.")
warn("Gruba ekleme icin WSL'yi kapat/ac: wsl --shutdown")
print()
