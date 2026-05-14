---
name: bite-me-room
description: A step-by-step guide to tackling the Bite Me room on TryHackMe.
version: 1.0
category: security
source: https://youtu.be/vAlkrw-o7m4
tags: [cybersecurity, hacking, TryHackMe, penetration-testing, network-scanning]
---

# Bite Me Room - TryHackMe Guide

## Step 1: Set Up Your Environment
1. Launch your Kali Linux virtual machine.
2. Create a directory for the Bite Me challenge:
   ```bash
   mkdir ~/bite_me
   cd ~/bite_me
   ```

## Step 2: Connect to the TryHackMe VPN
1. Connect to the TryHackMe VPN by running:
   ```bash
   sudo openvpn myuser.openvpn
   ```
2. Ensure you are connected before proceeding.

## Step 3: Start the Bite Me Room
1. Start the Bite Me room on TryHackMe. Take note of the IP address provided for the target machine.

## Step 4: Set Up Your Workspace
1. Create a README file for notes (optional):
   ```bash
   touch README.md
   ```
2. Store the IP address into a variable for easy reference:
   ```bash
   export TARGET_IP=<IP_ADDRESS>
   ```

## Step 5: Scan the Target Machine
1. Create a directory for Nmap scans:
   ```bash
   mkdir nmap
   ```
2. Run an Nmap scan to identify open ports and services:
   ```bash
   nmap -sC -sV -oN nmap/initial_scan.txt $TARGET_IP
   ```
3. To increase verbosity, you can use the `-v` flag:
   ```bash
   nmap -sC -sV -oN nmap/initial_scan.txt -v $TARGET_IP
   ```

## Step 6: Analyze Scan Results
1. From the Nmap output, identify open ports (at least Port 22 for SSH and Port 80 for HTTP).
2. Investigate each service running on these ports to discover potential vulnerabilities.

## Step 7: Capture User and Root Flags
1. Follow the tasks as instructed in the Bite Me room to retrieve the user and root flags.
   - Be sure to note down the flags as you progress.

## Step 8: Document Your Findings
1. As you proceed through the room, document your findings and any strategies that worked or didn't work.
2. Use the README file to keep track of your approach for future reference.

## Conclusion
- Complete the Bite Me room by proving you gained initial access and compromised the machine.
- Review your notes and analyses to solidify your learning experience. 
