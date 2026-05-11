# Word'den PowerPoint'e Dönüşüm Deseni

Word belgesini (`python-docx` ile) okuyup PowerPoint sunumuna (`python-pptx` ile) dönüştürme iş akışı.

## Kullanılan Kütüphaneler

- `python-docx` — Word okuma
- `python-pptx` — PowerPoint yazma

Her ikisi de Anaconda'da kurulu.

## Adımlar

### 1. Word belgesini oku ve yapıyı analiz et

Önce terminalden belgenin paragraflarını ve tablolarını dök:

```python
from docx import Document
doc = Document("dosya.docx")
print("=== PARAGRAPHS ===")
for i, p in enumerate(doc.paragraphs):
    if p.text.strip():
        print(f'P{i}: [{p.style.name}] {p.text[:200]}')
print("=== TABLES ===")
for ti, table in enumerate(doc.tables):
    print(f'Tablo {ti}: {len(table.rows)} satir x {len(table.columns)} kolon')
    for ri, row in enumerate(table.rows):
        cells = [cell.text.strip()[:40] for cell in row.cells]
        print(f'  Satir {ri}: {" | ".join(cells)}')
```

### 2. PowerPoint şablonu oluştur

Geniş ekran (13.333 x 7.5 inç) kullan. Masaüstü için ideal.

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
```

### 3. Renk paleti (Eymen'in sunumları için)

```python
MAVI_KOYU = RGBColor(0x1B, 0x3A, 0x5C)
MAVI_ACIK = RGBColor(0x2E, 0x86, 0xC1)
MAVI_CANLI = RGBColor(0x00, 0x96, 0xD6)
SARI = RGBColor(0xF3, 0x9C, 0x12)
YESIL = RGBColor(0x27, 0xAE, 0x60)
KIRMIZI = RGBColor(0xE7, 0x4C, 0x3C)
ACIK_MAVI = RGBColor(0xD6, 0xEA, 0xF8)
```

### 4. Yeniden kullanılabilir yardımcı fonksiyonlar

```python
def arkaplan_ekle(slide, renk):
    bg = slide.background; fill = bg.fill; fill.solid()
    fill.fore_color.rgb = renk

def baslik_ekle(slide, text, y=Inches(0.3), font_size=40, renk=MAVI_KOYU):
    # Büyük başlık, sol hizalı
    txBox = slide.shapes.add_textbox(Inches(0.8), y, Inches(11.7), Inches(1.0))
    tf = txBox.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = text
    p.font.size = Pt(font_size); p.font.color.rgb = renk
    p.font.bold = True; p.font.name = "Calibri"

def cizgi_ekle(slide, y=Inches(1.6)):
    # Mavi ayırıcı çizgi
    line = slide.shapes.add_shape(1, Inches(0.8), y, Inches(11.7), Pt(3))
    line.fill.solid(); line.fill.fore_color.rgb = MAVI_CANLI
    line.line.fill.background()

def madde_ekle(slide, maddeler, y_bas=Inches(1.8), x=Inches(0.8), font_size=16, sutun_sayisi=1):
    # ▸ ile liste. sutun_sayisi=2 ise iki textbox'a böler
    ...

def tablo_ekle(slide, data, x, y, genislik, yukseklik):
    # Tablo. data[0] başlık satırı. Başlık mavi, çift satırlar açık mavi
    ...
```

### 5. Her bölümü slayta dönüştür

Word'deki `Heading 1` → slayt başlığı
Word'deki `List Bullet` → madde listesi
Word'deki tablolar → PPT tabloları
Word'deki `Normal` → içerik paragrafı

### 6. Özel slaytlar

- **Kapak:** Koyu mavi arka plan, SARI başlık, beyaz alt başlık
- **Bilgi/Vurgu:** Açık mavi dikdörtgen içinde önemli not
- **Sonuç:** Koyu mavi arka plan, SARI başlık, beyaz metin
- **Karşılaştırma:** İki sütunlu düzen (sol: X, sağ: Y)

### 7. Başarılı Örnek

- **Kaynak:** `ic_musteri\10002_ic_musteri_memnuniyeti.docx`
- **Çıktı:** `Desktop\10002_ic_musteri_memnuniyeti.pptx` (15 slayt)
- **İçerik:** 10 bölüm + kapak + künye + istatistikler + sonuç + kaynaklar
