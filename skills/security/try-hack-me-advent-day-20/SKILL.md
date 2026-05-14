name: try-hack-me-advent-day-20
description: A guide on how to use PowerShell over SSH to navigate through an endpoint and find hidden contents in a cybersecurity challenge.
version: 1.0
category: security
source: https://youtu.be/LrdT2hUM6mw
tags:
  - try-hack-me
  - advent-of-cyber
  - powershell
  - ssh
body: |
  ## Introduction

  Welcome back! In today's video, we're tackling a cybersecurity challenge from Try Hack Me's Advent of Cyber series. The task is to navigate through an endpoint using PowerShell over SSH and find hidden contents in the stockings.

  ## Setup

  - **Platform**: Try Hack Me
  - **Challenge Name**: Power Shelf to the Rescue
  - **Username**: mceager
  - **IP Address**: 10.10.150.130
  - **Password**: rockstar0! (with a zero for elite speak)

  ## Connecting via SSH

  To connect to the remote machine, use the following command in your terminal:

  ```bash
  ssh mceager@10.10.150.130
  ```

  You might be prompted to confirm the connection. Type `yes` and then enter the password.

  ## Launching PowerShell

  Once logged in, you'll see a command prompt (`cmd.exe`). To launch PowerShell, type:

  ```powershell
  powershell
  ```

  Wait for PowerShell to load.

  ## Navigating to Documents

  Use the following command to navigate to the documents folder:

  ```powershell
  Set-Location -Path "C:\Users\mceager\Documents"
  ```

  Alternatively, you can use the alias `cd`:

  ```powershell
  cd C:\Users\mceager\Documents
  ```

  ## Finding Hidden Contents

  Once in the documents folder, look for any hidden contents. The challenge hints that the contents have been hidden within a specific file or directory.

  Use commands like `Get-ChildItem` to list files and directories:

  ```powershell
  Get-ChildItem -Force
  ```

  This will show all items, including hidden ones.

  ## Conclusion

  By following these steps, you should be able to navigate through the endpoint using PowerShell over SSH and find the hidden contents in the stockings. Remember to use verbose commands for clarity and to take advantage of PowerShell's syntax highlighting.

  Happy hacking!