---
name: cronjob-skill-guvenlik-denetimi
description: "Hermes Agent cronjob'larını ve skill'lerini güvenlik açısından denetleme, riskli cronjob'ları durdurma, bozuk/garbage skill'leri tespit edip silme, ransomware/fidye içerikli skill'leri analiz etme"
version: 1.0
category: devops
tags: [cronjob, security-audit, skill-cleanup, ransomware-scan, garbage-removal]
platforms: [windows]
---

# Cronjob ve Skill Güvenlik Denetimi

## Ne Zaman Kullanılır

- Kullanıcı "bilgisayarda kendi kendine çalışan bir şey var" derse
- Fidye/ransomware şüphesi olursa
- Skill listesi şiştiğinde ve bozuk skill'ler temizlenecekse
- Beklenmedik cronjob aktivitesi görüldüğünde
- Kullanıcı "dur/stopp" dediğinde tüm arkaplan işlemleri kontrol et

## Adım 1: Cronjob'ları Listele ve İncele

```
hermes cron list
```

ya da `cronjob(action='list')` tool'u ile.

**Riskli cronjob göstergeleri:**
- Çok sık çalışan (`*/5 * * * *` gibi)
- "super", "auto", "otonom", "gece" gibi isimler
- Açıklamasında "asla kullanıcıya sorma", "otomatik yap", "tüm işleri tespit et" gibi ifadeler
- Script çalıştıran cronjob'lar (`script` field'ı dolu olanlar)

## Adım 2: Riskli Cronjob'ları Durdur

Her cronjob için:
1. `cronjob(action='pause', job_id='...')` ile durdur
2. Gerekirse `cronjob(action='delete', job_id='...')` ile tamamen sil
3. Kullanıcıya hangilerinin durdurulduğunu bildir

## Adım 3: Bozuk/Garbage Skill'leri Tespit Et

Bozuk skill'ler genellikle John Hammond transcript kalıntılarıdır:

**Tespit kriterleri:**
- İsmi anlamsız transcript cümlesiyle başlıyorsa (`all-righty-`, `hey-everyone-`, `music-music-` gibi)
- Açıklaması kısaysa (15 karakterden az)
- İçeriği tekrarlayan transcript metniyse
- Kategorisi yoksa veya anlamsızsa

