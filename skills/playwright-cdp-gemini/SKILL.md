---
name: playwright-cdp-gemini
title: Chrome CDP + Playwright ile Gemini'ye mesaj gönderme (workflow)
description: Mevcut Chrome oturumuna CDP ile bağlanıp Gemini sohbet kutusuna metin yazma ve gönderme. Türkçe açıklamalı, adım adım çalışan workflow.
category: playwright-cdp-gemini
---

# Gemini Chat — CDP Workflow (güncel)

> **BU SKILL MODASI GEÇTİ.** Yerine kullanılacak:
> - `gemini-chat-cdp-workflow` — Chrome CDP başlatma + mesaj gönderme (step-by-step)
> - `hermes-gemini-copilot` — Tam otonom hata çözüm döngüsü (2 dene → Gemini → VS Code → Python)
> 
> İkisi de yeni Chrome yolunu (`scoop/apps/googlechrome/`) ve Anaconda Python'unu kullanır.

## Kısa özet (yerine geçen skill)
`skill_view('gemini-chat-cdp-workflow')` ile yükle.

Ana farklar:
- **Adım adım sıralı** — 1→5 arası net adımlar
- **Chrome öldürme + yeniden başlatma** dahil
- **Anaconda Python** ile çalıştırma (PATH sorunu yok)
- **Intro sayfası yönlendirme** CDP WebSocket ile
- Her seferinde **garantili çalışma** için test edildi
