CRONJOBS: 08:15 genel ozet(son dakika+X15+TR20+Dunya25), 08:30 Istanbul, 09:00 Kayseri. Her 20dk ekonomi takip (altin/gumus/doviz yon analizi). Hepsi Telegram'a. Teslimat: all (bu sohbet + Telegram). hermes-gunluk-yedek: 20:00 (güncellendi, eski 23:00).
§
Hermes yedek repo: asdafgf/hermes-beckup (private). ~/.hermes/ tam yedek — config, skills, cron, .env, auth.json. .gitignore'da sessions/, logs/, cache/, state.db* hariç. Günlük cron: 23:00. Geri yükleme: git clone https://github.com/asdafgf/hermes-beckup.git hermes
§
WSL Allow Once çözümü: skill devops/wsl-allow-once-cozumu. Windows Firewall'dan wsl.exe'ye kalıcı izin ver. Hata cozum dongusu: Claude sorun anlat => kod al => calistir => hata varsa Claude'a geri ver. WSL Docker: skill devops/wsl-docker-kurulum (10 adım). Supabase start hatası: npx supabase start WSL Docker'ı görmez, DOCKER_HOST ayarla gerekebilir.
§
Eymen | Turkce | Istanbul+Kayseri | Erciyes/Win11
Tercihler:
- Kisa, ozlu, madde madde Turkce cevap, sormadan islem yap
- Hata cozum dongusu: Claude sorun anlat => kod al => calistir => hata varsa Claude'a geri ver
- Allow Once sorma, kalici cozum uygula
- Admin/UAC sorunlarinda WSL tabanli cozum tercih et
Projeler: KiraLog (Expo/RN, local Supabase calisiyor, migration duzeltildi), n8n guvenlik kamerasi
§
KiraLog checkpoint 2026-05-12: Docker WSL Ubuntu v29.4.3, 12 container. local Supabase calisiyor (Studio 54323, REST 54321). 9/9 Edge Functions calisiyor flat dir+symlink ile. Web build 1350 module 0 hata. GitHub asdafgf/kiralog "FAZ 1 MVP". OTP test edilmedi, sequential_pipeline calistirilmadi. Cloud deploy 2FA+limit bekliyor. Devam: OTP test, pipeline run, deploy.
§
Android gelistirme ortami kurulumu tamam (May 12): JDK 21 LTS, Gradle 9.5.0, Android SDK 34/35/36, Build Tools 34/35/36, ADB, Android Studio Panda 4. ANDROID_HOME env ayarlandi. Expo/RN projeleri icin hazir.
§
Hermes terminal tool patchi (May 14): local.py'ye _close_pipes + Windows CTRL_BREAK_EVENT + creationflags eklendi. C:\Users\eymen\AppData\Local\hermes\hermes-agent\tools\environments\local.py. Hermes güncellemesinde sıfırlanabilir — skill devops/windows-terminal-hata-cozumu'ndan geri yüklenebilir.