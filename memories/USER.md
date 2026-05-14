**Name:**
§
Ad: Eymen. Teknik, siber güvenlik meraklısı. Özellikle WiFi cihaz takibi, Android ekran izleme/takip, NFC relay saldırıları. Hata olunca direkt Gemini'ye bağlan, Python kod iste, çalıştır, çözüm bulana kadar döngü. Bekleme istemez — sayısal ilerleme (yüzde) ister. Adım numarası yazınca direkt o adıma atla, açıklama bekleme. "Ne bekliyorsun" = çok yavaşsın. PTY canlı çıktı tercih. Ollama bilir, Türkçe. VS Code: Ctrl+N, Ctrl+S, ▶ Run. Açıksa tekrar açma. Kendi numarasını sorgulatırken etik sınır konusunda rahat — "kendi verim neden suç olsun" der. Deneysel/gri alan sorgulamalara açık. Gece boyunca arkaplan oturumları sever (otonom, durmadan çalışan). Script hatalarına karşı sabırsız — hemen düzeltip yeniden başlat.
§
Kullanıcı direkt adım numarasıyla atlar ("2" = adım 2'ye geç) — açıklama beklemez, sormadan yap.
§
VS Code tercihi: yeni proje aç (File→Open Folder), Gemini kodunu yeni dosyaya yapıştır (Ctrl+N), kaydet (Ctrl+S), ardından VS Code'un ▶ Run (yeşil oynatma) butonuyla veya sağ tık→Run Python File ile çalıştır. Terminal çıktısını kendisi görmek ister. VS Code açık mı kontrol et, tekrar tekrar açma — açıksa kullan.
§
Prefers live PTY terminal sessions to see model responses streaming in real time — does not want just the final text result. Likes progress updates during downloads/uploads. Technical user familiar with Ollama model names and quantization formats. Native Turkish speaker.
§
Kullanici olasilik-oncelik-ilkesini tum islemlerde uygulamamizi istiyor: her olasilik denenmeli, hicbiri atlanmamali. Bu bir karar verme ilkesi olarak 1. sirada dusunulmeli.
§
User is deeply technical, security-focused, and likes full automation. Key preferences:
- "Bana sorma" (don't ask me) — execute decisions autonomously
- Wants Claude + Gemini both consulted for skill generation, best answer selected
- Prefers bulk/batch processing over interactive steps
- Interested in: Android hacking, mobile security, vulnerability research, malware analysis
- OK with fallback/transcript-only skills when APIs are unavailable (better than nothing)
- Frustrated by API quota limits (Gemini 429) — prefers OpenRouter as alternative
- Wants transcript→skill pipeline running continuously without supervision
- Values clean, meaningful skill names (complained about garbage names like "all-righty", "hey-everyone")
- Likes progress stats (% counts, batch numbers)
§
18:45 14 May — Fidye/fake ransomware endisesi. Super-yonetici cronjob'unu tehlikeli buldu. Kullanici kendi kendine calisan islemlerden rahatsizlik duyuyor, kontrolun kendinde olmasini istiyor. Beklenmedik cronjob aktivitesi ve skill sayisindaki sisirme onu endiselendiriyor. Direktif: cronjob'lari incele, riskli olanlari durdur, bozuk skill'leri sil.
§
User is Eymen — deeply technical, security-focused, Turkish speaker. Key preferences:
- **Güvenlik önceliği**: Bilgisayarda kendi kendine karar veren hiçbir otonom uygulama istemez (cronjob, WiFi saldırısı, dışarı dosya gönderimi). Onay almadan hiçbir şey yapılmamalı.
- **Sadece güvenli skill'ler çalıştırılır**: ransomware/fidye içeren veya anlamsız transcript kalıntısı skill'ler temizlenmeli.
- **Şüpheli aktivite izleme istiyor**: WiFi, port, process değişikliklerinde haberdar olmak istiyor, müdahale değil sadece bildirim.
- Avast virüs programı kullanıyor, güvenlik konusunda titiz.
- "Bana sorma", "bekleme", "adım numarası verince direkt atla" — hızlı ve otonom çalışma bekler, ama sadece kendisinin onayladığı işlerde.
- Anlamsız/garbage skill'lerden (John Hammond transcript kalıntıları) rahatsız oluyor, temizlenmesini istiyor.