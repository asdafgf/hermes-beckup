---
name: cyber2-reverse-engineering
description: Learn how to reverse engineer a .NET application to retrieve sensitive information.
version: 1.0
category: security
source: https://youtu.be/3xPL0vHGKLE
tags:
  - cybersecurity
  - reverse engineering
  - .NET framework
  - walkthrough
body: |
  # Introduction
  Welcome back to another video! Today, we'll be working through a TryHackMe exercise titled "Advent of Cyber2". The objective is to help Elf McGeeger retrieve Santa's password from the TBFC (Toy Box For Christmas) dashboard.

  ## Prerequisites
  Before diving into the walkthrough, make sure you have completed all necessary setup steps. This includes deploying the machine and connecting to the TryHackMe VPN network.

  ## Storyline
  The storyline revolves around Santa getting his password stolen again. Elf McGeeger is tasked with reversing engineering the TBFC application to retrieve the password for Santa.

  ## Steps to Follow

  ### Step 1: Deploy Instances
  - Deploy two instances:
    - One for attacking (e.g., using Remmina)
    - One vulnerable instance attached to this task

  ### Step 2: Connect to RDP Instance
  - Use Remmina or any other RDP client to connect to the RDP instance.

  ### Step 3: Analyze the Application
  - The application is a simple login portal where users can enter their name (e.g., "cm").
  - If the username or password is incorrect, it will display an error message.

  ### Step 4: Disassemble the Application
  - Use tools like IL Spy or dnSpy to disassemble the .NET application.
    - **IL Spy**: Available on Linux and Windows.
    - **dnSpy**: Primarily available on Windows.

  ### Step 5: Reverse Engineering
  - Analyze the decompiled code to understand how the application checks usernames and passwords.
  - Identify any potential vulnerabilities or hardcoded credentials.

  ## Conclusion
  By following these steps, you'll learn how to reverse engineer a .NET application to retrieve sensitive information. This skill is crucial for cybersecurity professionals who need to analyze and secure applications.

  Happy hacking!