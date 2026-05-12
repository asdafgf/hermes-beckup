"""
replit_export.py — Runners-Journey @ Replit → ZIP İndirici
Gereksinimler:
    pip install undetected-chromedriver selenium colorama python-dotenv
"""

import os, sys, time, glob, traceback, re
from pathlib import Path
from getpass import getpass

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("colorama bulunamadı → pip install colorama"); sys.exit(1)

def log(msg, level="INFO"):
    icons = {"INFO": ("●", Fore.CYAN), "OK": ("✔", Fore.GREEN),
             "WARN": ("▲", Fore.YELLOW), "ERR": ("✖", Fore.RED),
             "STEP": ("►", Fore.MAGENTA)}
    icon, color = icons.get(level, ("·", Fore.WHITE))
    print(f"{color}{icon} {msg}{Style.RESET_ALL}")

try:
    from dotenv import load_dotenv; load_dotenv()
except ImportError: pass

REPLIT_EMAIL    = os.getenv("REPLIT_EMAIL", "")
REPLIT_PASSWORD = os.getenv("REPLIT_PASSWORD", "")
REPLIT_USER     = os.getenv("REPLIT_USER", "")
REPLIT_PROJECT  = os.getenv("REPLIT_PROJECT", "Proje")
DOWNLOAD_DIR    = os.getenv("DOWNLOAD_DIR",
                  str(Path.home() / "Downloads" / "replit_export"))

CHROME_EXE = r"C:\Users\eymen\scoop\apps\googlechrome\current\chrome.exe"
CHROME_PROFILE = r"C:\Users\eymen\AppData\Local\Google\Chrome\User Data"
TIMEOUT = 60

try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
except ImportError as e:
    log(f"Eksik paket: {e}", "ERR")
    log("Çözüm: pip install undetected-chromedriver selenium colorama python-dotenv", "WARN")
    sys.exit(1)

def build_driver():
    log("Chrome driver hazırlanıyor (undetected-chromedriver)...", "STEP")
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={CHROME_PROFILE}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,900")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36")
    prefs = {"download.default_directory": str(Path(DOWNLOAD_DIR).resolve()),
             "download.prompt_for_download": False,
             "download.directory_upgrade": True, "safebrowsing.enabled": False}
    options.add_experimental_option("prefs", prefs)
    options.binary_location = CHROME_EXE
    driver = uc.Chrome(options=options, use_subprocess=True)
    driver.set_page_load_timeout(TIMEOUT)
    log("Driver başlatıldı.", "OK")
    return driver

def login(driver):
    log("Replit giriş sayfasına gidiliyor...", "STEP")
    driver.get("https://replit.com/login")
    time.sleep(3)
    if "dashboard" in driver.current_url or "/~" in driver.current_url:
        log("Mevcut Chrome profiliyle zaten giriş yapılmış.", "OK")
        return
    try:
        wait = WebDriverWait(driver, TIMEOUT)
        email_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[name='username'], input[type='email']")))
        email_input.clear()
        email_input.send_keys(REPLIT_EMAIL)
        time.sleep(0.5)
        pass_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        pass_input.clear()
        pass_input.send_keys(REPLIT_PASSWORD)
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        wait.until(lambda d: "dashboard" in d.current_url or "/~" in d.current_url)
        log("Giriş başarılı!", "OK")
    except TimeoutException:
        log("Giriş zaman aşımı. Manuel giriş bekleniyor (max 120 sn)...", "WARN")
        WebDriverWait(driver, 120).until(
            lambda d: "dashboard" in d.current_url or "/~" in d.current_url)
        log("Manuel giriş algılandı.", "OK")

def navigate_to_project(driver):
    url = f"https://replit.com/@{REPLIT_USER}/{REPLIT_PROJECT}"
    log(f"Proje sayfasına gidiliyor: {url}", "STEP")
    driver.get(url)
    time.sleep(3)
    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.TAG_NAME, "main")))
    log(f"Proje sayfası yüklendi: {driver.title}", "OK")

