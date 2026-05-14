---
name: siber-guvenlik-mobil
description: Mobil Güvenlik ve Uç Nokta Koruma — 6 soru-cevap. MDM, EDR, BYOD, OWASP Mobile, şifreleme.
version: 1.0
category: security
tags: [mobile-security, mdm, edr, byod, owasp-mobile, encryption]
---

# Mobil Güvenlik ve Uç Nokta Koruma

## S1: Mobil tehditler 2026'da neler?
**Cevap:** En yaygın mobil tehditler: 1) Zararlı uygulamalar (resmi mağazalarda bile tespit edilen kötü amaçlı yazılımlar) 2) İşletim sistemi zafiyetleri (özellikle güncellenmeyen Android cihazlar) 3) Public Wi-Fi tuzakları (ortadaki adam saldırısı) 4) SMS phishing (smishing) 5) Mobil bankacılık truva atları. 2026'da mobil cihazlar, kurumsal ağa en yaygın giriş noktası.

## S2: MDM ve UEM nedir?
**Cevap:** MDM (Mobile Device Management): Kurumsal cihazları uzaktan yönetme (şifre politikası, uygulama dağıtımı, silme). UEM (Unified Endpoint Management): MDM'i genişletir — mobil+masaüstü+IoT'yi tek konsoldan yönetir. Özellikler: cihaz envanteri, uyumluluk politikası, kapsüllü uygulama dağıtımı, uzaktan silme. Örnek: Microsoft Intune, VMware Workspace ONE, Jamf.

## S3: EDR (Endpoint Detection and Response) nedir?
**Cevap:** EDR, uç noktalarda (bilgisayar, mobil) sürekli izleme ve anomali tespiti yapar. Davranışsal analizle bilinmeyen tehditleri tespit eder. Çalışma: kernel seviyesinde izleme, dosya/process/ağ bağlantısı kaydı, makine öğrenmesiyle anomali tespiti, otomatik karantina. Örnek: CrowdStrike Falcon, SentinelOne, Microsoft Defender for Endpoint.

## S4: BYOD (Bring Your Own Device) riskleri neler?
**Cevap:** BYOD: çalışanın kendi cihazını iş için kullanması. Riskler: 1) Veri sızıntısı (kişisel uygulama şirket verisine erişirse) 2) Kayıp/çalıntı cihazda şirket verisi 3) Kötü amaçlı kişisel uygulamalar 4) Karma (kişisel/iş) verinin mahremiyeti. Çözüm: containerization (iş verisi ayrı sandbox), kapsüllü uygulama, uzaktan silme yetkisi, kullanıcı onayı.

## S5: Mobil uygulama güvenliği (OWASP Mobile Top 10)?
**Cevap:** OWASP Mobile Top 10 (2024-2026): 1) Yanlış platform kullanımı 2) Güvensiz veri depolama 3) Güvensiz iletişim 4) Güvensiz kimlik doğrulama 5) Yetersiz kriptografi 6) Güvensiz yetkilendirme 7) İstemci kod kalitesi 8) Kod manipülasyonu 9) Tersine mühendislik 10) Ekstraksiyon. Test: SAST (statik kod analizi), DAST (dinamik), API testi, SSL pinning doğrulaması.

## S6: Uç nokta şifreleme nasıl çalışır?
**Cevap:** BitLocker (Windows): TPM + PIN/parola ile disk şifreleme, AES-128/256. FileVault (macOS): XTS-AES-128, FileVault2 ile tam disk. Mobil: iOS (AES-256 donanım şifreleme, Secure Enclave), Android (AES-128/256, FBE dosya bazlı şifreleme). 2026'da tüm işletim sistemleri varsayılan şifreleme sunuyor ancak etkinleştirme kullanıcıya bağlı.
