#!/usr/bin/env python3

"""

╔══════════════════════════════════════════════════════════════════╗

║        EXCEL ADD-IN DIAGNOSTIC TOOL  —  Full Authority          ║

║  Hedef: Office Catalog bağlantı sorunlarını tespit & raporla    ║

╚══════════════════════════════════════════════════════════════════╝



Kapsam:

  • DNS çözümleme

  • TCP bağlantı (port 80 / 443)

  • SSL sertifika doğrulama

  • HTTP/HTTPS yanıt kodu & gecikme

  • Proxy ayarı tespiti

  • Windows kayıt defteri (Office catalog URL'leri) — sadece Windows

  • İzin engeli (Firewall / AV sinyal tespiti)

  • Office add-in manifest URL erişim testi

  • Sonuç: JSON + HTML raporu

"""



import sys

import os

import json

import socket

import ssl

import time

import datetime

import platform

import subprocess

import traceback

import urllib.request

import urllib.error

import urllib.parse

from typing import Optional



# ── Renkli terminal çıktısı ────────────────────────────────────────

class C:

    OK    = "\033[92m"

    WARN  = "\033[93m"

    FAIL  = "\033[91m"

    BOLD  = "\033[1m"

    DIM   = "\033[2m"

    RESET = "\033[0m"



def ok(msg):   print(f"  {C.OK}✓{C.RESET} {msg}")

def warn(msg): print(f"  {C.WARN}⚠{C.RESET} {msg}")

def fail(msg): print(f"  {C.FAIL}✗{C.RESET} {msg}")

def hdr(msg):  print(f"\n{C.BOLD}{'─'*60}\n  {msg}\n{'─'*60}{C.RESET}")



# ── Test edilecek hedefler ─────────────────────────────────────────

TARGETS = [

    # Office Store / Catalog

    {"name": "Office Store Ana Sunucu",         "host": "store.office.com",              "port": 443},

    {"name": "Office CDN (officeapps)",          "host": "officeapps.live.com",           "port": 443},

    {"name": "Office Add-in Manifest CDN",       "host": "appsforoffice.microsoft.com",   "port": 443},

    {"name": "Microsoft Login",                  "host": "login.microsoftonline.com",     "port": 443},

    {"name": "Azure AD Auth",                    "host": "login.live.com",               "port": 443},

    {"name": "Office 365 API",                   "host": "outlook.office365.com",         "port": 443},

    {"name": "Graph API",                        "host": "graph.microsoft.com",           "port": 443},

    {"name": "Excel Add-in Catalog",             "host": "pages.store.office.com",        "port": 443},

    {"name": "Claude/Anthropic CDN",             "host": "api.anthropic.com",             "port": 443},

    {"name": "Office Telemetry",                 "host": "nexus.officeapps.live.com",     "port": 443},

    # Genel internet

    {"name": "Google DNS (kontrol)",             "host": "8.8.8.8",                      "port": 53},

    {"name": "Cloudflare DNS (kontrol)",         "host": "1.1.1.1",                      "port": 53},

]



MANIFEST_URLS = [

    "https://store.office.com/en-US/addinsinstallpage.aspx",

    "https://pages.store.office.com/addinsinstallpage.aspx?rs=en-US&assetid=WA200009404&isWac=True&ui=en-US&ad=US",

    "https://appsforoffice.microsoft.com/lib/1/hosted/office.js",

]



# ══════════════════════════════════════════════════════════════════

# TEST FONKSİYONLARI

# ══════════════════════════════════════════════════════════════════



def test_dns(host: str) -> dict:

    """DNS çözümleme testi."""

    result = {"test": "dns", "host": host, "status": None, "ip": None,

              "latency_ms": None, "error": None}

    try:

        t0 = time.monotonic()

        ip = socket.gethostbyname(host)

        latency = round((time.monotonic() - t0) * 1000, 2)

        result.update(status="ok", ip=ip, latency_ms=latency)

    except socket.gaierror as e:

        result.update(status="fail", error=str(e))

    return result





