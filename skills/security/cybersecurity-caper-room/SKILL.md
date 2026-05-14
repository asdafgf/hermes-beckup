name: cybersecurity-caper-room
description: A guide to performing basic penetration testing on a Linux system using the Cod Caper room on Try Hack Me.
version: 1.0
category: security
source: https://youtu.be/2ZZPwwXOH08
tags:
  - cybersecurity
  - penetration-testing
  - linux
  - nmap
  - try-hack-me
body: |
  ## Introduction

  Hello everyone! I'm John Hammond, and welcome back to another Try Hack Me video. In this video, we'll be taking a look at the Cod Caper room, which is a free room guiding you through infiltrating and exploiting a Linux system.

  ## Setting Up

  The Cod Caper room provides a guided environment for learning basic penetration testing skills. We'll start by setting up our environment and understanding the background of the scenario.

  ## Basic Pen Testing Knowledge

  Before diving into the tools, we need to have some basic pen testing knowledge. For this guide, we won't be going through every tool in detail but will focus on essential steps.

  ## Nmap Scanning

  One of the first steps in penetration testing is scanning the target machine for open ports and services. We'll use `nmap` to perform an initial scan.

  ```bash
  # Create a directory for the cod caper room
  mkdir cod-caper
  cd cod-caper

  # Run nmap on the target IP address
  nmap -sV -O <target-ip>
  ```

  The `-sV` flag enables version detection, and the `-O` flag attempts to detect the operating system.

  ## Post-Enumeration

  After scanning, we need to perform post-enumeration tasks. This includes gathering more information about the target machine and identifying potential vulnerabilities.

  ```bash
  # Save nmap scan results to a file
  nmap -sV -O <target-ip> > nmap-scan.txt
  ```

  You can then review the `nmap-scan.txt` file for detailed information about the open ports and services.

  ## Conclusion

  In this guide, we've covered the basics of performing a penetration test using the Cod Caper room on Try Hack Me. We learned how to use `nmap` for scanning and saving the results for further analysis.

  If you have any questions or need further assistance, feel free to ask in the comments below!