---
name: python-oto-debug-dongusu
description: "Automatic Python code-write-run-fix loop using the agent's own debug capability (not Claude Code). VS Code auto-open on user request. Runs silently until passing — no user interrupts."
version: 2.0
author: agent
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [python, vscode, debugging, workflow, auto-loop]
    category: software-development
    related_skills: [systematic-debugging, nexus-core]
---

# Python Auto-Debug Loop (bana sorma modu)

## Overview

Fully automatic code-test-fix loop. The user says "şu işi yapan kodu yaz" (write code that does this thing). You write it, run it in terminal, check output for errors, fix and re-run until it works. **No manual VS Code actions from the user.** No waiting for them to copy-paste errors. No asking permission mid-loop.

**⚠️ The skill was renamed from `python-vscode-claude-debug-loop` to `python-oto-debug-dongusu` because the debug agent is DeepSeek (this Hermes model), NOT Claude Code CLI. The old name was misleading.

Key principle — **"bana sorma dongu"** (don't ask me, just loop): The user does not want to be interrupted with questions during iteration. Fix the code, re-run, repeat until the output is correct. Only notify them when the final working result is ready.

## Prerequisites

- **Python** installed (`python --version`)
- **VS Code** optional — only if the user explicitly wants to see the file in VS Code (check with `code --version`)
- Git Bash or PowerShell available for running Python scripts

## Workflow Steps

### Phase 1: Write Initial Code

1. User describes the task: "şu işi yapan Python kodu yaz" or equivalent
2. **Do not ask clarifying questions unless the spec is impossible to implement.** If something is ambiguous, make a reasonable assumption, note it in a comment, and proceed.
3. Write the Python file to Desktop (preferred location for quick access):
   ```
   C:\Users\eymen\Desktop\<script_name>.py
   ```
4. Lint check: silently fix any syntax/lint issues before first run — don't mention it unless there's a structural problem.

### Phase 2: Run & Auto-Capture

5. Run directly in terminal:
   ```
   cd /c/Users/eymen/Desktop && python <script_name>.py
   ```
6. Capture ALL output — both stdout and stderr.

### Phase 3: Analyze & Fix (no user involvement)

7. If output contains errors (traceback, exceptions, wrong results):
   - Analyze the error directly (you are the debugger — don't delegate to Claude Code)
   - Fix the code, write the updated file
   - Re-run
   - **Do not ask the user for permission to retry**
   - **Do not summarize each iteration**
   - Loop silently until clean output

8. If output succeeds but looks wrong (e.g., wrong IP, missing data, incorrect logic):
   - Diagnose the root cause (wrong interface selected, wrong subnet scanned, permissions issue, etc.)
   - Fix the approach, not just the error message
   - Re-run and verify

### Phase 4: Deliver Results

9. When the script produces correct output:
   - Show the user the final output clearly (formatted nicely)
   - Save results to a companion text file when useful (e.g., `<script>_sonuc.txt`)
   - One-line summary of what was accomplished — no iteration history

### Phase 5: Optional VS Code Open

10. If the user says "VS Code'da aç" or asks to see the code:
    ```
    code <script>.py
    ```
    Otherwise assume they don't need VS Code open.

## Common Fix Patterns for Windows

### Wrong network interface selected
- Problem: Script picks VirtualBox IP (192.168.56.x or 192.168.37.x) instead of WiFi IP (192.168.0.x)
- Fix: Use PowerShell WMI directly:
  ```
  Get-CimInstance Win32_NetworkAdapter -Filter 'NetEnabled=True AND Name LIKE "%%Wi-Fi%%"' | Get-CimAssociatedInstance -ResultClassName Win32_NetworkAdapterConfiguration | Select-Object IPAddress, IPSubnet
  ```

### Ping blocked by Windows Firewall
- Problem: No devices respond to ping (0 active results)
- Fix: Switch to ARP-based scanning instead of ping. Send ARP queries with `ping -n 1 -w 200` then immediately read `arp -a` before the cache expires.

### Permission issues
- Problem: ARP table empty or "Access denied"
- Fix: The script needs admin rights. Note in output but don't abort — try reading ARP without admin first (often partial data works).

## Pitfalls

- **Do not loop more than 5-6 times silently.** If after 5 iterative fixes the code still fails, stop and present a clear diagnostic to the user: "Bu yaklaşımla çözülmüyor, sebebi: [reason]. Alternatif: [suggested approach]."
- **PowerShell quoting in Git Bash:** PowerShell commands with `$` signs break in Git Bash. Either: (a) escape `$` with `\$`, (b) use single quotes around the PowerShell block, or (c) use base64 encoding for complex commands.
- **Long-running scripts:** Use `timeout` parameter appropriately. WiFi scans need 60-120 seconds. Set expectations via a progress message before starting.
- **ARP cache is fast-expiring on Windows.** If you clear ARP (`arp -d`), run the scan immediately after or the cache repopulates from stale entries.
- **Confidence heuristic for network results:** If ARP returns devices but ping returns 0, the data is still valid (ARP shows actual past connections) — present it and explain the firewall limitation.

## Verification

After all fixes applied and script runs cleanly:
1. Final output is correct and complete
2. Results file saved to Desktop if useful
3. User is notified with clean formatted results — no debug history

## Related Skills

- `systematic-debugging` — 4-phase root cause debugging for complex bugs
- `nexus-core` — OMEGA framework for response structure
- `kod-yaz-calistir-hata-ayikla-dongusu` — Legacy name; same class of work, kept for backward compatibility. This skill (`python-oto-debug-dongusu`) is the maintained version.

## References

- `references/turkiye-siteleri-bot-korumasi.md` — Bot-protected Turkish sites (sahibinden, etc.): what works and what doesn't, with Playwright, n8n, and fallback strategies.