def test_tcp(host: str, port: int, timeout: float = 5.0) -> dict:

    """TCP bağlantı testi."""

    result = {"test": "tcp", "host": host, "port": port,

              "status": None, "latency_ms": None, "error": None}

    try:

        t0 = time.monotonic()

        with socket.create_connection((host, port), timeout=timeout):

            latency = round((time.monotonic() - t0) * 1000, 2)

        result.update(status="ok", latency_ms=latency)

    except (socket.timeout, ConnectionRefusedError, OSError) as e:

        result.update(status="fail", error=str(e))

    return result





def test_ssl(host: str, port: int = 443, timeout: float = 7.0) -> dict:

    """SSL/TLS sertifika doğrulama testi."""

    result = {"test": "ssl", "host": host, "port": port,

              "status": None, "issuer": None, "expiry": None,

              "days_left": None, "error": None}

    try:

        ctx = ssl.create_default_context()

        t0 = time.monotonic()

        with socket.create_connection((host, port), timeout=timeout) as sock:

            with ctx.wrap_socket(sock, server_hostname=host) as ssock:

                cert = ssock.getpeercert()

        latency = round((time.monotonic() - t0) * 1000, 2)

        issuer = dict(x[0] for x in cert.get("issuer", []))

        expiry_str = cert.get("notAfter", "")

        if expiry_str:

            expiry_dt = datetime.datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z")

            days_left = (expiry_dt - datetime.datetime.utcnow()).days

        else:

            days_left = None

        result.update(

            status="ok",

            issuer=issuer.get("organizationName", "?"),

            expiry=expiry_str,

            days_left=days_left,

            latency_ms=latency

        )

    except ssl.SSLCertVerificationError as e:

        result.update(status="ssl_fail", error=f"Sertifika doğrulama hatası: {e}")

    except Exception as e:

        result.update(status="fail", error=str(e))

    return result





def test_http(url: str, timeout: float = 10.0) -> dict:

    """HTTP/HTTPS yanıt kodu ve gecikme testi."""

    result = {"test": "http", "url": url, "status": None,

              "http_code": None, "latency_ms": None, "error": None,

              "redirect": None}

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (DiagTool/1.0)"})

    try:

        t0 = time.monotonic()

        with urllib.request.urlopen(req, timeout=timeout) as resp:

            latency = round((time.monotonic() - t0) * 1000, 2)

            result.update(

                status="ok",

                http_code=resp.status,

                latency_ms=latency,

                redirect=resp.url if resp.url != url else None

            )

    except urllib.error.HTTPError as e:

        result.update(status="http_error", http_code=e.code, error=str(e))

    except urllib.error.URLError as e:

        result.update(status="fail", error=str(e.reason))

    except Exception as e:

        result.update(status="fail", error=str(e))

    return result





def test_proxy() -> dict:

    """Sistem proxy ayarlarını tespit et."""

    result = {"test": "proxy", "env_http": None, "env_https": None,

              "env_no_proxy": None, "system_proxy": None}

    result["env_http"]    = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")

    result["env_https"]   = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")

    result["env_no_proxy"]= os.environ.get("NO_PROXY") or os.environ.get("no_proxy")

    # urllib sistem proxy algılama

    try:

        proxies = urllib.request.getproxies()

        result["system_proxy"] = proxies if proxies else None

    except Exception:

        pass

    return result





def test_registry_office() -> dict:

    """Windows kayıt defterinde Office Trust Center ayarlarını oku."""

    result = {"test": "registry", "platform": platform.system(),

              "status": None, "data": {}, "error": None}

    if platform.system() != "Windows":

        result.update(status="skip", error="Windows değil")

        return result

    try:

        import winreg

        paths = [

            r"SOFTWARE\Microsoft\Office\16.0\WEF\TrustedCatalogs",

            r"SOFTWARE\Microsoft\Office\15.0\WEF\TrustedCatalogs",

            r"SOFTWARE\Policies\Microsoft\Office\16.0\WEF",

        ]

        found = {}

        for path in paths:

            try:

                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)

                i = 0

                while True:

                    try:

                        subname = winreg.EnumKey(key, i)

                        subkey  = winreg.OpenKey(key, subname)

                        vals = {}

                        j = 0

                        while True:

                            try:

                                n, v, _ = winreg.EnumValue(subkey, j)

                                vals[n] = v

                                j += 1

                            except OSError:

                                break

                        found[f"{path}\\{subname}"] = vals

                        i += 1

                    except OSError:

                        break

                winreg.CloseKey(key)

            except FileNotFoundError:

                found[path] = "Bulunamadı"

        result.update(status="ok", data=found)

    except ImportError:

        result.update(status="fail", error="winreg modülü yüklenemedi")

    except Exception as e:

        result.update(status="fail", error=str(e))

    return result





