---
name: brute-force-password-cracking
description: A guide on how to perform brute force attacks and crack password hashes using Kali Linux.
version: 1.0
category: security
source: https://youtu.be/4X5aoQ8i-_g
tags:
  - cybersecurity
  - hacking
  - brute-force
  - password-cracking
  - ethical-hacking
body: |
  ## Introduction

  In this video, we will explore three methods to crack a password hash using Kali Linux. These methods include brute force attacks, guest passwords, and pass the hash.

  ## Setting Up the Environment

  We are working inside a Kali Linux virtual machine (VM) configured as our attacker HQ. The VM has access to another Linux server running Ubuntu alongside a Windows machine.

  ```bash
  # Display IP address of the Kali Linux machine
  ip addr show eth0
  ```

  ## Brute Force Attack

  We will attempt to brute force the password for an SSH service on the Ubuntu machine. This involves trying every possible combination of characters until we find the correct one.

  ```bash
  # Attempting brute force attack using Hydra
  hydra -l username -P /usr/share/wordlists/rockyou.txt ssh://192.168.1129
  ```

  ## Guest Passwords

  Sometimes, guest passwords or default passwords are used which can be easily guessed.

  ```bash
  # Attempting to login with common guest passwords
  ssh username@192.168.1129 -p 22
  ```

  ## Pass the Hash

  If we have a user's password hash, we can use it to authenticate without knowing the actual password.

  ```bash
  # Using hashcat to crack the hash
  hashcat -m 0 /path/to/hashfile.txt /usr/share/wordlists/rockyou.txt
  ```

  ## Conclusion

  This video demonstrated three methods to crack a password hash: brute force, guest passwords, and pass the hash. Each method has its own use case and potential risks. It's crucial to understand these techniques for ethical hacking and penetration testing.