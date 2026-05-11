# E-posta Gönderme (SMTP) Referansı

## Gereksinim
- Gönderici: Gmail/Outlook hesabı
- **Gmail için**: "2 Adımlı Doğrulama" AÇIK + "Uygulama Şifresi" (16 haneli) gerekli
  - Ayarlar: https://myaccount.google.com/ → Güvenlik → 2 Adımlı Doğrulama → Uygulama Şifreleri
- Normal hesap şifresi SMTP'de çalışmaz (535 Authentication hatası)

## SMTP Sunucuları

| Sağlayıcı | Host | Port | Şifre Türü |
|-----------|------|------|------------|
| Gmail | smtp.gmail.com | 587 (STARTTLS) | Uygulama Şifresi |
| Outlook/Hotmail | smtp-mail.outlook.com | 587 (STARTTLS) | Uygulama Şifresi |

## Çalışan Kod

```python
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

def send_email_with_attachment(sender, app_password, recipient, subject, body, filepath):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    with open(filepath, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=filepath.split('/')[-1].split('\\')[-1])
        msg.attach(part)

    context = ssl.create_default_context()
    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
    server.starttls(context=context)
    server.login(sender, app_password)
    server.sendmail(sender, recipient, msg.as_string())
    server.quit()
```

## Normal Şifre Neden Çalışmaz
- Google/Microsoft modern güvenlik politikası gereği **SMTP AUTH için normal şifreyi reddeder**
- Gmail hatası: `535 5.7.8 Username and Password not accepted`
- Outlook hatası: `535 5.7.3 Authentication unsuccessful`
- Çözüm: App Password (Gmail) veya OAuth2 / Modern Auth (Outlook)
