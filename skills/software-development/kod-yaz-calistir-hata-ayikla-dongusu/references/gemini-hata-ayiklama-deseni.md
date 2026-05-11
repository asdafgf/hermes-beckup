# Gemini Hata Ayıklama Döngüsü (Error-Feedback Pattern)

Bu desen, Gemini'nin ürettiği kodu Claude ile aynı döngüye sokmak için kullanılır.

## Akış

1. Gemini'ye kod yazdır
2. Kaydet ve çalıştır
3. Hata varsa: hatayı al, Gemini'ye "Kod çalıştı ama şu sorun var: [hata]" şeklinde bildir
4. Gemini düzeltilmiş kodu üretir
5. Kaydet, çalıştır, doğru sonuç alana kadar tekrarla

## Önemli: Terminalde Çalıştıramayacak Kadar Uzun Prompt'lar

Gemini'ye uzun bir kod + hata mesajı göndermek için terminalde tek satırda yapılamaz (tırnak sorunları). Bunun yerine:

**Ayrı bir `.py` dosyası yaz ve çalıştır:**

```python
# gemini_duzelt.py
import requests, json, time, os

key = open(os.path.expanduser("~/.gemini_api_key")).read().strip()
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

code = open("mevcut_kod.py", encoding="utf-8").read()

prompt = "Kod calisti ama sorun var:\n\n"
prompt += "[sorunu anlat]\n\n"
prompt += "KOD:\n" + code + "\n\nDUZELTILMIS KOD:"

payload = {"contents": [{"parts": [{"text": prompt}]}]}

for d in range(3):
    r = requests.post(f"{url}?key={key}", json=payload, timeout=120)
    if r.status_code == 429:
        time.sleep(5)
        continue
    r.raise_for_status()
    data = r.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    if "```python" in text:
        text = text.split("```python")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    print(text.strip())
    break
```

Sonra çıktıyı al ve `write_file` ile kaydet.

## Gemini'nin Sık Yaptığı Hatalar (Düzeltme Listesi)

| Hata | Düzeltme |
|---|---|
| `ThreadPoolProcessor` | `ThreadPoolExecutor` |
| `encoding="cp857"` | `encoding="utf-8", errors="ignore"` |
| `ip_address.is_broadcast` | KALDIR (böyle bir özellik yok) |
| ping timeout 100ms | 300ms yap |
| VirtualBox IP'leri dahil | `is_virtualbox_ip()` fonksiyonu ekle |
| ARP'de "dinamik" regex | MAC regex'ini esnek yap: `[-:]` |
| Broadcast MAC filtreleme unutulur | hem `-` hem `:` formatında kontrol et |

## Referans: Başarılı Örnek

WiFi taraması görevi (bu session'da yapıldı):
- **Claude kodu:** 0 düzeltme, 5 cihaz buldu
- **Gemini kodu:** 4 düzeltme gerektirdi, 4 cihaz buldu
- **Claude → Gemini geçişi:** Claude API kotası dolarsa Gemini'ye geç, döngü aynen işler
