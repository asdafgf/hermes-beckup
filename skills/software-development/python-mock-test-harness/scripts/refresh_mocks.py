#!/usr/bin/env python3
"""
Mock Güncelleyici Betiği (Mock Refresher)

Canlı API'lere istek atar, JSON yanıtlarını tests/fixtures/ altındaki
statik dosyalara yazar. API başarısız olursa eski fixture korunur.

Çalıştırma (windows): python scripts/refresh_mocks.py
Çalıştırma (linux):   python3 scripts/refresh_mocks.py
"""

import json
import os
import sys
import urllib.request
import urllib.error

FIXTURES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "tests",
    "fixtures",
)

SOURCES = {
    "bist_latest.json": {
        "url": "https://api.genelpara.com/embed/borsa.json",
        "label": "BIST",
    },
    "xauusd_latest.json": {
        "url": "https://api.genelpara.com/embed/altin.json",
        "label": "XAUUSD",
    },
}

OSINT_SOURCES = {
    "dns_ornek.json": {
        "url": "https://dns.google/resolve?name=example.com&type=A",
        "label": "DNS Google",
        "timeout": 10,
    },
}


def fetch_json(url: str, timeout: int = 15) -> dict | None:
    """Bir URL'den JSON çeker, başarısızsa None döner."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "MockRefresher/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, OSError) as e:
        print(f"  [!] HATA: {e}")
        return None


def save_fixture(filename: str, data: dict | list) -> bool:
    """JSON'u fixture dosyasına kaydeder."""
    os.makedirs(FIXTURES_DIR, exist_ok=True)
    path = os.path.join(FIXTURES_DIR, filename)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  [OK] {filename} ({len(json.dumps(data))} bytes)")
        return True
    except OSError as e:
        print(f"  [!] YAZMA HATASI {filename}: {e}")
        return False


def main():
    """Ana akış: tüm kaynakları gezer, günceller, doğrular."""
    print("=" * 55)
    print("  MOCK GUNCELLEYICI (Mock Refresher)")
    print("  Hedef:", FIXTURES_DIR)
    print("=" * 55)
    print()

    os.makedirs(FIXTURES_DIR, exist_ok=True)
    extant = [f for f in os.listdir(FIXTURES_DIR) if f.endswith(".json")]
    if extant:
        print(f"[i] Mevcut fixturelar: {', '.join(extant)}\n")

    success_count = 0
    total_count = 0

    for group_label, sources in [("Finansal API", SOURCES), ("OSINT API", OSINT_SOURCES)]:
        print(f"[{group_label}]")
        print("-" * 40)
        for filename, src in sources.items():
            total_count += 1
            print(f"  → {src['label']}: {src['url']}")
            data = fetch_json(src["url"], timeout=src.get("timeout", 15))
            if data is not None:
                data["_meta"] = {
                    "source": src["label"],
                    "url": src["url"],
                    "fetched_at": "auto",
                }
                if save_fixture(filename, data):
                    success_count += 1
            else:
                path = os.path.join(FIXTURES_DIR, filename)
                if os.path.exists(path):
                    sz = os.path.getsize(path)
                    print(f"      Eski {filename} korunuyor ({sz} bytes).")
                else:
                    print(f"      [{filename} mevcut degil, atlandi]")
            print()

    # Doğrulama
    all_fixtures = [f for f in os.listdir(FIXTURES_DIR) if f.endswith(".json")]
    valid = sum(
        1 for f in all_fixtures
        if json.load(open(os.path.join(FIXTURES_DIR, f)))  # noqa: SIM115
    )
    print(f"[Dogrum] {valid}/{len(all_fixtures)} fixture gecerli JSON.")
    print()
    print("=" * 55)
    print(f"  SONUC: {success_count}/{total_count} kaynak guncellendi.")
    if success_count < total_count:
        print("  BAZI kaynaklara erisilemedi — eski veriler korunuyor.")
    print("=" * 55)
    return 0 if success_count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
