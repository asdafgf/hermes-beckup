# Manuel Tablo Doğrulama Aracı
# Referans: Desktop\tablo_dogrula_manuel.py
#
# Kullanıcı elle veri girer, program toplamları hesaplar ve doğrular.
# Kullanım:
#   python tablo_dogrula_manuel.py
#   Sistem verisi (veya BITIS): ELEKTRIK: 36,13,26,35,9
#   ...
#   BITIS
#   Bildirilen toplamlar: 104,106,95,109,64

# Örnek veri giriş formatı:
# ELEKTRIK: 36,13,26,35,9
# PERVANE: 0,6,17,16,6
# MOTOR: 4,20,5,14,11
# BITIS
# Bildirilen toplamlar: 104,106,95,109,64

# Çıktı:
# 2022: Hesaplanan=95, Bildirilen=104 -> YANLIS (Fark: -9)
# ...
# TUM DOGRULAMALAR BASARILI! veya BAZI DOGRULAMALAR BASARISIZ!

import re

def dogrula():
    sistemler = []
    isimler = []
    
    print("Sistem verilerini girin (SISTEM: V1,V2,V3,V4,V5)")
    print("BITIS yazarak bitirin.")
    
    while True:
        line = input("> ").strip().upper()
        if line == "BITIS":
            break
        match = re.match(r"^([A-Z]+):\s*([\d,]+)$", line)
        if match:
            degerler = [int(v.strip()) for v in match.group(2).split(',')]
            if len(degerler) == 5:
                sistemler.append(degerler)
                isimler.append(match.group(1))
    
    yillar = [2022, 2023, 2024, 2025, 2026]
    hesaplanan = [sum(s[i] for s in sistemler) for i in range(5)]
    
    print("\nHesaplanan:", hesaplanan)
    bildirilen_str = input("Bildirilen toplamlar (virgulle): ").strip()
    bildirilen = [int(v.strip()) for v in bildirilen_str.split(',')]
    
    for i, y in enumerate(yillar):
        fark = hesaplanan[i] - bildirilen[i]
        durum = "DOGRU" if fark == 0 else "YANLIS"
        print(f"{y}: H={hesaplanan[i]} B={bildirilen[i]} -> {durum} (fark: {fark})")

if __name__ == "__main__":
    dogrula()
