# CDP Connection Troubleshooting - Eymen's Setup

## Environment
- OS: Windows 11 (Erciyes)
- Chrome: Scoop ile kurulu — `/c/Users/eymen/scoop/apps/googlechrome/148.0.7778.97/chrome.exe`
- Shell: git-bash (MSYS) üzerinden terminal çağrıları
- Python: Hermes venvi Anaconda'dan inherit ediyor

## Common Issues

### PATH karışıklığı — 'python' playwright'i görmüyor
- Hermes'in `python`'u venv'deki Python'a çözümlenir, Anaconda'daki paketleri görmez
- `pip show playwright` çalışır çünkü `pip` de Anaconda'ya çözümlenir ama `python -m playwright` venv Python'uyla çalışır
- **Çözüm**: Doğrudan `/c/Users/eymen/anaconda3/python.exe` ile çağır veya `python -c "import sys; print(sys.executable)` ile hangi Python olduğunu kontrol et

### Chrome başlıyor ama CDP portu açılmıyor
- Chrome zaten çalışıyorsa `--remote-debugging-port` flag'ini görmezden gelir
- Birden çok Chrome process'i olabilir (her biri farklı flag'lerle)
- **Çözüm**: `taskkill //F //IM chrome.exe` ile TÜM Chrome process'lerini öldür, sonra başlat

### Gemini sekmesi chrome://intro/ sayfasında kalıyor
- Chrome --new-window ile başlatıldığında URL yerine intro sayfası açılabilir
- **Çözüm 1**: URL'i doğrudan ver, --new-window kullanma
- **Çözüm 2**: CDP WebSocket ile Page.navigate yap

### Playwright type() çok yavaş
- delay=50 → 100 karakterde 5sn, timeout riski
- delay=20 optimal
- delay=5 hızlı ama React input bazen karakterleri kaçırabilir

## Verified Working Sequence
1. `taskkill //F //IM chrome.exe`
2. `sleep 3`
3. Chrome'u background=true ile başlat:
   - `"/c/Users/eymen/scoop/apps/googlechrome/148.0.7778.97/chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:/Users/eymen/AppData/Local/Google/Chrome/CDPProfile" "https://gemini.google.com/app"`
4. 10-15sn bekle (loop ile curl kontrol et)
5. Gemini sekmesi açılmadıysa CDP WebSocket ile navigate
6. `/c/Users/eymen/anaconda3/python.exe` ile Playwright script'ini çalıştır