**Garbage prefix listesi (bu skill'ler genelde silinecek):**
```
all-righty, alrighty, and-, but-, dont-, hello-, hey-,
how-, ive-, just-, ladies-, lets-, like-, music-, the-, this-,
what-, when-, well-, you-, your-, yes-, can-chad-,
downloading-, everyone-, have-, there-, think-, want-,
whether-, years-, our-, computer-malware-, created-,
ed-ai, had-, david-bombal-, networkchuck-, got-any,
for-later, before-, bite-me, blood-hound, c2-, cairo-,
capturetheflag, consentfix, cool-this, cosmos-, ctf-,
data-pretty, debug-buttercup, deobfuscate, detect-malware,
detect-url, devcontainer-setup, dhcp-snooping,
disable-windows, effective-redteamer, encryption-ctf,
env-hide, exploit-, exposed-email, fake-claudebot,
few-days, fishing-email, forgot-press, fuzzing-,
gave-credit, gh-cli, golang-malware, good-morning,
google-bad, graph-spy, guidepoint-ctf, hacking-phone,
harris-heller, have-collection, have-handful, have-this,
hawaii-vacation, hows-going, hunt-ransomware,
incidentresponse, insecure-defaults, install-domain,
internal-network, internet-relay, interview-cybersecurity,
jeanna, kaido, kringle-con, kringlecon, kubernetes-,
linux-, local-admin, loki-c2, mal-, malicious-code,
malvertising, malware-, mcp-ccna, mcp-security,
microsoft-365, microsoft-recall, modern-python,
nmap-vpn, npm-wireshark, omg-cables, open-bullet,
password-, payload-, phishing-, php-weird,
playing-captured, plex-track, powershell-,
powerful-android, privilegeescalation, python-vpn,
qr-code, ransomware-, recover-malware, removeanti,
reverse-engineering, right-here, root-android,
seatbelt-sandboxer, semgrep-rule, setup-low-priv,
sharp-edges, so-couple, solana-, spec-to-code,
sqlinjection, substrate-, supplychain-,
suspicious-youtube, tabby-guide, take-ownership,
testing-handbook, token-integration, ton-vulnerability,
trailmark, trojan-, try-hack, typo-squatting,
vector-forge, vpn-, webshell-, windows-, wireshark,
years-ago, zeroize-audit, burpsuite-project-parser,
have-you-ever, well-hey, what-actually, what-secrets,
whats-everybody, whats-going, when-ethical, when-think,
when-was, when-you, wmd-, peing-, few-days-ago,
righty-, say-, someone-, sorry-, speak-, tend-,
there-are, think-ive, very-here, crypto-protocol-diagram
```

## Adım 4: Güvensiz Skill'leri Tara

```
search_files(pattern='(ransomware|encrypt.*file|shutil\\.rmtree|os\\.remove)', 
             path='~/AppData/Local/hermes/skills', file_glob='SKILL.md', limit=20)
```

**Aranacak riskli pattern'ler:**
- `ransomware`, `ransom`, `fidye` — bilgi amaçlıysa sorun yok
- `encrypt`, `decrypt` + `file` — şifreleme kodu içerebilir
- `os.remove`, `os.unlink`, `shutil.rmtree` — dosya silme
- `subprocess.run`, `os.system` — sistem komutu çalıştırma
- `base64 decode`, `powershell -e` — obfuscated kod

**Önemli:** Bu skill'lerin çoğu eğitim/analiz amaçlıdır, çalıştırılabilir zararlı kod değildir. Panik yapmadan önce içeriği oku.

## Adım 5: Skill'leri Sil

### Yöntem 1: skill_manage tool'u (tek tek)
```
skill_manage(action='delete', name='skill-adi')
```

### Yöntem 2: Hermes CLI (bulunamazsa)
```
hermes curate
```
ya da direkt dizini sil:
```
rm -rf ~/AppData/Local/hermes/skills/bozuk-skill-adi
```

## Adım 6: Kullanıcı Güvenlik Politikası — Otonom Cronjob'lar

Bu oturumda kullanıcı şu kuralı netleştirdi:
> **"Bilgisayarda kendi kendine karar veren hiçbir uygulama olmasın. Dosya gönderimi yok, dışarı test yok, onay almadan hiçbir şey yapılmasın."**

**Uygulama prensipleri:**
1. Tüm cronjob'lar başlangıçta PAUSED durumda olmalı — kullanıcı istemedikçe aktif edilmez
2. `super-yonetici` tarzı "asla kullanıcıya sorma" script'leri doğrudan silinir, durdurulmaz
3. Güvenlik izleme script'leri sadece RAPOR eder, asla müdahale etmez
4. Şüpheli aktivite (WiFi tarama, port dinleme, dosya şifreleme) tespit edilirse kullanıcıya bildir, kendi kendine çözme
5. Kullanıcı onayı olmadan dışarıya veri gönderen (API call, webhook, GitHub push) hiçbir cronjob çalıştırılmaz

## Notlar

- Bozuk skill'ler fiziksel dosya olarak var olmayabilir (GitHub import), sadece skills listesinde görünür
- Silme işlemi başarısız olursa `skill_manage(action='delete')` dene
- `hermes skills uninstall` CLI onay ister (`--yolo` onayı geçemez), onun yerine `skill_manage(action='delete')` tool'unu kullan
- Kullanıcıya her adımda ne yapıldığını bildir (sayılarla: "X/Y skill silindi")
- Cronjob'ları durdururken kullanıcıya hangilerinin durduğunu ve nedenini açıkla
- Bu skill'i kullanırken cronjob listesini ve skills listesini her zaman ilk adımda al
- Garbage skill tespitinde **aşırı agresif olma** — `windows-allow-once-otomatik` gibi geçerli skill'leri yanlışlıkla silme. Her silme öncesi skill'in içeriğini kontrol et.
- Toplu silme için referans: `references/batch-skill-deletion.md`
- Pasif güvenlik izleme kurulumu: `references/passive-security-monitoring.md`
