---
name: windows-c-junction-fix
title: Windows C:\c Junction Fix
description: Fix path mismatch by creating a junction link C:\c → C:\ so MSYS/git-bash paths resolve correctly.
---

# Windows `C:\c` Junction Fix

## Ne zaman kullanılır

- Sistemde path uyuşmazlığı var (ör. MSYS `/c/...` beklentisiyle fiziksel `C:\c` çakışması)
- `cd /c/c` çalışmıyor veya beklenen dizine gitmiyor
- Junction linki bozulmuş / silinmiş

## Komut

Yönetici PowerShell ile junction oluştur:

```powershell
powershell -Command "Start-Process powershell -Verb RunAs -ArgumentList 'New-Item -ItemType Junction -Path C:\c -Target C:\ -Force'"
```

## Doğrulama

```bash
ls -la /c/c         # → /c/c -> /c şeklinde symlink göstermeli
cd /c/c && ls       # → C:\ içeriğini listelemeli
```

## Terminal yeniden başlatma

Junction oluşturulduktan sonra Hermes terminal'i zaten yenilenir. Ekstra adım gerekmez.

## Pitfalls

- Junction oluşturmak **yönetici yetkisi** gerektirir (UAC onayı)
- Hermes terminal tool MSYS üzerinden çalıştığı için direkt `New-Item` çalışmaz — `Start-Process -Verb RunAs` ile yönetici PowerShell başlatmak gerekir
- Junction zaten varsa `-Force` ile üzerine yazılır
