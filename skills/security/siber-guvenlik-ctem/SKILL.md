---
name: siber-guvenlik-ctem
description: Sürekli Tehdit Maruziyet Yönetimi (CTEM) — 6 soru-cevap. ASM, dark web izleme, shadow IT, zafiyet önceliklendirme.
version: 1.0
category: security
tags: [ctem, asm, threat-exposure, dark-web, shadow-it, vulnerability]
---

# Sürekli Tehdit Maruziyet Yönetimi (CTEM)

## S1: CTEM nedir ve geleneksel zafiyet taramalarından farkı ne?
**Cevap:** Continuous Threat Exposure Management (CTEM), sürekli ve proaktif bir tehdit maruziyet yönetimi yaklaşımıdır.
- **Geleneksel:** Yılda/ayda bir zafiyet taraması → rapor → yama → bir sonraki taramaya kadar bekle.
- **CTEM:** Sürekli keşif, önceliklendirme, düzeltme ve doğrulama döngüsü.
- **Gartner 2026:** CTEM kullanan şirketlerin ihlal yaşama olasılığı 3 kat daha düşük.
- **5 aşama:**
  1. Kapsam belirleme (hangi varlıklar izlenecek?)
  2. Keşif (zafiyetleri, yanlış yapılandırmaları bul)
  3. Önceliklendirme (gerçek risk taşıyanları belirle)
  4. Düzeltme (yama, yapılandırma değişikliği)
  5. Doğrulama (düzeltme çalıştı mı?)

## S2: Dış saldırı yüzeyi yönetimi (ASM) — unutulmuş varlıklar nasıl keşfedilir?
**Cevap:** Attack Surface Management (ASM), dışarıdan görünen tüm varlıklarınızı keşfeder:
- **Keşfedilenler:**
  - Unutulmuş alt alan adları (subdomain'ler)
  - Açık API endpoint'leri
  - Süresi dolmuş/geçersiz SSL sertifikaları
  - Bulut çalışma alanları (S3 bucket, Azure Blob)
  - Shadow IT (izinsiz bulut hizmetleri)
  - Üçüncü taraf bağlantıları
- **Araçlar:** Censys, Shodan, RiskIQ, CrowdStrike Falcon Surface
- **2026 trendi:** ASM artık CTEM'in ayrılmaz bir parçası. Gartner, ASM'siz CTEM'in eksik olduğunu belirtiyor.
- **Sıklık:** Sürekli (7/24) tarama, günde bir rapor.

## S3: Karanlık ağ izleme — çalınan veriler dark web'de nasıl dolaşır?
**Cevap:** Dark web izleme, CTEM'in önemli bir bileşenidir:
- **İzlenenler:**
  - Çalınan kullanıcı adı/şifre kombinasyonları
  - Şirket e-posta adresleri
  - Kredi kartı numaraları
  - API anahtarları ve token'lar
  - Satılık kurumsal erişimler
- **Nasıl çalışır:**
  - Dark web forumları, Telegram grupları, IRC kanalları taranır
  - Şirket domain'i ve sızdırılmış veri setleri eşleştirilir
  - Tespit edilen sızıntılarda anlık uyarı
- **Örnek:** Bir çalışanın şifresi başka bir sitede çalındıysa, aynı şifreyi iş yerinde kullanıyorsa risk var.
- **Araçlar:** Digital Shadows, Recorded Future, SpyCloud.

## S4: Shadow IT yönetimi — çalışanların izinsiz kullandığı bulut hizmetleri hangi riskleri taşır?
**Cevap:** Shadow IT, çalışanların IT onayı olmadan kullandığı yazılım ve hizmetlerdir.
- **Riskler:**
  - Veri sızıntısı (Dropbox, Google Drive, ChatGPT'ye hassas dosya yükleme)
  - Uyumsuzluk (KVKK/GDPR ihlali)
  - Zararlı yazılım (lisanssız/denetimsiz yazılımlar)
  - Erişim kontrolü eksikliği (kim erişti belli değil)
- **Tespit:**
  - Ağ trafiği analizi (Cloud Access Security Broker - CASB)
  - DNS günlükleri (bilinmeyen domain'lere sorgular)
  - Endpoint ajanları (bilinmeyen uygulamalar)
- **2026'da:** IT departmanları ağ seviyesinde izinsiz AI araçlarını engelliyor, onaylı sandbox versiyonlar sunuyor.
- **Çözüm:** Şirket politikası + teknik engelleme (CASB, NGFW) + eğitim.

## S5: Binlerce zafiyet arasından kritik olanlar nasıl önceliklendirilir?
**Cevap:** Zafiyet yönetiminde her şey kritik değildir. Önceliklendirme için:
- **CVSS puanı:** 0-10 arası, aciliyet belirler (9+ kritik)
- **EPSS (Exploit Prediction Scoring System):** Zafiyetin aktif olarak sömürülme olasılığı
- **Varlık değeri:** Zafiyet kritik bir sistemde mi? (müşteri veritabanı vs iç wiki)
- **Saldırgan ilgisi:** Dark web'de satılıyor mu? Exploit kit'lerinde var mı?
- **İş etkisi:** Bu zafiyet iş sürekliliğini nasıl etkiler?
- **2026'da:** AI destekli önceliklendirme araçları binlerce zafiyeti saniyelerde analiz edip ilk 10'a indiriyor.
- **Kural:** Tüm zafiyetlerin %5'i gerçek risk taşır. Geri kalan %95'i yönetilir ihmal.

## S6: Sertifika ve TLS yönetimi — süresi dolmuş sertifikalar nasıl saldırı vektörüdür?
**Cevap:** Süresi dolmuş/zayıf TLS sertifikaları ciddi bir güvenlik açığıdır:
- **Riskler:**
  - Süresi dolmuş sertifika → hizmet kesintisi (web sitesi, API erişilemez)
  - Zayıf TLS (TLS 1.0/1.1) → ortadaki adam saldırısı (MITM)
  - Kendinden imzalı sertifika → kimlik doğrulaması yok
  - Wildcard sertifika → bir alt alan adı tehlikeye girerse hepsi düşer
- **2026 istatistiği:** Fortune 500 şirketlerinin %70'inde en az bir süresi dolmuş sertifika tespit edildi.
- **Yönetim:**
  - Merkezi sertifika yönetimi (Certificate Lifecycle Management)
  - Otomatik yenileme (Let's Encrypt, ACME protokolü)
  - Sertifika envanteri ve son kullanma tarihi takibi
  - Zayıf TLS protokollerini devre dışı bırakma (TLS 1.3 zorunlu)