def test_firewall_ping(host: str) -> dict:

    """ICMP ping ile erişilebilirlik testi."""

    result = {"test": "ping", "host": host, "status": None, "output": None}

    try:

        flag = "-n" if platform.system() == "Windows" else "-c"

        cmd  = ["ping", flag, "3", host]

        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

        output = proc.stdout + proc.stderr

        if proc.returncode == 0:

            result.update(status="ok", output=output.strip()[:300])

        else:

            result.update(status="fail", output=output.strip()[:300])

    except subprocess.TimeoutExpired:

        result.update(status="timeout", output="Ping zaman aşımına uğradı")

    except Exception as e:

        result.update(status="error", output=str(e))

    return result





def test_traceroute(host: str) -> dict:

    """Traceroute ile ağ yolu analizi."""

    result = {"test": "traceroute", "host": host, "status": None, "hops": None}

    try:

        if platform.system() == "Windows":

            cmd = ["tracert", "-h", "15", "-w", "1000", host]

        else:

            cmd = ["traceroute", "-m", "15", "-w", "2", host]

        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        output = proc.stdout[:1500]

        result.update(status="ok" if proc.returncode == 0 else "partial", hops=output)

    except subprocess.TimeoutExpired:

        result.update(status="timeout", hops="Zaman aşımı")

    except FileNotFoundError:

        result.update(status="skip", hops="traceroute komutu bulunamadı")

    except Exception as e:

        result.update(status="error", hops=str(e))

    return result





# ══════════════════════════════════════════════════════════════════

# RAPOR ÜRETİCİ

# ══════════════════════════════════════════════════════════════════



