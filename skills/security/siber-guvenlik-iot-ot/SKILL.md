---
name: siber-guvenlik-iot-ot
description: IoT, OT ve Endüstriyel Güvenlik — 6 soru-cevap. SCADA, PLC, IT-OT yakınsaması, 5G, edge, botnet.
version: 1.0
category: security
tags: [iot, ot, scada, plc, industrial-security, 5g, edge]
---

# IoT, OT ve Endüstriyel Kontrol Sistem Güvenliği

## S1: IoT güvenliğindeki en büyük zafiyetler neler?
**Cevap:** 30 milyar+ IoT cihazının çoğu: varsayılan şifreyle gelir, güncelleme almaz (veya alamaz), şifrelemesiz iletişim kullanır, düşük işlem gücü nedeniyle güvenlik yazılımı çalıştıramaz. En yaygın zafiyet: açık portlar, zayıf kimlik doğrulama, güncellenmemiş yazılım. Örnek: Bir akıllı bebek monitörü tüm eve giriş noktası olabilir.

## S2: OT (Operational Technology) güvenliği neden kritik?
**Cevap:** OT, fabrika kontrol sistemlerini (SCADA, PLC, DCS) kapsar. Kritik çünkü: fiziksel dünyayı kontrol eder (enerji, su, üretim), eski sistemler (10-20 yıllık, yama almaz), güvenlik için tasarlanmamış (öncelik: güvenilirlik ve süreklilik). 2026'da OT saldırıları %200 arttı.

## S3: IT-OT yakınsaması hangi riskleri getirir?
**Cevap:** Endüstri 4.0 ile BT ve OT ağları birleşiyor. Risk: Daha önce izole olan OT ağları (air-gapped) artık internet bağlantılı. Bir BT ağından OT sistemine geçiş mümkün. Saldırgan BT'den sızıp OT'ye geçerek fiziksel hasar verebilir. Çözüm: OT ağını mikro segmentasyonla ayırma, OT-SIEM kullanma, IT-OT arasında sıkı firewall.

## S4: Akıllı şebekeler ve kritik altyapı saldırıları?
**Cevap:** Enerji dağıtım sistemleri (akıllı şebekeler) uzaktan yönetiliyor. Saldırgan: sayaçları manipüle edebilir, enerji dağıtımını durdurabilir, transformatörleri yakabilir. Örnek: Ukrayna elektrik şebekesi saldırısı (2015, 2016), Colonial Pipeline (2021). 2026'da ulus-devlet aktörleri kritik altyapıyı hedeflemeye devam ediyor.

## S5: IoT botnet'leri ve DDoS saldırıları?
**Cevap:** Mirai botnet'inden bu yana IoT cihazları DDoS için silah olarak kullanılıyor. Güvenli olmayan kameralar, yönlendiriciler, akıllı cihazlar botnet'e eklenir. 2026'da AI destekli botnet'ler daha akıllı: hedef seçimi, trafik deseni taklidi, kendi kendini onarma.

## S6: 5G ve edge güvenlik nasıl sağlanır?
**Cevap:** 5G ağ dilimleme (network slicing): her hizmet için ayrı sanal ağ. Güvenlik: dilimler arası izolasyon, uç cihaz kimlik doğrulaması, şifreleme. Edge computing: veri kaynağına yakın işlem. Risk: edge cihazlar fiziksel korumasız, düşük işlem gücü. Çözüm: edge'de hafif güvenlik ajanları, donanım TPM, düzenli güncelleme.
