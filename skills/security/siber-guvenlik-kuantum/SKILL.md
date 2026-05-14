---
name: siber-guvenlik-kuantum
description: Kuantum Güvenliği ve Kriptografi — 5 soru-cevap. PQC, NIST standartları, harvest-now-decrypt-later, hibrit yaklaşım.
version: 1.0
category: security
tags: [quantum, cryptography, pqc, nist, post-quantum]
---

# Kuantum Güvenliği ve Kriptografi

## S1: Kuantum bilgisayarlar mevcut şifrelemeyi ne zaman kırabilir? 'Topla şimdi, çöz sonra' stratejisi nedir?
**Cevap:** Kuantum bilgisayarların RSA-2048 gibi güncel şifrelemeyi kırması için ~1 milyon fiziksel kübit gerekli. 2026'da en güçlü sistemler ~1.000-2.000 kübite ulaştı. Tahmin: 2030-2035 arası.
- **'Harvest Now, Decrypt Later' (Topla şimdi, çöz sonra):** Saldırganlar bugün şifrelenmiş verileri çalıp depoluyor. Kuantum bilgisayar hazır olduğunda tüm bu verileri çözecekler.
- **Risk altındaki veriler:** Uzun ömürlü veriler (devlet sırları, patentler, sağlık kayıtları, finansal veriler) en büyük risk altında.
- **2026'da:** Finans ve sağlık regülatörleri şirketlerden kuantum geçiş planı istiyor.

## S2: Post-kuantum kriptografi (PQC) — NIST hangi algoritmaları onayladı?
**Cevap:** NIST (ABD Ulusal Standartlar Enstitüsü) 2024'te ilk PQC standartlarını yayınladı, 2026'da eklemeler devam ediyor:
- **Onaylanan algoritmalar:**
  1. **CRYSTALS-Kyber** (KEM - Anahtar Kapsülleme) — Genel anahtar değişimi için
  2. **CRYSTALS-Dilithium** (Dijital imza) — Yazılım imzalamak için
  3. **FALCON** (Dijital imza) — Daha kompakt imzalar
  4. **SPHINCS+** (Dijital imza) — Hash tabanlı, yedek algoritma
- **2026'da:** NIST ek algoritmalar için 4. tur değerlendirmeyi sürdürüyor.
- **Geçiş:** Mevcut RSA/ECC'den PQC'ye kademeli geçiş öneriliyor.

## S3: RSA ve ECC'nin yerini hangi yöntemler alacak?
**Cevap:**
| Güncel Algoritma | Kuantum Risk | PQC Alternatifi |
|-----------------|-------------|-----------------|
| RSA-2048 | Shor algoritması ile kırılabilir | CRYSTALS-Kyber (KEM) |
| ECC (Eliptik Eğri) | Shor ile kırılabilir | CRYSTALS-Dilithium (imza) |
| AES-256 | Grover ile yarı yarıya zayıflar | AES-256 yeterli (anahtar boyutu 2x) |
| SHA-256 | Grover ile zayıflar | SHA-384/512 yeterli |
- **Önemli:** AES ve SHA için tamamen değişim gerekmez — sadece anahtar boyutlarını büyütmek yeterli.
- **Geçiş stratejisi:** Hibrit şifreleme (RSA + Kyber birlikte) öneriliyor. Böylece biri kırılsa bile diğeri korur.

## S4: Kripto envanteri çıkarma — kamu anahtarı şifrelemesinin kullanıldığı yerler nasıl tespit edilir?
**Cevap:** Kuantum geçişinin ilk adımı, mevcut kripto kullanımını envantere çıkarmaktır:
- **Taranması gerekenler:**
  - TLS/SSL sertifikaları (web sunucuları, API'ler)
  - VPN yapılandırmaları (IPSec, OpenSSL)
  - Kod imzalama sertifikaları
  - SSH anahtarları
  - Veritabanı şifreleme
  - E-posta imzalama (S/MIME, PGP)
  - IoT cihaz sertifikaları
- **Araçlar:** Otomatik kripto keşif araçları (Cryptography Discovery, CryptoInventory)
- **Önceliklendirme:** Uzun ömürlü veriler (5+ yıl saklanacak) öncelikli
- **2026'da:** Regülatörler finans ve sağlık sektöründe kripto envanterini zorunlu kılıyor.

## S5: Hibrit kuantum geçiş yaklaşımı nedir? Mevcut sistemler nasıl taşınır?
**Cevap:** Hibrit yaklaşım, güncel algoritma (RSA/ECC) ile PQC algoritmasını birlikte kullanır:
- **Nasıl çalışır:** TLS bağlantısında hem RSA hem CRYSTALS-Kyber anahtar değişimi yapılır. İkisi de kırılmadığı sürece bağlantı güvende.
- **Avantajları:**
  - Kuantum bilgisayar hazır olana kadar güvenlik sağlar
  - Mevcut sistemlerle uyumlu
  - Kademeli geçiş imkanı
- **Geçiş adımları:**
  1. Kripto envanteri çıkar
  2. Uzun ömürlü verileri belirle
  3. Hibrit TLS yapılandırmasına geç
  4. PQC destekli sertifikaları dağıt
  5. Zamanla RSA/ECC'yi devre dışı bırak
- **Zorluklar:** Eski donanım/yazılım uyumu, performans (PQC daha büyük anahtarlar), standartların oturması.
