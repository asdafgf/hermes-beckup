# Referans: 16 Testlik Mock Arkitektürü

Bu referans, `C:\Users\eymen\Desktop\test-harness\` altında kurulan test altyapısının detaylı dökümantasyonudur.

## Test Kapsamı (16 test, 0.05sn)

### financial/veri_cekici.py — 8 test

| Test | Teknik | Ne Sınar |
|---|---|---|
| `test_hisse_getir_basarili` | Mock().return_value | Başarılı API çağrısı, doğru URL |
| `test_hisse_getir_api_hatasi` | raise_for_status side_effect | 429 hata kodu, None dönüşü |
| `test_hisse_getir_network_hatasi` | session.get side_effect | Connection timeout, None dönüşü |
| `test_sepet_getir_bos_liste` | Boş liste girdisi | [] → [] |
| `test_sepet_getir_coklu` | call_count kontrolü | 3 API çağrısı, 3 sonuç |
| `test_anlik_fiyat_basarili` | @patch('requests.get') | XAUUSD fiyat çekme |
| `test_anlik_fiyat_hata` | @patch side_effect | API hatası, None |
| `test_session_mock_decorator` | @patch decorator | Alternatif mock yöntemi |

### osint/tarayici.py — 8 test

| Test | Teknik | Ne Sınar |
|---|---|---|
| `test_dns_basarili` | @patch socket.gethostbyname_ex | DNS çözümleme |
| `test_dns_bulunamadi` | socket.gaierror | DNS bulunamadı |
| `test_whois_basarili` | @patch whois.whois | WHOIS sorgusu |
| `test_whois_hata` | whois.whois side_effect | WHOIS timeout |
| `test_port_acik` | socket().connect_ex=0 | Port açık |
| `test_port_kapali` | socket().connect_ex=1 | Port kapalı |
| `test_coklu_port` | side_effect=[0,1] | Sıralı port tarama |
| `test_port_servis_adi` | Port→servis eşlemesi | SSH, MySQL, vs. |

## Fixture'lar (conftest.py)

| Fixture | Tür | Kullanım |
|---|---|---|
| `bist_api_anahtari` | Veri | Sabit test API key |
| `bist_cekici` | Mock | Session mock'lu BIST çekici |
| `basarili_api_yaniti` | Mock | 200 OK yanıt şablonu |
| `hata_api_yaniti` | Mock | 429 hata yanıtı şablonu |
| `osint_tarayici` | Instance | Mock'suz tarayıcı instance'ı |

## Yerel CI/CD (ci/run_tests.py)

| Parametre | İşlev |
|---|---|
| (parametresiz) | Tüm testleri çalıştır |
| `--watch` | Dosya değişikliklerini izle + otomatik test |
| `--coverage` | Kod kapsamı raporu ekle |
| `tests/test_financial.py` | Tek dosyayı test et |

## Kritik Mock Kalıpları

### 1. HTTP API Mock (requests.Session)
```python
# Fixture
cekici.session = Mock()
cekici.session.get.return_value = mock_resp

# Test
assert cekici.hisse_getir("THYAO")["fiyat"] == 125.50
cekici.session.get.assert_called_once_with(URL, timeout=10)
```

### 2. HTTP Error Mock
```python
mock_resp.raise_for_status.side_effect = \
    requests.exceptions.HTTPError("429", response=mock_resp)
```

### 3. Socket Mock (açık/kapalı port)
```python
# Açık port
instance.connect_ex.return_value = 0
# Kapalı port
instance.connect_ex.return_value = 1
# Sıralı
instance.connect_ex.side_effect = [0, 1, 0]
```

### 4. Decorator ile Mock
```python
@patch('src.financial.veri_cekici.requests.Session')
def test_ornek(mock_session):
    mock_session.return_value.get.return_value = mock_resp
```
