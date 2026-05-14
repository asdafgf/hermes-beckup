# Güvensiz Skill Tespit Referansı

## Riskli Keyword'ler ve Anlamları

| Keyword | Risk Seviyesi | Açıklama |
|---------|--------------|----------|
| `ransomware` | 🟡 Düşük | Genelde CTF/analiz skill'leri, bilgi amaçlı |
| `ransom` | 🟡 Düşük | Ransomware analiz rehberleri |
| `encrypt.*file` | 🟠 Orta | Şifreleme kodu içerebilir, içeriği oku |
| `shutil.rmtree` | 🔴 Yüksek | Dosya/dizin silebilir |
| `os.remove` | 🔴 Yüksek | Dosya silebilir |
| `os.unlink` | 🔴 Yüksek | Dosya silebilir |
| `subprocess.run` | 🟠 Orta | Sistem komutu çalıştırabilir |
| `os.system` | 🟠 Orta | Sistem komutu çalıştırabilir |
| `base64.decode` | 🟢 Bilgi | Genelde obfuscation çözme amaçlı |
| `powershell -e` | 🟠 Orta | Encoded PowerShell komutu |
| `fidye` | 🟢 Bilgi | Türkçe ransomware analizi |

## Gerçek Fidye mi, Eğitim mi?

**Eğitim amaçlı olduğunu gösteren işaretler:**
- İçeriğinde CTF, Hack The Box, TryHackMe referansı var
- "analiz", "rehber", "kılavuz" kelimeleri geçiyor
- YouTube video linki var (John Hammond, IppSec, NetworkChuck)
- Dosya şifreleme değil, dosya *analizi* anlatılıyor
- "sakın deneme", "eğitim amaçlıdır" uyarısı var

**Gerçek tehdit göstergeleri:**
- Skill içinde çalıştırılabilir Python/Bash kodu var ve otomatik çalışıyor
- Cronjob ile tetikleniyor
- Kullanıcıya sormadan dosya şifreleme/silme yapıyor
- Skill adı fidye yazılımı adlarına benziyor

## Hızlı Tarama Komutu

```bash
grep -rl "ransomware\|shutil.rmtree\|os.remove\|os.unlink\|encrypt.*file" ~/AppData/Local/hermes/skills/*/SKILL.md 2>/dev/null
```

Bu komut tüm SKILL.md dosyalarını tarar ve riskli içerik bulunanları listeler.
