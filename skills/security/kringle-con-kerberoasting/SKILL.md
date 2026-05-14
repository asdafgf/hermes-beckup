markdown
name: kringle-con-kerberoasting
description: A guide to navigating the Kerberoasting challenge in the SANS KringleCon 2021.
body: |
  This skill guide walks you through the Kerberoasting challenge as part of the SANS KringleCon 2021 holiday hack challenge. The challenge is designed to help you learn and practice your cybersecurity skills in a playful environment. 

  ### Overview of the Challenge
  The goal of this challenge is to obtain a secret research document from a host on the Elf University domain. You need to first register as a student on the Elf U portal, after which you will interact with various characters and complete tasks.

  ### Steps to Complete the Challenge
  1. **Register at Elf U Portal**: Start by signing up as a student on the Elf University portal.
  2. **Find Eve Snowshoes**: Teleport to Santa's office to locate Eve Snowshoes, who will provide you hints and direct you on tasks.
  3. **Complete Terminal Challenges**: Eve challenges you to use `fail2ban` on a terminal challenge known as "cranberry pie". 

  ### Using `fail2ban`
  - The elves need assistance in automating the monitoring of logs to block malicious IP addresses.
  - You need to configure `fail2ban` to detect any IPs that generate 10 or more failure messages within an hour and block them by adding them to the naughty list.
  - Commands to know:
    - `naughty list add [ip_address]` to block an IP.
    - `naughty list dell [ip_address]` to remove an IP from the naughty list.
    - `naughty list list` to view all currently blocked IPs.
  
  ### Important Notes
  - `fail2ban` will not rescan previously viewed logs, meaning updates to the configuration won't apply retroactively. You'll need to manage the log files carefully to ensure all malicious activity is captured.

  Complete the tasks and refer to the resources provided in the challenge to refine your skills and understanding of Kerberos and Active Directory permissions.
category: security