---
name: siber-guvenlik-bulut
description: Bulut Güvenliği — 6 soru-cevap. Paylaşılan sorumluluk, CASB, CSPM, CWPP, multi-cloud, DevSecOps.
version: 1.0
category: security
tags: [cloud-security, casb, cspm, cwpp, devsecops, multi-cloud]
---

# Bulut Güvenliği

## S1: Paylaşılan sorumluluk modeli nedir?
**Cevap:** Bulut güvenliği sağlayıcı ve müşteri arasında paylaşılır. AWS/Azure/GCP: fiziksel güvenlik, hipervizör, ağ altyapısından sorumlu. Müşteri: işletim sistemi, uygulama, veri, erişim yönetimi, ağ yapılandırmasından sorumlu. En yaygın hata: müşterilerin sorumluluklarını sağlayıcıya bırakması. IaaS'de müşteri daha çok, SaaS'de sağlayıcı daha çok sorumlu.

## S2: CASB (Cloud Access Security Broker) nedir?
**Cevap:** CASB, bulut hizmetleri ile kullanıcılar arasında güvenlik politikası uygulayan bir aracıdır. Yetkisiz erişimleri engeller, veri kaybını önler (DLP), uyumluluğu denetler. Örnek: Netskope, McAfee MVISION Cloud. 2026'da CASB, SSE (Security Service Edge) çözümlerinin bir parçası haline geliyor.

## S3: CSPM (Cloud Security Posture Management) nedir?
**Cevap:** CSPM, bulut altyapısındaki yanlış yapılandırmaları otomatik tespit eder. Örnek: Açık S3 bucket, herkese açık güvenlik grubu, şifrelenmemiş veritabanı. Sürekli tarama yapar, uyumluluk raporlar, düzeltme önerir. Örnek: Wiz, Prisma Cloud, Lacework.

## S4: CWPP (Cloud Workload Protection) nedir?
**Cevap:** CWPP, buluttaki iş yüklerini (sanal sunucu, container, serverless) korur. Kötü amaçlı yazılım taraması, zafiyet yönetimi, çalışma zamanı koruması sağlar. Container güvenliği için: görüntü tarama (image scanning), çalışma zamanı izleme, admission controller.

## S5: Multi-cloud güvenlik nasıl sağlanır?
**Cevap:** AWS+Azure+GCP birlikte kullanıldığında: 1) Merkezi kimlik yönetimi (SSO, federasyon) 2) Tutarlı güvenlik politikası (IaC ile policy-as-code) 3) Merkezi log toplama (SIEM'e tüm bulutlar) 4) CSPM ile sürekli uyumluluk kontrolü 5) Bulutlar arası ağ segmentasyonu. Zorluk: Her bulutun kendi güvenlik modeli farklı.

## S6: DevSecOps nedir?
**Cevap:** DevSecOps, güvenliği yazılım geliştirme yaşam döngüsüne entegre eder. Shift-left: güvenlik testini sola (erken aşamalara) kaydırma. CI/CD pipeline'ında: SAST (kaynak kod taraması), DAST (dinamik analiz), SCA (bağımlılık taraması), container taraması, IaC taraması (Terraform güvenlik). 2026 trendi: Pipeline içinde güvenlik geçitleri otomatik.
