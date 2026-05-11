"""
Gemini ile kod yazma ve sorgulama aracı
HTTP requests ile doğrudan Gemini API'ye bağlanır.
Kullanım: python gemini_araci.py soru "..." | python gemini_araci.py kod "..."
"""
import os
import sys
import json
import time
import requests

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

def get_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    key_file = os.path.expanduser("~/.gemini_api_key")
    if os.path.exists(key_file):
        with open(key_file) as f:
            return f.read().strip()
    print("\nGemini API anahtari gerekli.")
    print("Al: https://aistudio.google.com/apikey")
    key = input("API Anahtari: ").strip()
    if key:
        os.makedirs(os.path.dirname(key_file), exist_ok=True)
        with open(key_file, "w") as f:
            f.write(key)
        print("Anahtar kaydedildi")
    return key

def gemini_sor(prompt, model="gemini-2.5-flash"):
    key = get_api_key()
    if not key:
        return "[HATA] API anahtari gerekli"
    url = GEMINI_API_URL.format(model=model)
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    for deneme in range(3):
        try:
            r = requests.post(f"{url}?key={key}", json=payload, timeout=120)
            if r.status_code == 429:
                if deneme < 2:
                    time.sleep(5)
                    continue
                return "[HATA] Kota asildi (429)"
            r.raise_for_status()
            data = r.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
            return json.dumps(data, ensure_ascii=False)[:500]
        except requests.exceptions.RequestException as e:
            if deneme < 2:
                time.sleep(5)
                continue
            return f"[HATA] {e}"
    return "[HATA] Maksimum deneme"

def gemini_kod_yaz(gorev):
    prompt = f"""Gorev: {gorev}

Kurallar:
- Windows'ta calisacak Python kodu yaz
- Hata mesajlari Turkce olsun
- encoding='utf-8', errors='ignore' ekle
- Gerekiyorsa threading/concurrent.futures kullan
- Ana fonksiyon main() olsun
- Sadece kodu yaz, aciklama ekleme

Kod:"""
    return gemini_sor(prompt)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanim: python gemini_araci.py soru \"...\" | python gemini_araci.py kod \"...\"")
        sys.exit(1)
    komut = sys.argv[1]
    if komut == "soru":
        print(gemini_sor(" ".join(sys.argv[2:])))
    elif komut == "kod":
        print(gemini_kod_yaz(" ".join(sys.argv[2:])))
    elif komut == "api":
        print(f"Anahtar: {get_api_key()[:8]}...")
    else:
        print(f"Bilinmeyen komut: {komut}")
