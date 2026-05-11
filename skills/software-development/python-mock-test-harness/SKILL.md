---
name: python-mock-test-harness
description: >-
  4-katmanlı Python test altyapısı — unittest.mock ile dış bağımlılık izolasyonu,
  pytest + conftest ile merkezi fixture yönetimi, Mock Refresher ile canlı veri→fixture
  dönüşümü, watchdog debounce ile yerel CI/CD, ve React Native UI test iskeleti (MSW).
---

# Python Mock Test Harness

## Ne Zaman Kullanılır

- Dış API'lere (BIST, XAUUSD, WHOIS, DNS) bağımlı kodları **ağ isteği yapmadan** test etmek
- PyTest conftest.py ile proje genelinde paylaşılan test verisi (fixture) yönetimi
- `unittest.mock` ile socket, requests, whois çağrılarını simüle etme
- Mock verilerini canlı API'lerden güncelleme (Mock Refresher)
- Dosya değişikliklerinde **debounce ile** otomatik test koşumu
- React Native/Mobil UI bileşenlerini MSW ile mock API üzerinden test etme

## Mimarı (5 Katman)

### Katman 1 — Mock/Stubbing (unittest.mock)

**3 mock tekniği:**

1. **`Mock()` nesnesi** — elle mock oluştur, return_value ve side_effect ata
   ```python
   mock_resp = Mock()
   mock_resp.status_code = 200
   mock_resp.json.return_value = {"price": 125.50, "change_pct": 1.23}
   mock_resp.raise_for_status.return_value = None
   ```

2. **`@patch` dekoratörü** — fonksiyon seviyesinde otomatik mock
   ```python
   @patch('socket.gethostbyname_ex')
   def test_dns(self, mock_dns):
       mock_dns.return_value = ("example.com", [], ["93.184.216.34"])
   ```

3. **`side_effect`** — farklı çağrılarda farklı yanıtlar veya hata simülasyonu
   ```python
   mock_socket.connect_ex.side_effect = [0, 1]  # ilk açık, ikinci kapalı
   mock_get.side_effect = ConnectionError("API kapalı")  # hata fırlat
   ```

**Kritik kurallar:**
- `raise_for_status` bir **metot**'tur, property değil — `side_effect` ile hata fırlat
- `requests.exceptions.ConnectionError`, `HTTPError` gibi **gerçek exception sınıflarını** kullan, `Exception` değil
- `import requests` test dosyasında yapılmalı, fixture'da kullanılacaksa conftest'te de import et
- Mock'un çağrıldığını doğrulamak için `assert_called_once_with()`, `assert_not_called()` kullan

### Katman 2 — Pytest Fixture'ları (conftest.py)

**Merkezi fixture dosyası** `tests/conftest.py`'de tanımlanır, tüm test dosyaları kullanır:

```python
# conftest.py
@pytest.fixture
def bist_cekici(bist_api_anahtari):
    cekici = BISTVeriCekici(bist_api_anahtari)
    cekici.session = Mock()  # HTTP session mock'la
    return cekici

@pytest.fixture
def basarili_api_yaniti():
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"price": 125.50, ...}
    mock_resp.raise_for_status.return_value = None
    return mock_resp
```

**Fixture türleri:**
- **Veri fixture'ları** — sabit test değerleri (API key, domain list)
- **Mock fixture'ları** — önceden yapılandırılmış mock nesneleri
- **Context manager fixture'ları** — `with patch(...)` sarmalayan yield'li fixture
- **Fixture parametrizasyonu** — `@pytest.mark.parametrize` ile farklı yanıt senaryoları

### Katman 3 — Statik Fixture Dosyaları + Mock Refresher

**Statik fixture'lar (`tests/fixtures/`):** Gerçek API yanıtlarının JSON kopyaları. Testler bunları kullanır — ağ isteği gitmez.

```python
@pytest.fixture
def bist_verisi():
    """tests/fixtures/bist_latest.json'den okur."""
    path = os.path.join(FIXTURES_DIR, "bist_latest.json")
    with open(path) as f:
        return json.load(f)
```

**Mock Refresher (`scripts/refresh_mocks.py`):** Canlı API'lere istek atar, dönen JSON'ı doğrudan `tests/fixtures/` içindeki dosyaların üzerine yazar. Böylece test verisi güncel kalır.

**Fallback stratejisi:** API başarısız olursa (`HTTP 404`, timeout) eski fixture dosyası korunur, hiçbir test kırılmaz. `_meta` anahtarı her fixture'a source/url/fetched_at bilgisini ekler.

