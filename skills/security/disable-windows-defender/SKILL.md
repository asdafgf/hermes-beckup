---
name: disable-windows-defender
description: A guide on how to disable Windows Defender, focusing on educational purposes.
version: 1.0
category: security
source: https://youtu.be/HWck6-CnlX8
tags:
  - cybersecurity
  - windows defender
  - anti-virus
  - phishing
  - rdp
body: |
  ## Introduction

  This video showcases how to disable Windows Defender, a popular antivirus software. The goal is not to promote the disabling of security measures but rather to understand how such actions can be taken by threat actors and to highlight the importance of proper cybersecurity practices.

  ## Setting Up the Environment

  - **VMware Workstation**: Used for creating virtual machines.
  - **Windows 11 Base Image**: A fresh installation with VMware tools installed.
  - **Snapshot Manager**: To revert back to a clean state after experiments.

  ## Creating a Low-Privileged User

  - **User Creation**: Create a low-privileged user (e.g., Joe Shmoe) who might have been compromised through phishing or weak passwords.
  - **Reboot**: Restart the machine to ensure all settings are flushed out.

  ## Disabling Windows Defender

  - **Command Prompt as Administrator**: Open Command Prompt with administrative privileges.
  - **Disable Defender**: Use PowerShell commands to disable Windows Defender temporarily for testing purposes.

  ```powershell
  Set-MpPreference -DisableRealtimeMonitoring $true
  ```

  - **Verify Status**: Check the status of Windows Defender to confirm it has been disabled.

  ```powershell
  Get-MpComputerStatus
  ```

  ## Conclusion

  This guide demonstrates how a threat actor might attempt to disable security measures on a target machine. It's crucial to understand such actions and implement robust cybersecurity practices to protect against real-world threats.
```

This YAML frontmatter and body provide a structured guide based on the provided transcript, focusing on educational purposes rather than promoting harmful activities.