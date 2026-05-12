# n8n Şifre Sıfırlama

## Ne Zaman
Kullanıcı login olamıyor, "Wrong username or password" hatası alıyor.

## Prosedür

1. **n8n'i durdur**
   - PID bul: `tasklist | findstr node`
   - Durdur: `taskkill //F //PID <PID>`

2. **Kullanıcıyı bul**
   ```bash
   sqlite3 ~/.n8n/database.sqlite "SELECT id, email, firstName, lastName FROM user;"
   ```

3. **Bcrypt hash oluştur** (n8n'in kendi modülü ile)
   ```bash
   cd /c/Users/eymen/AppData/Roaming/npm/node_modules/n8n
   HASH=$(node -e "const bcrypt = require('bcryptjs'); console.log(bcrypt.hashSync('123456', 10));")
   ```

4. **Veritabanına yaz**
   ```bash
   sqlite3 /c/Users/eymen/.n8n/database.sqlite "UPDATE user SET password='$HASH' WHERE email='markopasa_@hotmail.com';"
   ```

5. **n8n'i başlat**: `n8n start &`

## Önemli
- `bcrypt` Python paketi değil, n8n'in node_modules'undeki `bcryptjs` kullanılır
- Hash her seferinde farklı olur, bu normal — bcrypt salt üretir
- Şifre varsayılan: `123456`
