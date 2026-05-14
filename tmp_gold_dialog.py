import urllib.request
import json

def ask_ollama(model, prompt):
    data = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read())["response"]

model = "gemma3:4b"

# Round 1: Hermes asks Ollama about gold
print("=" * 60)
print("HERMES: Altın fiyatlarının yükselmesinde en büyük etken nedir?")
print("        ABD faiz kararları mı, jeopolitik riskler mi?")
print("        Bunlar birbirini nasıl etkiliyor?")
print("=" * 60)

r1 = ask_ollama(model, (
    "Sen bir AI asistansın. Sana Hermes adında başka bir AI mesaj atıyor:\n\n"
    "HERMES: 'Altın fiyatlarının yükselmesinde en büyük etken nedir? "
    "ABD faiz kararları mı, jeopolitik riskler mi? Bunlar birbirini nasıl etkiliyor?'\n\n"
    "Bu soruyu cevapla. Cevabının sonunda Hermes'e bir soru sor: "
    "'Altın mı gümüş mü daha iyi bir yatırım aracı, neden?'"
))
print(f"\nOLLAMA: {r1}\n")
print("=" * 60)

# Round 2: Hermes answers Ollama's question
print("HERMES: Gümüş mü altın mı sorusuna cevabım şu:")
print()
print("        Altın daha istikrarlı bir değer saklama aracıdır. Merkez bankaları")
print("        rezervlerini altında tutar, ons altın 5000 yıllık tarihi olan")
print("        küresel bir güven limanıdır. Gümüş ise daha volatildir — sanayi")
print("        talebinden (güneş panelleri, elektronik) çok etkilenir. Kısa")
print("        vadede gümüş daha fazla kazandırabilir ama riski de yüksektir.")
print("        Uzun vadede altın daha güvenlidir.")
print()
print("        Peki sana bir sorum var: Altının düşüşünde Fed faiz artırımları mı")
print("        daha etkili, yoksa doların güçlenmesi mi? İkisi aynı şey değil mi?")
print("=" * 60)

r2 = ask_ollama(model, (
    "Sana Hermes AI cevap veriyor:\n\n"
    "HERMES: 'Gümüş daha volatil ama altın daha güvenli bir liman. "
    "Peki sana bir sorum var: Altının düşüşünde Fed faiz artırımları mı "
    "daha etkili, yoksa doların güçlenmesi mi? İkisi aynı şey değil mi?'\n\n"
    "Buna cevap ver. Cevabının sonunda Hermes'e bir soru sor: "
    "'Peki ons altın için teknik analizde hangi seviyeler önemli - direnç ve destek noktaları neler?'"
))
print(f"\nOLLAMA: {r2}\n")
print("=" * 60)

# Round 3: Hermes answers about technical analysis
print("HERMES: Teknik analizde ons altın için önemli seviyeler genelde şöyle:")
print()
print("        DESTEK: $2.300 - $2.280 (psikolojik), $2.250 (200 günlük hareketli ortalama)")
print("        DİRENÇ: $2.400 (tarihi zirve bölgesi), $2.450 (yeni rekor bölgesi)")
print()
print("        Ama bu seviyeler günlük değişir, güncel grafik bakmak gerek.")
print("        Son bir sorum var: Altın fiyatını etkileyen en öngörülemez faktör")
print("        nedir? Yani hangi değişkeni hesaplamak en zordur?")
print("=" * 60)

r3 = ask_ollama(model, (
    "Sana Hermes AI cevap veriyor:\n\n"
    "HERMES: 'Destek $2300, direnç $2400 civarı. "
    "Son bir sorum var: Altın fiyatını etkileyen en öngörülemez faktör "
    "nedir? Yani hangi değişkeni hesaplamak en zordur?'\n\n"
    "Buna cevap ver."
))
print(f"\nOLLAMA: {r3}")
print("=" * 60)
