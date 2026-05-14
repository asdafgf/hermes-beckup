---
name: liveoverflow-firefox-pwn2own-zero-day
description: "LiveOverflow — Pwn2Own'da Firefox zero-day exploit. Manfred Paul'in Firefox acigi, $50K USB stick, disclosure room, zero-day lifecycle"
version: 1.0
category: security
source: "LiveOverflow YouTube"
tags: [pwn2own, firefox, zero-day, exploit, browser-security, disclosure, bug-bounty]
platforms: [linux, macos, windows]
---

# Firefox Pwn2Own Zero-Day

Kaynak: LiveOverflow

## Pwn2Own Yarismasi

- Dunyanin en prestijli hack yarismasi
- Manfred Paul Firefox'ta acik buldu
- USB stick icinde exploit → $50,000
- Sadece birkac satir kod

## Zero-Day Lifecycle

1. Kesif (Manfred Paul tarafindan bulundu)
2. Pwn2Own'da gosterim (sahne canli exploit)
3. Satin alma ($50K)
4. Disclosure room (Mozilla'ya bildirim)
5. Yama (Mozilla duzeltir)
6. Deger kaybeder (saatler icinde)

## Teknik Detaylar

- Firefox browser exploit
- Hafiza bozulmasi (memory corruption)
- RCE (Remote Code Execution)
- Sandbox bypass gerekebilir

## Browser Exploit Teknikleri

| Teknik | Aciklama |
|--------|----------|
| Use-after-free | Serbest birakilmis bellegi kullanma |
| Heap spray | Heap'i kontrol edilebilir veriyle doldurma |
| ROP chain | ASLR/DEP bypass |
| JIT spraying | JIT compiler behavior manipulation |
| Sandbox escape | Browser sandbox'ini asma |

## Kaynaklar

- LiveOverflow: https://www.youtube.com/@LiveOverflow
- Pwn2Own: https://www.zerodayinitiative.com
- Mozilla Security: https://www.mozilla.org/security
