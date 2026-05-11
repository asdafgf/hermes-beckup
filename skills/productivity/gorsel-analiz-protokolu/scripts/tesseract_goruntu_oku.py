# Tesseract + Pandas ile Görsel Tablo Analizi
# Referans: Desktop\goruntu_analiz.py (çalışan versiyon)
# 
# Bu script:
# 1. Tesseract OCR ile görseldeki metni okur
# 2. Regex ile sistem adı + sayı çiftlerini parse eder
# 3. Pandas DataFrame'e çevirir
# 4. Yıl toplamlarını hesaplar ve bildirilenlerle karşılaştırır

import os, re
import pandas as pd
import numpy as np
from PIL import Image
import pytesseract

# === TESSERACT YAPILANDIRMASI ===
# Scoop ile kurulan Tesseract binary yolu
TESSERACT_CMD = r"C:\Users\eymen\scoop\apps\tesseract\current\tesseract.exe"
if os.path.exists(TESSERACT_CMD):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

# === OCR ===
def oku_goruntu(gorsel_yolu):
    """Görseldeki metni Tesseract ile oku"""
    img = Image.open(gorsel_yolu)
    metin = pytesseract.image_to_string(img, lang='tur+eng')
    return metin

# === PARSE ===
def parse_et(metin):
    """
    Tesseract ham çıktısından sistem adı + sayı çiftlerini çıkar.
    
    Beklenen format:
    ELEKTRIK 36 13 26 35 9
    TOPLAM 104 106 95 109 64
    
    Not: Tesseract bazen sayıları birleştirebilir veya harf olarak okuyabilir.
    Regex ile 2 basamaklı sayıları ayıklamak en güvenilir yöntemdir.
    """
    satirlar = metin.strip().split('\n')
    sistemler = {}
    toplam_satiri = None
    
    for satir in satirlar:
        satir = satir.strip()
        if not satir:
            continue
        
        # TOPLAM satırı
        if satir.upper().startswith('TOPLAM'):
            sayilar = re.findall(r'\d+', satir)
            if sayilar:
                toplam_satiri = [int(s) for s in sayilar]
            continue
        
        # Sistem satırı: SISTEM_ADI 36 13 26 35 9
        match = re.match(r'^([A-ZÇĞİÖŞÜ\s/]+)\s+([\d\s]+)$', satir)
        if match:
            ad = match.group(1).strip().rstrip(',.:;')
            sayi_metni = match.group(2).strip()
            sayilar = re.findall(r'\b\d+\b', sayi_metni)
            degerler = [int(s) for s in sayilar if int(s) < 500]
            if len(degerler) >= 3:
                sistemler[ad] = degerler[:5]
    
    return sistemler, toplam_satiri

# === DOĞRULAMA ===
def dogrula(sistemler, toplam_satiri, yillar=[2022,2023,2024,2025,2026]):
    """Pandas ile toplam doğrulaması yap"""
    if not sistemler:
        return None, "Hiç sistem bulunamadı"
    
    df = pd.DataFrame.from_dict(sistemler, orient='index', columns=yillar[:len(list(sistemler.values())[0])])
    
    sonuclar = []
    hesaplanan = df.sum().values
    
    if toplam_satiri and len(toplam_satiri) >= len(hesaplanan):
        for i, y in enumerate(yillar[:len(hesaplanan)]):
            h = int(hesaplanan[i])
            b = toplam_satiri[i] if i < len(toplam_satiri) else 0
            fark = h - b
            durum = "DOGRU" if fark == 0 else f"YANLIS (fark: {fark})"
            sonuclar.append(f"{y}: H={h} B={b} -> {durum}")
    
    return df, sonuclar

# === KULLANIM ===
if __name__ == "__main__":
    gorsel = r"C:\Users\eymen\AppData\Local\hermes\image_cache\img_ce23f3a5e742.jpg"
    metin = oku_goruntu(gorsel)
    print("--- Ham Metin ---")
    print(metin[:500])
    sistemler, toplam = parse_et(metin)
    df, sonuc = dogrula(sistemler, toplam)
    print("\n--- Dogrulama ---")
    if isinstance(sonuc, list):
        for s in sonuc:
            print(s)
