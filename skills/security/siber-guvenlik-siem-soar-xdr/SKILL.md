---
name: siber-guvenlik-siem-soar-xdr
description: SIEM, SOAR ve XDR Platformları — 6 soru-cevap. SOC, AI SOC Agent, log yönetimi, otomasyon.
version: 1.0
category: security
tags: [siem, soar, xdr, soc, log-management, automation]
---

# SIEM, SOAR ve XDR Platformları

## S1: SIEM nedir ve nasıl çalışır?
**Cevap:** SIEM (Security Information and Event Management), kurumdaki tüm güvenlik kaynaklarından (firewall, server, uygulama, bulut) log toplar, korelasyon kurallarıyla analiz eder ve gerçek zamanlı uyarı üretir. 2026'da SIEM: AI ile destekleniyor, bulutta çalışıyor, günde milyonlarca log olayını analiz ediyor. Örnek: Splunk, Microsoft Sentinel, Elastic SIEM.

## S2: SOAR nedir?
**Cevap:** SOAR (Security Orchestration, Automation, Response), güvenlik olaylarına otomatik müdahale için playbook'lar çalıştırır. Bir SIEM uyarısı geldiğinde SOAR: IP'yi otomatik karalisteye ekler, host'u izole eder, ticket açar, analiste bildirim gönderir. 2026'da SOAR playbook'ları doğal dil ile yazılabiliyor. Örnek: Palo Alto XSOAR, Splunk SOAR.

## S3: XDR nedir? SIEM ve SOAR'dan farkı ne?
**Cevap:** XDR (Extended Detection and Response), endpoint, ağ, bulut ve e-posta verilerini tek platformda birleştirir. SIEM sadece log toplarken, XDR tehdidi tespit eder, araştırır ve müdahale eder. Fark: SIEM size ne olduğunu söyler, XDR ne yapmanız gerektiğini söyler. 2026 trendi: XDR + SIEM entegrasyonu standartlaşıyor.

## S4: SIEM vs SOAR vs XDR vs AI SOC Agent karşılaştırması?
**Cevap:** SIEM=log toplama+korelasyon. SOAR=otomasyon+playbook. XDR=uçtan uca tespit+müdahale. AI SOC Agent=otonom tehdit avcılığı+triyaj. 2026'da en iyi yaklaşım: SIEM+XDR veri kaynağı, SOAR otomasyon katmanı, AI SOC Agent aracı olarak birlikte çalışır.

## S5: SOC (Security Operations Center) yapısı nasıldır?
**Cevap:** Tier 1: Gelen uyarıları triyaj eder, yanlış pozitifleri eler. Tier 2: Olay müdahale, derinlemesine analiz. Tier 3: Tehdit avcılığı, tersine mühendislik. 2026'da AI Tier 1 rolünü üstleniyor, insanlar Tier 2-3'e kayıyor.

## S6: 2026'da SOC verimliliği nasıl artırılır?
**Cevap:** AI destekli uyarı azaltma (yanlış pozitif oranını %80 düşürür), SOAR otomasyonu (tekrarlayan görevleri kaldırır), XDR entegrasyonu (araç karmaşasını azaltır), SIEM'de UEBA (anomali tespiti ile gerçek tehditleri öne çıkarır). Hedef: Zamanı düzeltme (Time to Remediate) metriğini iyileştirmek.
