# Mock Refresher + Watchdog Debounce + RN UI — Session Notları

## Tarih: 2025-05-11

## 1. Mock Refresher (`scripts/refresh_mocks.py`)

**Amaç:** Canlı API yanıtlarını `tests/fixtures/*.json`'a düzenli olarak kopyalayarak test verisini güncel tutmak.

**Yaşananlar:**
- `api.genelpara.com` endpoint'leri 404 döndü (değişmiş/kalkmış)
- Betik düzgün çalıştı: başarısız API'ler için eski fixture korundu, DNS Google çalıştı
- `save_fixture()` sadece `data is not None` ise yazar — bu fallback kritik

**Önemli detay:**
```python
data["_meta"] = {
    "source": label,
    "url": url,
    "fetched_at": "auto",  # str(datetime.now()) da olabilir
}
```
Her fixture'a meta eklenmeli ki hangi API'den ne zaman alındığı belli olsun.

## 2. Watchdog Debounce (`ci/run_tests.py`)

**Amaç:** `time.sleep(N)` kullanmadan, çoklu Ctrl+S'yi tek teste dönüştürmek.

**Çözüm:**
- `threading.Timer(1.5, fn)` — her değişiklikte eski timer'ı iptal edip yenisini başlatır
- `threading.Lock` — çoklu event thread'inde race condition'ı önler
- `watchdog 4.0.2` kurulu ve çalışıyor

**Yaşananlar:**
- `timeout 5 python ci/run_tests.py --watch` → hiç çıktı vermedi (çünkü `time.sleep(0.1)` döngüsü timeout ile kesilemiyor, `SIGTERM` windows'ta `time.sleep`'i bölmüyor)
- Doğrudan terminal'de çalıştırılmalı, `timeout` ile değil

**Test sonucu:** `python ci/run_tests.py` → 16/16 test, 0.03s

## 3. React Native UI İskeleti (`tests/ui/test_dashboard.tsx`)

**Amaç:** MSW (Mock Service Worker) ile Python backend yerine mock yanıt döndüren RN testi.

**MSW Handler pattern'i:**
```typescript
// Her handler = bir API endpoint mock'u
rest.get(`${API_BASE}/bist/latest`, (_, res, ctx) => {
  return res(ctx.status(200), ctx.json({ data: {...} }));
});
```

**Lifecycle (zorunlu):**
```typescript
beforeAll(() => server.listen());       // MSW sunucusunu başlat
afterEach(() => server.resetHandlers()); // handler override'larını temizle
afterAll(() => server.close());         // sunucuyu durdur
```

**5 handler tanımlandı:** BIST, XAUUSD, DNS, Port, Error

## 4. Bağımlılıklar

```bash
pip install watchdog  # Anaconda'da 4.0.2
npm install msw @testing-library/react-native --save-dev
```

## 5. Proje Durumu — Test-harness (16 dosya)

```
test-harness/
├── scripts/refresh_mocks.py                    # Mock Refresher
├── src/financial/veri_cekici.py                # mock'lanan modül
├── src/osint/tarayici.py                       # mock'lanan modül
├── tests/conftest.py                           # 16 fixture
├── tests/test_financial.py                     # 8 test
├── tests/test_osint.py                         # 8 test
├── tests/fixtures/
│   ├── bist_latest.json                        # manuel yedek (325 bytes)
│   ├── xauusd_latest.json                      # manuel yedek (248 bytes)
│   └── dns_ornek.json                          # DNS Google'dan (617 bytes)
├── tests/ui/test_dashboard.tsx                 # RN test iskeleti (246 satır)
├── ci/run_tests.py                             # watchdog + debounce
├── pytest.ini
└── requirements.txt
```

## Gelecek Geliştirmeler

- `refresh_mocks.py`'ye bir API bulma (service discovery) katmanı eklenebilir
- Mock fixture'ların otomatik versiyonlanması (birden fazla sürüm, tarihçe)
- CI/CD'ye coverage raporu ekleme (`--coverage`)