```python
# refresh_mocks.py — akış şeması
for filename, src in SOURCES.items():
    data = fetch_json(src["url"])       # canlı API
    if data is not None:
        save_fixture(filename, data)    # fixture'a yaz
    else:
        # mevcut dosyayı koru, silme/güncelleme yapma
```

**Örnek fixture yapısı:**
```json
{
  "bist": {
    "XU100": {"price": 9850.45, "change_pct": 1.23},
    "XU030": {"price": 11230.20, "change_pct": 0.87}
  },
  "timestamp": "2025-05-11T06:44:00Z",
  "_meta": {
    "source": "BIST",
    "url": "https://api.genelpara.com/embed/borsa.json",
    "fetched_at": "auto"
  }
}
```

### Katman 4 — Yerel CI/CD (Watchdog + Debounce)

**Watchdog Kütüphanesi:** `pip install watchdog` ile. Dosya sistemi olaylarını poll yerine OS-native API ile izler (düşük CPU, hızlı algılama).

**Debounce Mekanizması (threading.Timer):**
```python
class DebouncedWatcher:
    def __init__(self, debounce_seconds=1.5):
        self._timer = None
        self._lock = Lock()

    def on_modified(self, event_path):
        if not event_path.endswith('.py'):
            return
        with self._lock:
            if self._timer:
                self._timer.cancel()      # önceki timer'ı iptal et
            self._timer = Timer(self.debounce_seconds, self._run_tests)
            self._timer.daemon = True
            self._timer.start()
```

**Neden `threading.Timer` + `Lock`:**
- `time.sleep(N)` → sistemi dondurur, çoklu Ctrl+S'yi teke indirgeyemez
- `threading.Timer` → her değişiklikte geri sayım sıfırlanır, son kaydettikten 1.5s sonra test koşar
- `Lock` → aynı anda birden fazla test tetiklenmesini engeller

**Çalıştırma:**
```bash
# Watch mode (debounce 1.5s)
python ci/run_tests.py --watch

# Tek seferlik test
python ci/run_tests.py
```

**Olay akışı:**
```
Ctrl+S (0.0s) → Timer(1.5) başlat
Ctrl+S (0.8s) → Timer iptal, yeni Timer(1.5) başlat
Ctrl+S (1.2s) → Timer iptal, yeni Timer(1.5) başlat
bekleme       → 1.5s geçti → test koş (tek sefer)
```

### Katman 5 — React Native/UI Test İskeleti (MSW + Jest)

**MSW (Mock Service Worker):** Jest/node ortamında HTTP isteklerini intercept eder, Python backend'e gitmeden mock yanıt döndürür.

**Handler tanımı:**
```typescript
// tests/ui/mocks/handlers.ts
import { rest } from 'msw';

const API_BASE = 'http://localhost:8000/api';

export const handlers = [
  rest.get(`${API_BASE}/bist/latest`, (req, res, ctx) => {
    return res(ctx.status(200), ctx.json({
      status: 'ok',
      data: { XU100: { price: 9850.45, change_pct: 1.23 } },
    }));
  }),
  // Hata senaryosu da tanımlanabilir
  rest.get(`${API_BASE}/error`, (req, res, ctx) => {
    return res(ctx.status(503), ctx.json({ error: 'Service Unavailable' }));
  }),
];
```

**Server setup:**
```typescript
import { setupServer } from 'msw/node';
export const server = setupServer(...handlers);
```

**Test şablonu:**
```typescript
import { render, screen, waitFor } from '@testing-library/react-native';

describe('Dashboard Bileseni (MSW ile)', () => {
  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());
  afterAll(() => server.close());

  it('bilesen render olur ve API'den veri ceker', async () => {
    const onData = jest.fn();
    render(<Dashboard onDataFetched={onData} />);
    await waitFor(() => {
      expect(onData).toHaveBeenCalledWith(
        expect.objectContaining({ XU100: expect.any(Object) })
      );
    });
  });

  it('API hatasinda error state gosterilir', async () => {
    server.use(rest.get(`${API_BASE}/bist/latest`, (_, res, ctx) =>
      res(ctx.status(500), ctx.json({ error: 'Internal error' }))
    ));
    // ... assert error state
  });
});
```

**Önemli:** MSW handler'ları `beforeAll/afterEach/afterAll` ile lifecycle yönetimi gerektirir. `server.resetHandlers()` her test arası handler override'larını temizler.

