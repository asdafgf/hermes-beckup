#!/usr/bin/env python3
"""Guvenlik izleme scripti - sadece raporla, mudahale etme"""
import subprocess, json, os, socket

def check_wifi():
    """WiFi arayuzunu kontrol et"""
    r = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                       capture_output=True, text=True, timeout=10)
    if 'There is 1 interface' in r.stdout or 'There is 1 interface' in r.stderr:
        return "WiFi: Mevcut (lokasyon izni kapali)"
    if 'SSID' in r.stdout:
        lines = r.stdout.split('\n')
        ssid = [l for l in lines if 'SSID' in l or 'Profil' in l]
        return f"WiFi: {' | '.join(s.strip() for s in ssid[:3])}"
    return "WiFi: Yok veya erisilemez"

def check_suspicious_ports():
    """Supheli portlari kontrol et"""
    r = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, timeout=10)
    suspicious_ports = [4444, 1337, 5555, 6666, 9999, 31337, 12345, 54321]
    found = []
    for line in r.stdout.split('\n'):
        for port in suspicious_ports:
            if f':{port} ' in line and 'LISTENING' in line:
                found.append(f"Port {port}: {line.strip()}")
    return found

def check_suspicious_processes():
    """Supheli process adlarini kontrol et"""
    r = subprocess.run(['tasklist', '//FO', 'CSV'], capture_output=True, text=True, timeout=10)
    suspicious = ['tcpview', 'wireshark', 'airodump', 'nmap', 'mimikatz', 
                  'procdump', 'psexec', 'netcat', 'nc.exe', 'beacon']
    found = []
    for line in r.stdout.split('\n'):
        for s in suspicious:
            if s.lower() in line.lower():
                found.append(f"Suspicious process: {line.strip()}")
    return found

def check_unknown_connections():
    """Bilinmeyen IP baglantilarini kontrol et"""
    r = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, timeout=10)
    lines = r.stdout.split('\n')
    estab = [l.strip() for l in lines if 'ESTABLISHED' in l and '443' in l]
    return estab[:10]  # Ilk 10 tanesini goster

# Raporu olustur
report_parts = []

wifi_status = check_wifi()
report_parts.append(f"## WiFi Durumu\n{wifi_status}")

susp_ports = check_suspicious_ports()
if susp_ports:
    report_parts.append(f"## Supheli Port!\n" + "\n".join(susp_ports))
else:
    report_parts.append("## Port Tarama\nTum portlar guvenli. Supheli port yok.")

susp_procs = check_suspicious_processes()
if susp_procs:
    report_parts.append(f"## Supheli Process!\n" + "\n".join(susp_procs))
else:
    report_parts.append("## Processler\nSupheli process yok.")

# Aktif baglantilardan bilinmeyen IP'leri kontrol et
conns = check_unknown_connections()
known_ips = ['149.154.166', '20.190.', '13.107.', '40.99.', '52.168.', 
             '192.178.', '4.208.', '4.231.', '34.149.', '150.171.',
             '74.242.', '160.79.', '98.66.', '85.153.', '157.240.']
unknown = []
for c in conns:
    if not any(k in c for k in known_ips):
        unknown.append(c)

if unknown:
    report_parts.append(f"## Bilinmeyen Baglanti!\n" + "\n".join(unknown[:5]))

# Ozet
now = __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')
report = f"# Guvenlik Raporu - {now}\n\n" + "\n\n".join(report_parts)

print(report)