def generate_html_report(all_results: dict, output_path: str):

    """Tüm sonuçlardan HTML raporu üret."""



    def badge(status):

        colors = {"ok": "#22c55e", "fail": "#ef4444", "warn": "#f59e0b",

                  "skip": "#6b7280", "partial": "#f59e0b",

                  "ssl_fail": "#ef4444", "http_error": "#f59e0b",

                  "timeout": "#ef4444", "error": "#ef4444"}

        labels = {"ok": "OK", "fail": "HATA", "warn": "UYARI",

                  "skip": "ATLA", "partial": "KISMİ",

                  "ssl_fail": "SSL HATA", "http_error": "HTTP HATA",

                  "timeout": "ZAMAN AŞIMI", "error": "HATA"}

        c = colors.get(status, "#6b7280")

        l = labels.get(status, status.upper() if status else "?")

        return f'<span style="background:{c};color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700">{l}</span>'



    def rows_from_list(items, keys):

        html = ""

        for item in items:

            html += "<tr>"

            for k in keys:

                v = item.get(k, "")

                if k == "status":

                    html += f"<td>{badge(str(v) if v else 'fail')}</td>"

                elif v is None:

                    html += "<td>—</td>"

                else:

                    html += f"<td>{v}</td>"

            html += "</tr>"

        return html



    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sys_info = all_results.get("system", {})



    # İstatistik hesapla

    dns_results  = all_results.get("dns", [])

    tcp_results  = all_results.get("tcp", [])

    ssl_results  = all_results.get("ssl", [])

    http_results = all_results.get("http", [])



    total = len(dns_results) + len(tcp_results) + len(ssl_results) + len(http_results)

    fails = sum(1 for r in dns_results+tcp_results+ssl_results+http_results

                if r.get("status") not in ("ok", "skip"))

    score = round((total - fails) / max(total, 1) * 100)

    score_color = "#22c55e" if score >= 80 else "#f59e0b" if score >= 50 else "#ef4444"



    proxy = all_results.get("proxy", {})

    proxy_html = ""

    for k, v in proxy.items():

        if k == "test":

            continue

        proxy_html += f"<tr><td>{k}</td><td>{v if v else '—'}</td></tr>"



    reg = all_results.get("registry", {})

    reg_data = reg.get("data", {})

    reg_html = ""

    if isinstance(reg_data, dict):

        for path, vals in reg_data.items():

            if isinstance(vals, dict):

                for n, v in vals.items():

                    reg_html += f"<tr><td style='font-size:11px'>{path}</td><td>{n}</td><td>{v}</td></tr>"

            else:

                reg_html += f"<tr><td colspan='2' style='font-size:11px'>{path}</td><td>{vals}</td></tr>"



    ping_results = all_results.get("ping", [])

    ping_html = ""

    for p in ping_results:

        st = badge(p.get("status", "fail"))

        ping_html += f"<tr><td>{p.get('host')}</td><td>{st}</td><td><pre style='margin:0;font-size:10px;white-space:pre-wrap'>{p.get('output','—')[:200]}</pre></td></tr>"



    tr_result = all_results.get("traceroute", {})

    tr_html = f"<pre style='background:#1e293b;color:#94a3b8;padding:12px;border-radius:6px;font-size:11px;overflow-x:auto'>{tr_result.get('hops','—')}</pre>"



    html = f"""<!DOCTYPE html>

<html lang="tr">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Excel Add-in Diagnostics Raporu</title>

<style>

  *{{box-sizing:border-box;margin:0;padding:0}}

  body{{font-family:'Segoe UI',system-ui,sans-serif;background:#0f172a;color:#e2e8f0;min-height:100vh;padding:32px 24px}}

  h1{{font-size:22px;font-weight:700;letter-spacing:-0.5px}}

  h2{{font-size:14px;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:1px;margin:32px 0 12px}}

  .header{{display:flex;align-items:center;gap:16px;margin-bottom:32px;padding-bottom:24px;border-bottom:1px solid #1e293b}}

  .logo{{width:42px;height:42px;background:#ef4444;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:22px}}

  .score-card{{background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid #334155;border-radius:16px;padding:24px;margin-bottom:24px;display:flex;align-items:center;gap:24px}}

  .score-circle{{width:90px;height:90px;border-radius:50%;border:4px solid {score_color};display:flex;flex-direction:column;align-items:center;justify-content:center;flex-shrink:0}}

  .score-num{{font-size:28px;font-weight:800;color:{score_color}}}

  .score-label{{font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:1px}}

  .sysinfo{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px;margin-bottom:24px}}

  .syscard{{background:#1e293b;border-radius:10px;padding:14px}}

  .syscard-label{{font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:4px}}

  .syscard-val{{font-size:13px;font-weight:600;color:#e2e8f0}}

  table{{width:100%;border-collapse:collapse;background:#1e293b;border-radius:10px;overflow:hidden;margin-bottom:20px}}

  th{{background:#0f172a;padding:10px 14px;text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:0.8px;color:#64748b}}

  td{{padding:10px 14px;font-size:12px;border-bottom:1px solid #0f172a;vertical-align:top}}

  tr:last-child td{{border-bottom:none}}

  tr:hover td{{background:#0f172a30}}

  .summary-box{{background:#1e293b;border-left:3px solid {score_color};border-radius:0 8px 8px 0;padding:14px 18px;margin-bottom:12px}}

  .ts{{color:#475569;font-size:12px}}

  @media(max-width:600px){{.score-card{{flex-direction:column}}}}

</style>

</head>

<body>

<div class="header">

  <div class="logo">⚙</div>

  <div>

    <h1>Excel Add-in Diagnostics</h1>

    <div class="ts">Oluşturulma: {ts} — {sys_info.get('platform','?')}</div>

  </div>

</div>



<div class="score-card">

  <div class="score-circle">

    <div class="score-num">{score}%</div>

    <div class="score-label">Sağlık</div>

  </div>

  <div>

    <div style="font-size:18px;font-weight:700;margin-bottom:6px">

      {'🟢 Bağlantı Sağlıklı' if score >= 80 else '🟡 Kısmi Sorun' if score >= 50 else '🔴 Kritik Bağlantı Sorunu'}

    </div>

    <div style="color:#94a3b8;font-size:13px">

      Toplam {total} test · {fails} hata tespit edildi

    </div>

    <div style="color:#64748b;font-size:12px;margin-top:6px">

      Hedef: Office Store / Add-in Catalog bağlantı doğrulaması

    </div>

  </div>

</div>



<div class="sysinfo">

  <div class="syscard"><div class="syscard-label">İşletim Sistemi</div><div class="syscard-val">{sys_info.get('platform','?')}</div></div>

  <div class="syscard"><div class="syscard-label">Python</div><div class="syscard-val">{sys_info.get('python','?')}</div></div>

  <div class="syscard"><div class="syscard-label">Hostname</div><div class="syscard-val">{sys_info.get('hostname','?')}</div></div>

  <div class="syscard"><div class="syscard-label">Yerel IP</div><div class="syscard-val">{sys_info.get('local_ip','?')}</div></div>

</div>



<h2>🌐 DNS Çözümleme</h2>

<table>

  <tr><th>Hedef</th><th>Durum</th><th>IP Adresi</th><th>Gecikme (ms)</th><th>Hata</th></tr>

  {rows_from_list(dns_results, ['host','status','ip','latency_ms','error'])}

</table>



<h2>🔌 TCP Bağlantı</h2>

<table>

  <tr><th>Hedef</th><th>Port</th><th>Durum</th><th>Gecikme (ms)</th><th>Hata</th></tr>

  {rows_from_list(tcp_results, ['host','port','status','latency_ms','error'])}

</table>



<h2>🔒 SSL/TLS Sertifika</h2>

<table>

  <tr><th>Hedef</th><th>Durum</th><th>Yayıncı</th><th>Son Geçerlilik</th><th>Kalan Gün</th><th>Hata</th></tr>

  {rows_from_list(ssl_results, ['host','status','issuer','expiry','days_left','error'])}

</table>



<h2>🌍 HTTP/HTTPS Yanıt</h2>

<table>

  <tr><th>URL</th><th>Durum</th><th>HTTP Kodu</th><th>Gecikme (ms)</th><th>Yönlendirme</th><th>Hata</th></tr>

  {rows_from_list(http_results, ['url','status','http_code','latency_ms','redirect','error'])}

</table>



<h2>🛡️ Proxy Yapılandırması</h2>

<table>

  <tr><th>Ayar</th><th>Değer</th></tr>

  {proxy_html}

</table>



<h2>📌 Ping Testi</h2>

<table>

  <tr><th>Hedef</th><th>Durum</th><th>Çıktı</th></tr>

  {ping_html if ping_html else '<tr><td colspan="3">Ping testi çalıştırılmadı</td></tr>'}

</table>



<h2>🗂️ Windows Kayıt Defteri (Office Catalog)</h2>

{'<table><tr><th>Yol</th><th>Anahtar</th><th>Değer</th></tr>' + reg_html + '</table>'

 if reg_html else '<div class="summary-box">Windows dışı platform veya kayıt defteri bulunamadı.</div>'}



<h2>🛤️ Traceroute — pages.store.office.com</h2>

{tr_html}



<h2>📋 Tanı Özeti & Öneriler</h2>

<div style="display:grid;gap:10px">

  {'<div class="summary-box"><strong>🔴 DNS Sorunu:</strong> Bazı Office sunucuları çözümlenemiyor. DNS sunucunuzu 8.8.8.8 veya 1.1.1.1 olarak değiştirin.</div>' if any(r.get('status')=='fail' for r in dns_results) else ''}

  {'<div class="summary-box"><strong>🔴 TCP Bağlantı Engeli:</strong> 443 portuna bağlantı kurulamıyor. Güvenlik duvarı veya ağ politikası engel oluyor olabilir.</div>' if any(r.get('status')=='fail' for r in tcp_results) else ''}

  {'<div class="summary-box"><strong>🔴 SSL Sertifika Hatası:</strong> Sertifika doğrulanamıyor. Kurumsal SSL inspection (MITM proxy) aktif olabilir — BT ekibine danışın.</div>' if any(r.get('status')=='ssl_fail' for r in ssl_results) else ''}

  {'<div class="summary-box"><strong>🟡 HTTP Hataları:</strong> Bazı URL\'ler 4xx/5xx döndürüyor. Office Store bölge kısıtlaması olabilir.</div>' if any(r.get('status') in ('http_error','fail') for r in http_results) else ''}

  {'<div class="summary-box"><strong>🟡 Proxy Tespit Edildi:</strong> Sistem proxy aktif. Office eklentileri proxy üzerinden çalışmayabilir — bypass listesi ekleyin.</div>' if any(v for k,v in proxy.items() if k!='test' and v) else ''}

  <div class="summary-box" style="border-color:#22c55e"><strong>ℹ️ Genel Öneriler:</strong><br>

    1. Excel → Dosya → Seçenekler → Güven Merkezi → Güven Merkezi Ayarları → Güvenilen Kataloglar<br>

    2. Store URL: <code>https://store.office.com</code> ekleyip "Menüde Göster" işaretle<br>

    3. Group Policy ile engelleniyorsa: Computer Config → Administrative Templates → Microsoft Office → Security Settings → Block Web Add-ins<br>

    4. Ağ yöneticisinden <code>*.office.com, *.officeapps.live.com, *.microsoft.com</code> domainlerine izin vermesini isteyin

  </div>

</div>



<br><div style="color:#334155;font-size:11px;text-align:center">Excel Add-in Diagnostics Tool — Tüm haklar saklıdır</div>

</body>

</html>"""



    with open(output_path, "w", encoding="utf-8") as f:

        f.write(html)





