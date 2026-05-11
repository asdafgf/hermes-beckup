"""
Tesseract + Akilli Parse ile Gorselden Tablo Okuma + Dogrulama
Kullanim: python tesseract_tablo_oku.py <gorsel_yolu>

BILINEN_SISTEMLER listesini tablodaki sistemlere gore guncellemeyi unutma.
"""
import os, re, sys
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import pandas as pd
from PIL import Image
import pytesseract

# Tesseract binary yolunu ayarla
tess_path = r"C:\Users\eymen\scoop\apps\tesseract\current\tesseract.exe"
if os.path.exists(tess_path):
    pytesseract.pytesseract.tesseract_cmd = tess_path

# Tablodaki sistem adlari (gorseldeki tabloya gore guncelle)
BILINEN_SISTEMLER = [
    "ELEKTRIK", "PERVANE", "MOTOR", "UCAK LASTIGI", "YDT",
    "LASTIK KOMPOZIT", "INIS TAKIMI", "GOVDE", "BORDA", "ELEKTRONIK",
    "YAKIT", "BORU HORTUM", "KLIMA", "GYRO", "HIDROLIK",
    "PARASUT", "HAM MALZEME", "AVIYONIK", "BARIYER", "KUMANDA",
    "RADAR", "YSC", "DIGER"
]

def tesseract_oku(gorsel_yolu):
    """Tesseract ile gorseli oku"""
    if not os.path.exists(gorsel_yolu):
        print(f"HATA: Dosya bulunamadi: {gorsel_yolu}")
        sys.exit(1)
    img = Image.open(gorsel_yolu)
    metin = pytesseract.image_to_string(img, lang='tur+eng')
    return metin

def akilli_parse(metin):
    """Tesseract ciktisindan bilinen sistem adlarina gore veri cikar"""
    satirlar = metin.strip().split('\n')
    sistemler = {}
    toplamlar = []

    for satir in satirlar:
        satir = satir.strip()
        if not satir or len(satir) < 5:
            continue
        
        satir_upper = satir.upper()
        
        if satir_upper.startswith('TOPLAM') or 'TOPLAM' in satir_upper:
            sayilar = re.findall(r'\b\d{2,3}\b', satir)
            toplamlar = [int(s) for s in sayilar if 10 <= int(s) <= 200]
            continue
        
        bulunan_sistem = None
        for bilinen in BILINEN_SISTEMLER:
            ilk_kelime = bilinen.split()[0]
            if ilk_kelime in satir_upper:
                bulunan_sistem = bilinen
                break
        
        if bulunan_sistem:
            sayilar = re.findall(r'\b\d+\b', satir)
            degerler = [int(s) for s in sayilar if 0 <= int(s) <= 200]
            if len(degerler) >= 2:
                sistemler[bulunan_sistem] = degerler[:5]

    return sistemler, toplamlar

def dogrula(sistemler, toplamlar, yillar=[2022,2023,2024,2025,2026]):
    """pandas ile dogrulama"""
    if not sistemler:
        print("\n❌ HIC SISTEM BULUNAMADI")
        return None
    
    max_col = max(len(v) for v in sistemler.values())
    for ad in sistemler:
        while len(sistemler[ad]) < max_col:
            sistemler[ad].append(0)
    
    df = pd.DataFrame.from_dict(sistemler, orient='index', columns=yillar[:max_col])
    df = df.sort_index()
    
    print(f"\n  BULUNAN SISTEM: {df.shape[0]}/{len(BILINEN_SISTEMLER)}")
    print(df.to_string())
    
    print(f"\n=== YIL TOPLAMLARI ===")
    hesaplanan = df[yillar[:max_col]].sum().values
    for i, y in enumerate(yillar[:len(hesaplanan)]):
        h = int(hesaplanan[i])
        if i < len(toplamlar):
            b = toplamlar[i]
            fark = h - b
            durum = "✅" if fark == 0 else "❌"
            print(f"  {y}: H={h} B={b} {durum} (fark: {fark})")
        else:
            print(f"  {y}: H={h}")
    
    eksik = set(BILINEN_SISTEMLER) - set(sistemler.keys())
    if eksik:
        print(f"\n⚠️ EKSIK SISTEMLER ({len(eksik)}): {', '.join(sorted(eksik))}")
    
    return df

if __name__ == "__main__":
    gorsel = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\eymen\AppData\Local\hermes\image_cache\img_ce23f3a5e742.jpg"
    
    print(f"Gorsel: {gorsel}")
    metin = tesseract_oku(gorsel)
    print("\n--- Tesseract Cikti ---")
    print(metin[:500])
    print("...")
    
    sistemler, toplamlar = akilli_parse(metin)
    df = dogrula(sistemler, toplamlar)
    print(f"\n  {len(sistemler)}/{len(BILINEN_SISTEMLER)} sistem bulundu, toplam: {toplamlar}")
