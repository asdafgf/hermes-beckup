"""
wsl_docker_kur.py
WSL Ubuntu icine Docker kurar. Admin gerekmez.
Kullanim: python wsl_docker_kur.py
"""

import subprocess, time, sys

G = "\033[92m"; Y = "\033[93m"; R = "\033[91m"; B = "\033[94m"; S = "\033[0m"
def ok(msg):   print(f"{G}OK {msg}{S}")
def info(msg): print(f"{B}-> {msg}{S}")
def warn(msg): print(f"{Y}!! {msg}{S}")
def err(msg):  print(f"{R}XX {msg}{S}")

def bekle(sn=10):
    for i in range(sn, 0, -1): print(f"\r  {Y}{i}s...{S}", end="", flush=True); time.sleep(1)
    print()

def calistir(aciklama, komut, hata_kritik=True):
    info(aciklama)
    r = subprocess.run(["wsl", "-e", "bash", "-c", komut], capture_output=False, text=True)
    if r.returncode != 0 and hata_kritik: err(f"BASARISIZ: {aciklama} (kod {r.returncode})"); sys.exit(1)
    elif r.returncode == 0: ok(f"Tamam: {aciklama}")
    return r.returncode

print(f"\n{B}{'='*55}\n  WSL Ubuntu - Docker Kurulum\n{'='*55}{S}\n")
r = subprocess.run(["wsl", "echo", "OK"], capture_output=True, text=True)
if r.returncode != 0 or "OK" not in r.stdout: err("WSL erisilemiyor."); sys.exit(1)
ok("WSL erisilebilir.")
bekle(3)

calistir("Eski Docker temizleniyor", "sudo apt-get remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true", hata_kritik=False); bekle(5)
calistir("apt-get update", "sudo apt-get update -y"); bekle(10)
calistir("Bagimliliklar (ca-certificates, curl, gnupg)", "sudo apt-get install -y ca-certificates curl gnupg lsb-release"); bekle(5)
calistir("Docker GPG anahtari", "sudo install -m 0755 -d /etc/apt/keyrings && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg && sudo chmod a+r /etc/apt/keyrings/docker.gpg"); bekle(5)
calistir("Docker repo ekle", 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null'); bekle(5)
calistir("apt-get update (Docker repo)", "sudo apt-get update -y"); bekle(10)
calistir("Docker Engine+CLI+Compose", "sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin"); bekle(10)
calistir("Docker servis baslat", "sudo service docker start"); bekle(5)
kullanici = subprocess.run(["wsl", "whoami"], capture_output=True, text=True).stdout.strip()
calistir(f"'{kullanici}' docker grubuna", f"sudo usermod -aG docker {kullanici}"); bekle(5)
info("Test: sudo docker run --rm hello-world")
subprocess.run(["wsl", "-e", "bash", "-c", "sudo docker run --rm hello-world"], capture_output=False, text=True)
print(f"\n{G}{'='*55}\n  KURULUM TAMAM\n{'='*55}{S}")
print("\nKullanim: wsl -e bash -c 'docker ps'")
