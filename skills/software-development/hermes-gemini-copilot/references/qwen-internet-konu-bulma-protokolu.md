# İnternetten Konu Bul → Ollama'ya Sor → Skill Kaydet Döngüsü
# ===================================================================
# Bu protokol, 14 May 2026'daki Eymen oturumunda oluşturuldu.
# 
# Akış:
#   1. web_search("konu hakkında 2025 2026 en son teknikler")
#   2. web_search sonuçlarından 1 konu seç
#   3. Konuyu qwen_run() ile qwen2.5-coder'a sor
#   4. Yanıtı skill olarak kaydet (SKILL.md + references/qwen_yanit.txt)
#   5. Tekrar et (aynı konuyu 2 kere işleme)
#   6. 08:00'de dur, 08:10'da Telegram raporu
#
# Önemli:
#   - script/qwen_otonomegitim.sh bu iş için hazır shell scriptidir
#   - web_search sonuçlarını Hermes (ben) seçer, script'e parametre olarak geçer
#   - qwen_run() PTY gerektirmez, curl ile REST API kullanır
#   - Her konu ~2-5 dk sürer (qwen yanıt süresi)
#   - Kullanıcı hızlı geçiş ister → konular arası bekleme yok

# Kullanım:
#   cd ~/.hermes/scripts
#   bash qwen_otonomegitim.sh "KONU_BASLIGI" "ID" "KATEGORI" "PROMPT"
#
# Örnek:
#   bash qwen_otonomegitim.sh \
#     "Bettercap ile WiFi Ağ Keşfi" \
#     "WEB-001" \
#     "wifi" \
#     "Bettercap aracını kullanarak... 3-4 paragraf."

# Tuzaklar:
# 1. qwen_run içindeki Python JSON payload'da stream:false kullan
#    (stream:False değil — Python syntax'ında False, JSON'da false)
# 2. Ollama "Stopping..." deadlock'ı için önce qwen_fix_ollama() çağır
# 3. Background process notify_on_complete ile izle