# ══════════════════════════════════════════════════════════════════

# ANA AKIŞ

# ══════════════════════════════════════════════════════════════════



def main():

    print(f"""

{C.BOLD}╔══════════════════════════════════════════════════════╗

║    EXCEL ADD-IN DIAGNOSTICS  —  Tam Yetki Modu      ║

╚══════════════════════════════════════════════════════╝{C.RESET}

  Başlangıç: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

""")



    all_results = {

        "system": {

            "platform": platform.platform(),

            "python": sys.version.split()[0],

            "hostname": socket.gethostname(),

            "local_ip": None

        },

        "dns": [], "tcp": [], "ssl": [], "http": [],

        "proxy": {}, "registry": {}, "ping": [], "traceroute": {}

    }



    # Yerel IP

    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.connect(("8.8.8.8", 80))

        all_results["system"]["local_ip"] = s.getsockname()[0]

        s.close()

    except Exception:

        pass



    # ── DNS ──────────────────────────────────────────────────────

    hdr("1/7 — DNS Çözümleme Testi")

    for t in TARGETS:

        if ":" not in t["host"]:  # IP değil hostname ise

            r = test_dns(t["host"])

            all_results["dns"].append({"name": t["name"], **r})

            if r["status"] == "ok":

                ok(f"{t['name']:40s} → {r['ip']} ({r['latency_ms']} ms)")

            else:

                fail(f"{t['name']:40s} → {r['error']}")



    # ── TCP ──────────────────────────────────────────────────────

    hdr("2/7 — TCP Bağlantı Testi")

    for t in TARGETS:

        r = test_tcp(t["host"], t["port"])

        all_results["tcp"].append({"name": t["name"], **r})

        if r["status"] == "ok":

            ok(f"{t['name']:40s} :{t['port']} → {r['latency_ms']} ms")

        else:

            fail(f"{t['name']:40s} :{t['port']} → {r['error']}")



    # ── SSL ──────────────────────────────────────────────────────

    hdr("3/7 — SSL/TLS Sertifika Doğrulama")

    for t in TARGETS:

        if t["port"] == 443:

            r = test_ssl(t["host"])

            all_results["ssl"].append({"name": t["name"], **r})

            if r["status"] == "ok":

                days = r.get("days_left", "?")

                color = C.WARN if isinstance(days, int) and days < 30 else C.OK

                print(f"  {color}✓{C.RESET} {t['name']:40s} → {r['issuer']} | {days} gün kaldı")

            elif r["status"] == "ssl_fail":

                warn(f"{t['name']:40s} → {r['error']}")

            else:

                fail(f"{t['name']:40s} → {r['error']}")



    # ── HTTP ─────────────────────────────────────────────────────

    hdr("4/7 — HTTP/HTTPS Yanıt Kodu Testi")

    for url in MANIFEST_URLS:

        r = test_http(url)

        all_results["http"].append(r)

        short = url[:65] + "..." if len(url) > 65 else url

        if r["status"] == "ok":

            ok(f"[{r['http_code']}] {short} ({r['latency_ms']} ms)")

        elif r["status"] == "http_error":

            warn(f"[{r['http_code']}] {short}")

        else:

            fail(f"{short} → {r['error']}")



    # ── PROXY ────────────────────────────────────────────────────

    hdr("5/7 — Proxy Yapılandırması")

    proxy = test_proxy()

    all_results["proxy"] = proxy

    has_proxy = any(v for k, v in proxy.items() if k != "test" and v)

    if has_proxy:

        warn("Proxy tespit edildi:")

        for k, v in proxy.items():

            if k != "test" and v:

                print(f"    {k}: {v}")

    else:

        ok("Proxy yok — direkt bağlantı")



    # ── REGISTRY ─────────────────────────────────────────────────

    hdr("6/7 — Windows Kayıt Defteri (Office Trust Center)")

    reg = test_registry_office()

    all_results["registry"] = reg

    if reg["status"] == "skip":

        warn("Windows değil — atlandı")

    elif reg["status"] == "ok":

        if reg["data"]:

            ok(f"{len(reg['data'])} kayıt bulundu")

            for path in list(reg["data"].keys())[:3]:

                print(f"  {C.DIM}{path}{C.RESET}")

        else:

            warn("Kayıt defterinde Office katalog kaydı bulunamadı")

    else:

        fail(reg.get("error", "?"))



    # ── PING + TRACEROUTE ────────────────────────────────────────

    hdr("7/7 — Ping & Traceroute")

    ping_hosts = ["store.office.com", "8.8.8.8"]

    for h in ping_hosts:

        r = test_ping = test_firewall_ping(h)

        all_results["ping"].append(r)

        if r["status"] == "ok":

            ok(f"Ping {h}")

        else:

            warn(f"Ping başarısız: {h}")



    print(f"  {C.DIM}Traceroute çalıştırılıyor (pages.store.office.com)...{C.RESET}")

    tr = test_traceroute("pages.store.office.com")

    all_results["traceroute"] = tr



    # ── RAPOR OLUŞTUR ─────────────────────────────────────────────

    hdr("RAPORLAR OLUŞTURULUYOR")

    ts    = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    base  = f"excel_addin_diag_{ts}"

    json_path = f"{base}.json"

    html_path = f"{base}.html"



    with open(json_path, "w", encoding="utf-8") as f:

        json.dump(all_results, f, ensure_ascii=False, indent=2)

    ok(f"JSON raporu: {json_path}")



    generate_html_report(all_results, html_path)

    ok(f"HTML raporu: {html_path}")



    # ── ÖZET ──────────────────────────────────────────────────────

    dns_fail  = sum(1 for r in all_results["dns"]  if r.get("status") == "fail")

    tcp_fail  = sum(1 for r in all_results["tcp"]  if r.get("status") == "fail")

    ssl_fail  = sum(1 for r in all_results["ssl"]  if r.get("status") in ("fail","ssl_fail"))

    http_fail = sum(1 for r in all_results["http"] if r.get("status") not in ("ok","skip"))



    print(f"""

{C.BOLD}═══════════════════════ ÖZET ═══════════════════════{C.RESET}

  DNS  hataları : {dns_fail:2d} / {len(all_results['dns'])}

  TCP  hataları : {tcp_fail:2d} / {len(all_results['tcp'])}

  SSL  hataları : {ssl_fail:2d} / {len(all_results['ssl'])}

  HTTP hataları : {http_fail:2d} / {len(all_results['http'])}



  {"🔴 KRİTİK SORUN — Bağlantı engelleniyor" if (dns_fail+tcp_fail+ssl_fail)>3 else

   "🟡 KISMİ SORUN — Bazı servisler erişilemiyor" if (dns_fail+tcp_fail+ssl_fail)>0 else

   "🟢 BAĞLANTI SAĞLIKLI"}



  Raporlar: {json_path}  |  {html_path}

{C.BOLD}═══════════════════════════════════════════════════{C.RESET}

""")





if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\n\n  İptal edildi.")

    except Exception as e:

        print(f"\n{C.FAIL}BEKLENMEYEN HATA:{C.RESET} {e}")

        traceback.print_exc()