def download_zip(driver):
    wait = WebDriverWait(driver, TIMEOUT)
    # Yöntem 1: Doğrudan ZIP URL
    direct_url = f"https://replit.com/@{REPLIT_USER}/{REPLIT_PROJECT}.zip"
    before = set(glob.glob(str(Path(DOWNLOAD_DIR) / "*.zip")))
    driver.get(direct_url)
    time.sleep(5)
    after = set(glob.glob(str(Path(DOWNLOAD_DIR) / "*.zip")))
    if after - before:
        f = list(after - before)[0]
        log(f"ZIP indirildi (doğrudan URL): {f}", "OK")
        return f
    # Yöntem 2: Menü
    log("Doğrudan URL çalışmadı; menü yöntemi deneniyor...", "WARN")
    driver.get(f"https://replit.com/@{REPLIT_USER}/{REPLIT_PROJECT}")
    time.sleep(3)
    for sel in ["[data-cy='kebab-menu']", "button[aria-label='More options']",
                 "//button[contains(@aria-label,'more') or contains(@aria-label,'More')]"]:
        try:
            m = wait.until(EC.element_to_be_clickable(
                (By.XPATH if sel.startswith("//") else By.CSS_SELECTOR, sel)))
            log("Menü bulundu", "OK")
            m.click(); time.sleep(1.5)
            break
        except: continue
    else:
        raise RuntimeError("Menü bulunamadı.")
    for sel in ["//li[contains(text(),'Download')]", "//button[contains(text(),'Download')]",
                 "[data-cy='download-zip']"]:
        try:
            d = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH if sel.startswith("//") else By.CSS_SELECTOR, sel)))
            log("Download as ZIP bulundu", "OK")
            before = set(glob.glob(str(Path(DOWNLOAD_DIR) / "*.zip")))
            d.click()
            log("İndirme başlatıldı...", "STEP")
            deadline = time.time() + 120
            while time.time() < deadline:
                time.sleep(2)
                if not glob.glob(str(Path(DOWNLOAD_DIR) / "*.crdownload")):
                    after = set(glob.glob(str(Path(DOWNLOAD_DIR) / "*.zip")))
                    if after - before:
                        f = list(after - before)[0]
                        log(f"İndirme tamamlandı: {f}  ({Path(f).stat().st_size/1024:.0f} KB)", "OK")
                        return f
            raise TimeoutError("İndirme 120sn'de tamamlanamadı")
        except: continue
    raise RuntimeError("Download ZIP seçeneği bulunamadı.")

def main():
    print(f"\n{Fore.MAGENTA}{'═'*55}{Style.RESET_ALL}")
    log("REPLIT EXPORT — Başlatılıyor", "STEP")

    if not REPLIT_EMAIL: REPLIT_EMAIL = input("● Replit e-posta: ").strip()
    if not REPLIT_PASSWORD: REPLIT_PASSWORD = getpass("● Replit şifre: ")
    if not REPLIT_USER: REPLIT_USER = input("● Replit kullanıcı adı: ").strip()
    if not REPLIT_PROJECT: REPLIT_PROJECT = input("● Proje adı: ").strip()
    Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)
    log(f"İndirme klasörü: {DOWNLOAD_DIR}", "INFO")

    driver = None
    try:
        driver = build_driver()
        login(driver)
        navigate_to_project(driver)
        zip_path = download_zip(driver)
        log(f"TAMAMLANDI → {zip_path}", "OK")
    except KeyboardInterrupt:
        log("Kullanıcı tarafından iptal edildi.", "WARN")
    except Exception as e:
        log(f"HATA: {e}", "ERR")
        traceback.print_exc()
    finally:
        if driver:
            try: driver.quit(); log("Browser kapatıldı.", "INFO")
            except: pass

if __name__ == "__main__":
    main()
