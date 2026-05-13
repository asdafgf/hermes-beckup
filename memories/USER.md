**Name:**
§
Hata çözüm prensibi: 2 kez kendi dene, 3'te Gemini'ye bağlan → kod al → VS Code'a yapıştır → çalıştır → çıktıyı Gemini'ye ver → çözüm bulana kadar döngü. Otomatik, sormadan yap. Skill: hermes-gemini-copilot
§
Kullanıcı direkt adım numarasıyla atlar ("2" = adım 2'ye geç) — açıklama beklemez, sormadan yap.
§
Hermes ile Chrome Web Terminal/Gemini sohbet kontrolü istiyor. Çözüm: MCP server (Chrome CDP tabanlı). Eğer Chrome extension yüklenemezse, CDP (Chrome DevTools Protocol) ile doğrudan bağlanan MCP server kullanılır.
§
VS Code tercihi: yeni proje aç (File→Open Folder), Gemini kodunu yeni dosyaya yapıştır (Ctrl+N), kaydet (Ctrl+S), ardından VS Code'un ▶ Run (yeşil oynatma) butonuyla veya sağ tık→Run Python File ile çalıştır. Terminal çıktısını kendisi görmek ister. VS Code açık mı kontrol et, tekrar tekrar açma — açıksa kullan.