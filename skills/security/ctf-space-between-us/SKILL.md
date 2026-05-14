name: ctf-space-between-us
description: A dynamic scoring challenge that requires users to escalate their privileges on a target system.
version: 1.0
category: security
source: https://youtu.be/mEGnhfOX-xs
tags:
  - cybersecurity
  - CTF
  - privilege escalation

body: |
  ## Introduction

  In this guide, we will walk through the process of creating and solving a dynamic scoring challenge called "The Space Between Us" for a Capture The Flag (CTF) event. This challenge aims to teach users how to escalate their privileges on a target system.

  ## Challenge Setup

  1. **Create a Virtual Machine**: Set up a Kali Linux virtual machine.
  2. **Install Necessary Tools**: Install tools such as `nmap`, `metasploit`, and any other required software for the challenge.
  3. **Configure the Target System**: Create a target system with vulnerabilities that can be exploited to escalate privileges.

  ## Challenge Description

  The challenge is titled "The Space Between Us" and is categorized under Miscellaneous. It has a medium difficulty level and dynamic scoring, bringing the point value down to 100-120 points after the competition.

  **Challenge Prompt**: Escalate your privileges on the target system and return the root flag.

  ## Solution Steps

  1. **Initial Enumeration**:
     - Use `nmap` to scan the target system for open ports.
       ```bash
       nmap -sV <target_ip>
       ```
     - Identify any services running on the target that could be exploited.

  2. **Exploitation**:
     - Based on the enumeration, identify a vulnerable service and use appropriate exploitation techniques (e.g., Metasploit modules).
       ```bash
       msfconsole
       use exploit/<exploit_module>
       set RHOSTS <target_ip>
       exploit
       ```

  3. **Privilege Escalation**:
     - Once the initial shell is obtained, look for ways to escalate privileges (e.g., using `sudo -l` to check for misconfigurations).
     - Use techniques like privilege escalation exploits or misconfigured services to gain root access.

  4. **Retrieve the Flag**:
     - After gaining root access, navigate to the directory containing the flag and retrieve it.
       ```bash
       cat /root/flag.txt
       ```

  ## Conclusion

  "The Space Between Us" is a dynamic scoring challenge that teaches users how to escalate their privileges on a target system. By following the steps outlined in this guide, you can successfully complete the challenge and learn valuable skills in cybersecurity.

  For more information on CTFs and cybersecurity, visit [Plex Track](https://www.plextrack.io/).