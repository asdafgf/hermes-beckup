# Passive Security Monitoring Cronjob — 14 May 2026

## Principle: REPORT ONLY, NO ACTION

This cronjob runs every 15 minutes and only reports suspicious activity to the user. It never takes action.

## What It Checks

1. **WiFi interface status** — is there an active WiFi connection? Any unexpected SSID?
2. **Suspicious listening ports** — 4444, 1337, 5555, 6666, 9999, 31337, 12345, 54321 (common C2/backdoor ports)
3. **Suspicious process names** — wireshark, airodump, nmap, mimikatz, procdump, psexec, netcat, beacon
4. **Unknown outbound connections** — established HTTPS connections to IPs not in the known allowlist

## Known Good IPs (Microsoft/Telegram/DeepSeek/Cloudflare)

```
149.154.166.*  (Telegram)
20.190.*       (Microsoft)
13.107.*       (Microsoft)
40.99.*        (Microsoft)
52.168.*       (Microsoft)
192.178.*      (Google)
4.208.*        (DeepSeek)
4.231.*        (DeepSeek)
34.149.*       (Google)
150.171.*      (Microsoft)
74.242.*       (Microsoft)
160.79.*       (Microsoft)
98.66.*        (Akamai)
85.153.*       (Telegram)
157.240.*      (Facebook/Meta)
```

## Cronjob Configuration

```bash
hermes cron create \
  --name guvenlik-izleme \
  --schedule "*/15 * * * *" \
  --script guvenlik_izle.py \
  --deliver origin \
  --no-agent
```

## Script Location

`~/.hermes/scripts/guvenlik_izle.py` — uses only `netsh`, `netstat`, and `tasklist`. No elevated privileges needed (netsh wlan requires Location Services for SSID).
