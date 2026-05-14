# Example: Verifying a Skill with Empty Qwen Responses

Date: 2026-05-14
Skill: ag-guvenligi-port-tarama-sniffing-ve-mitm (SIB-002)
Model: qwen2.5-coder:7b
Tool: Ollama local API (curl)

## Problem

The skill's `references/diyalog.txt` had both Qwen2.5-coder responses empty:

```
Qwen2.5-coder (Yanit 1): [BOS - henuz yanit yok]
Qwen2.5-coder (Yanit 2): [BOS - henuz yanit yok]
```

No `references/qwen_yanit.txt` or `references/qwen_yanit_dogrulanmis.txt` existed — only the skeleton diyalog.txt.

## Approach

1. Read SKILL.md, diyalog.txt — understood the topic and the questions Hermes asked
2. Crafted a verification prompt that asked qwen2.5-coder to:
   - Evaluate the topic as if it had content
   - **Generate the missing content** (since it was empty)
   - Check for inaccuracies in whatever existed
3. Used the `-d @file` technique to avoid bash escaping issues with Turkish text
4. Saved result to `references/qwen_derin_dogrulama.txt`

## Key Decisions

### Result classification
Even though the topic itself is valid (ağ güvenliği is a real topic), the **empty Qwen responses** made the skill incomplete. Classified as "KISMEN GEÇERLİ" rather than "GEÇERLİ".

### Verification report structure
```
=== DOGRULAMA RAPORU ===
1. GENEL DEGERLENDIRME:
2. PORT TARAMA TEKNIKLERI (her biri: nasil calisir, kullanim, tespit):
3. PAKET ANALIZI:
4. ARP SPOOFING ve MITM:
5. MODERN ACLARDA ARP SPOOFING:
6. DUZELTILMESI GEREKENLER / EKSIKLER:
=== SONUC: KISMEN GECERLI ===
```

### Findings from qwen2.5-coder's analysis
- TCP SYN, Connect, UDP, FIN scans: technically correct but needed deeper explanation
- UDP scan had a minor technical inaccuracy (blamed NAT instead of stateless protocol)
- Missing: Nmap flag examples, BPF filter examples, VLAN hopping, DAI configuration
- Overall: "KISMEN GECERLI"

## Pitfall Avoided

**Bash string escaping with Turkish characters.** The original attempt used inline JSON with `'...'` quotes. Bash tried to parse `(Açılış)` as a subshell. Solution: write JSON to `/tmp/` file, use `curl -d @file`.

```bash
# Write prompt to file (escapes handled by write_file, not bash)
echo '{"model":"qwen2.5-coder:7b","prompt":"...","stream":false}' > /tmp/prompt.json
# Send with curl (no inline escaping issues)
curl -s --max-time 180 -X POST http://localhost:11434/api/generate -d @/tmp/prompt.json
```
