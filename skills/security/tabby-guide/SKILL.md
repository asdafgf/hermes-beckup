---
name: tabby-guide
description: A step-by-step guide for exploiting the Tabby machine from Hack The Box.
version: 1.0
category: security
source: https://youtu.be/UQOJOFWjQr0
tags: [hackthebox, tabby, penetration-testing, cybersecurity, nmap]
---

# Step-by-Step Guide to Exploit the Tabby Machine

## Step 1: Setup VPN
- Connect to the Hack The Box VPN to access the target machine.

## Step 2: Create Directories
- Open your terminal.
- Create a directory for your work:
  ```bash
  mkdir ~/youtube
  cd ~/youtube
  ```

## Step 3: Create a README File
- Create a README file for your notes:
  ```bash
  touch README.md
  echo "# Tabby Machine" >> README.md
  echo "Date: November 7, 2020" >> README.md
  ```

## Step 4: Create an Nmap Directory
- Create a directory for Nmap scans:
  ```bash
  mkdir nmap
  cd nmap
  ```

## Step 5: Run Initial Nmap Scan
- Execute an Nmap scan on the target IP:
  ```bash
  nmap -sC -sV -oN initial_scan.txt 10.10.14.194
  ```

## Step 6: Manual Enumeration
- Open a new terminal window for manual enumeration.
- Check for any web services:
  ```bash
  firefox http://10.10.14.194
  ```

## Step 7: Inspect Web Server
- Observe the homepage of the website which appears to be Mega Hosting.
- Note down the contact information provided.

## Step 8: Modify Hosts File
- Edit your `/etc/hosts` file to include the target domain:
  ```bash
  sudo nano /etc/hosts
  ```
- Add the following line:
  ```
  10.10.14.194 megahosting.htb
  ```

## Step 9: Run a Full Nmap Scan
- Perform another Nmap scan to check all ports:
  ```bash
  nmap -p- -oN all_ports_scan.txt 10.10.14.194
  ```

## Step 10: Access Through Domain
- Open your web browser and navigate to:
  ```bash
  http://megahosting.htb
  ```

## Step 11: Examine Links
- Check the available links on the website to identify potential further enumeration opportunities.

## Step 12: Continue Enumeration
- Based on the findings from initial scans and web exploration, proceed with further enumeration techniques specific to the services exposed (SSN, HTTP, etc.).

## Final Step: Extract Information
- After identifying potential vulnerabilities, proceed to exploit them based on your research and findings.
