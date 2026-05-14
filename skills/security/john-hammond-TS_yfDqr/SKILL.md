markdown
# nmap-scan

**Description:** Perform an initial Nmap scan to enumerate open ports on the target machine.

**Body:**
1. Create a directory for storing Nmap logs:
   ```bash
   mkdir ~/zero_day/nmap
   ```

2. Run an Nmap scan with default scripts and version detection, outputting results to a log file:
   ```bash
   nmap -sV -sC <target_ip> -oN ~/zero_day/nmap/initial_<target_ip>.nmap
   ```
   Replace `<target_ip>` with the actual IP address of the target machine.

3. Wait for the scan to complete and review the results in `~/zero_day/nmap/initial_<target_ip>.nmap`.

**Category:** Security