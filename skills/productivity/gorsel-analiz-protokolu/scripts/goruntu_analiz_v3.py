"""
GORUNTU ANALIZI v3 - Tesseract + Akilli Parse
En guvenilir otomatik goruntu okuma yontemi.
Referans: Desktop\goruntu_analiz_v3.py (calisan versiyon)

Kullanim:
  python goruntu_analiz_v3.py <gorsel_yolu>
  python goruntu_analiz_v3.py (default olarak son gorseli kullanir)
"""
import os, re, sys
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import pandas as pd
import numpy as np
from PIL import Image
import pytesseract

# Tesseract binary
tess_path = r"C:\Users\eymen\scoop\apps\tesseract\current\tesseract.exe"
if os.path.exists(tess_path):
    pytesseract.pytesseract.tesseract_cmd = tess_path

# Tablodaki sistem adlari (kullanici kendi tablosuna gore guncellesin)
BILINEN_SISTEMLER = [
    "ELEKTRIK", "PERVANE", "MOTOR", "UCAK LASTIGI", "YDT",
    "LASTIK KOMPOZIT", "INIS TAKIMI", "GOVDE", "BORDA", "ELEKTRONIK",
    "YAKIT", "BORU HORTUM", "KLIMA", "GYRO", "HIDROLIK",
    "PARASUT", "HAM MALZEME", "AVIYONIK", "BARIYER", "KUMANDA",
    "RADAR", "YSC", "DIGER"
]

# Hizli test icin en yaygin OCR hatalari -> dogru kelime eslemesi
OCR_ESLESME = {
    'ELEKTRİK': 'ELEKTRIK', 'ELEKTR': 'ELEKTRIK',
    'UÇAK': 'UCAK LASTIGI', 'UCAK': 'UCAK LASTIGI',
    'LASTİK': 'LASTIK KOMPOZIT', 'LASTIK': 'LASTIK KOMPOZIT',
    'İNİŞ': 'INIS TAKIMI', 'INIS': 'INIS TAKIMI',
    'GÖVDE': 'GOVDE',
    'ELEKTRONİK': 'ELEKTRONIK',
    'KLİMA': 'KLIMA',
    'HİDROLİK': 'HIDROLIK',
    'PARAŞÜT': 'PARASUT',
    'AVİYONİK': 'AVIYONIK',
    'BARİYER': 'BARIYER',
    'DİĞER': 'DIGER',
}

def tesseract_oku(gorsel_yolu):
    """PSM modlarini dene, en iyisini sec"""
    img = Image.open(gorsel_yolu)
    sonuclar = []
    for psm in [3, 4, 6]:
        metin = pytesseract.image_to_string(img, lang='tur+eng', config=f'--psm {psm}')
        sistem_sayisi = sum(1 for s in BILINEN_SISTEMLER if s.split()[0] in metin.upper())
        sonuclar.append((sistem_sayisi, metin, psm))
    sonuclar.sort(key=lambda x: -x[0])
    print(f"PSM secimi: {sonuclar[0][2]} ({sonuclar[0][0]}/{len(BILINEN_SISTEMLER)} sistem)")
    return sonuclar[0][1]

def akilli_parse(metin):
    """Bilinen sistem adlarina gore veri cikar"""
    satirlar = metin.strip().split('\n')
    sistemler = {}
    toplamlar = []
    for satir in satirlar:
        satir = satir.strip()
        if not satir or len(satir) < 4:
            continue
        satir_upper = satir.upper()
        if satir_upper.startswith('TOPLAM') or 'TOPLAM' in satir_upper:
            sayilar = re.findall(r'\b\d{2,3}\b', satir)
            toplamlar = [int(s) for s in sayilar if 10 <= int(s) <= 200]
            continue
        if 'YIL' in satir_upper or 'SILEN' in satir_upper:
            continue
        bulunan = None
        for bilinen in BILINEN_SISTEMLER:
            ilk_kelime = bilinen.split()[0]
            if ilk_kelime in satir_upper:
                bulunan = bilinen
                break
        if bulunan:
            sayilar = re.findall(r'\b\d+\b', satir)
            degerler = [int(s) for s in sayilar if 0 <= int(s) <= 200]
            if len(degerler) >= 2:
                sistemler[bulunan] = degerler[:5]
    return sistemler, toplamlar

def dogrula(sistemler, toplamlar, yillar=[2022,2023,2024,2025,2026]):
    if not sistemler:
        print("\n❌ HIC SISTEM BULUNAMADI")
        return None
    max_col = max(len(v) for v in sistemler.values())
    for ad in sistemler:
        while len(sistemler[ad]) < max_col:
            sistemler[ad].append(0)
    df = pd.DataFrame.from_dict(sistemler, orient='index', columns=yillar[:max_col])
    df = df.sort_index()
    print(f"\n  Sistem: {df.shape[0]}/{len(BILINEN_SISTEMLER)}")
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
        print(f"\n⚠️ Eksik ({len(eksik)}): {', '.join(sorted(eksik))}")
    return df

if __name__ == "__main__":
    gorsel = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\eymen\AppData\Local\hermes\image_cache\img_ce23f3a5e742.jpg"
    print(f"Gorsel: {gorsel}")
    metin = tesseract_oku(gorsel)
    print("\n--- Cikti ---")
    print(metin[:400])
    sistemler, toplamlar = akilli_parse(metin)
    df = dogrula(sistemler, toplamlar)
