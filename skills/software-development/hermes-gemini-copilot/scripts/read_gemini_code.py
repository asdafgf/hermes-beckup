#!/usr/bin/env python3
"""
read_gemini_code.py — Gemini'den Playwright ile kod cevabını oku.
Kullanım: python read_gemini_code.py [bekleme_saniyesi]

UYARI: Bu script'i Anaconda Python ile çalıştır:
  /c/Users/eymen/anaconda3/python.exe read_gemini_code.py 12

Çıktı: STDOUT'a kod bloklarını yazar.
- Başarısızsa NO_GEMINI_PAGE yazar.
- 5 sn varsayılan bekleme, argüman olarak değiştirilebilir.
"""
import asyncio
import sys
from playwright.async_api import async_playwright

async def main():
    wait = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        gemini = None
        for page in browser.contexts[0].pages:
            if "gemini.google.com" in page.url:
                gemini = page
                break
        
        if not gemini:
            print("NO_GEMINI_PAGE")
            return
        
        await asyncio.sleep(wait)
        
        # Kod bloklarını kontrol et
        codes = await gemini.eval_on_selector_all(
            "pre code",
            "els => els.map(e => e.textContent).filter(t => t.length > 20)"
        )
        
        if codes and len(codes) > 0:
            # Son kodu al
            last_code = codes[-1][:8000]
            print(f"CODE:{last_code}")
            return
        
        # Son çare - son sohbet metnini al
        all_text = await gemini.evaluate("document.body.innerText")
        # Son 4000 karakter
        tail = all_text[-4000:] if len(all_text) > 4000 else all_text
        print(f"TEXT:{tail}")

if __name__ == "__main__":
    asyncio.run(main())
