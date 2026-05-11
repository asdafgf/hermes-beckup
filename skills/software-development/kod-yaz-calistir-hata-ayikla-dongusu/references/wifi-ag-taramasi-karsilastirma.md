# WiFi Ağı Taraması — Claude vs Gemini Karşılaştırması

Bu belge, aynı görevi (WiFi ağındaki cihazları IP + MAC olarak listeleme) Claude ve Gemini'ye yazdırma ve sonuçları karşılaştırma oturumunun kaydıdır.

## Görev

Windows 11'de WiFi ağına bağlı cihazların IP ve MAC adreslerini listeleyen Python scripti:
- 192.168.0.0/24 ağı taranacak
- Broadcast adresleri (ff:ff:ff:ff:ff:ff) gösterilmeyecek
- Multicast adresleri (224.x.x.x, 239.x.x.x) gösterilmeyecek
- VirtualBox ağları (192.168.37.x, 192.168.56.x, 172.x.x.x) gösterilmeyecek
- Kendi IP'si listede görünmeyecek
- Modem (192.168.0.1) ayrı işaretlenecek
- ThreadPoolExecutor ile paralel tarama
- Türkçe hata mesajları

## Çalıştığı Sistem

- **Kullanıcı:** Eymen
- **Bilgisayar:** Erciyes (Windows 11)
- **WiFi:** Intel Wi-Fi 6E AX211
- **IP:** 192.168.0.20
- **Modem:** 192.168.0.1 (MAC: 98:f2:17:02:03:4f)
- **Ağ:** 192.168.0.0/24

## Karşılaştırma

| Kriter | Claude | Gemini |
|--------|--------|--------|
| İlk denemede çalıştı | ✅ Evet | ❌ Hayır |
| Düzeltme sayısı | 0 | 4 |
| Doğru cihaz sayısı | 5 | 4 |
| Broadcast filtresi | ✅ Otomatik | ❌ Elle düzeltildi |
| Kendi IP'yi gizleme | ✅ Otomatik | ❌ Elle düzeltildi |
| Kod kalitesi | Temiz, sade | Karmaşık, gereksiz kod |
| Çalışma süresi | ~120 saniye | ~120 saniye (aynı) |

## Gemini'nin Yaptığı Hatalar (Sırayla)

1. **ThreadPoolProcessor** — `concurrent.futures`'da böyle bir sınıf yok, doğrusu `ThreadPoolExecutor`
2. **cp857 encoding** — Windows'ta `ipconfig` çıktısı için `cp857` varsaydı, doğrusu `utf-8`, `errors='ignore'`
3. **WiFi IP bulamama** — `ipconfig` regex'i çalışmadı, PowerShell ile çözüldü
4. **ip_address.is_broadcast** — `IPv4Address` nesnesinde böyle bir özellik yok, sadece `is_multicast` var

## Alınan Dersler

1. Gemini kod yazabilir ama Claude'a göre **daha fazla denetim ve düzeltme gerektirir**
2. Gemini'ye hatayı geri bildirip düzelttirme döngüsü çalışıyor — bu yöntem geçerli
3. İkinci ve üçüncü düzeltmede Gemini daha iyi kod üretiyor (öğreniyor)
4. Broadcast filtreleme gibi incelikler Gemini'nin atladığı detaylar
5. Claude birincil tercih, Gemini yedek olarak kullanılmalı