## Klasör Yapısı

```
proje/
├── scripts/
│   └── refresh_mocks.py              # Mock verilerini canlı API'den günceller
├── src/
│   ├── financial/veri_cekici.py      # mock'lanacak modül
│   └── osint/tarayici.py             # mock'lanacak modül
├── tests/
│   ├── conftest.py                   # merkezi fixture'lar
│   ├── fixtures/
│   │   ├── bist_latest.json          # statik mock verisi (refresh_mocks ile güncellenir)
│   │   ├── xauusd_latest.json
│   │   └── dns_ornek.json
│   ├── ui/
│   │   ├── mocks/
│   │   │   └── handlers.ts           # MSW handler tanımları
│   │   ├── test_dashboard.tsx         # React Native test örneği
│   │   └── jest.config.js            # Jest + RNTL konfigürasyonu
│   ├── test_financial.py             # finans testleri
│   └── test_osint.py                 # OSINT testleri
├── ci/
│   └── run_tests.py                  # watchdog + debounce CI/CD
├── pytest.ini                        # pytest yapılandırması
└── requirements.txt
```

## Çalıştırma Komutları

```bash
# 1. Mock verilerini güncelle (canlı API istekleri)
python scripts/refresh_mocks.py

# 2. Tüm testleri çalıştır
python ci/run_tests.py

# 3. Watch mode (debounce ile)
python ci/run_tests.py --watch

# 4. Sadece UI testleri (RN projesinde)
cd mobile && npx jest tests/ui/
```

## Tuzaklar

- **Mock'un `raise_for_status`'u metottur:** `Mock(raise_for_status=Mock(side_effect=...))` çalışmaz çünkü property olarak set eder. `mock_resp.raise_for_status.side_effect = ...` ile ata.
- **Exception sınıfı seçimi:** `requests.exceptions.ConnectionError` kullan, `Exception("Connection timeout")` değil. Aksi halde try/except `requests.RequestException` yakalamaz.
- **Import scope'u:** Decorator içinde kullanılan modüller test dosyasında import edilmiş olmalı. `# noqa: F821` bir çözüm değil — doğru import'u yap.
- **Side effect sırası:** `side_effect = [0, 1]` listedeki sırayla tetiklenir. `side_effect = Exception(...)` listede değilse hemen fırlatılır.
- **conftest.py'de requests import'u:** Fixture'da `requests.exceptions` kullanılıyorsa conftest'in tepesinde `import requests` yap.
- **Watchdog debounce:** `time.sleep()` KULLANMA — `threading.Timer` + `Lock` ile yap. Yoksa çoklu kaydetme işlemi N tane test tetikler.
- **Mock Refresher fallback:** API başarısız olduğunda eski fixture'ı silme. `save_fixture()` sadece `data is not None` ise yazar.
- **MSW lifecycle:** Her test `server.resetHandlers()` ile başlamalı yoksa önceki testin handler override'ları birikir.
- **refresh_mocks windows yolu:** `subprocess.run(['python', 'scripts/refresh_mocks.py'], ...)` windows'ta çalışır ama `/c/Users/.../python.exe` mutlak yolu kullanılıyorsa `cwd` parametresini de geç.
- **API 404 fallback:** `refresh_mocks.py`'de canlı API 404 döndüğünde eski fixture JSON **silinmez, korunur**. `_meta` anahtarı source/url bilgisini taşır.
- **refresh_mocks.py çalıştırma:** Anaconda Python ile çalıştırılmalı (`/c/Users/eymen/anaconda3/python.exe scripts/refresh_mocks.py`). Hermes'in varsayılan Python'unda bazı kütüphaneler (beautifulsoup4) olmayabilir.

## Referanslar

- `references/` — örnek test senaryoları, mock kalıpları, eski session detayları
- `templates/` — conftest.py şablonu, CI/CD betiği şablonu, MSW handler şablonu
- `scripts/` — test jeneratörü, fixture doğrulayıcı

## İlgili Skill'ler

- `test-driven-development` — TDD döngüsü (RED-GREEN-REFACTOR)
- `systematic-debugging` — hata ayıklama + AI escalation
- `kod-yaz-calistir-hata-ayikla-dongusu` — kod yaz/çalıştır/hata ayıkla döngüsü

## Bağımlılıklar

- pytest>=8.0
- requests
- python-whois (OSINT testleri için)
- watchdog>=4.0 (CI/CD watcher için)
- msw>=2.0 (RN UI testleri için — opsiyonel)
