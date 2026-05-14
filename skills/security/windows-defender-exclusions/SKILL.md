---
name: windows-defender-exclusions
description: "Learn how low-privileged users can access Windows Defender antivirus exclusions and explore methods to detect and mitigate such activities."
version: 1.0
category: security
source: https://youtu.be/fxO1V0mzePQ
tags:
  - cybersecurity
  - windows-defender
  - antivirus-exclusions
  - low-privileged-users
body: |
  ## Introduction

  Recently, a group of security experts raised an issue regarding how low-privileged users can access exclusion paths set in the Windows Defender antivirus. This article will explore this topic and share insights on how to detect and mitigate such activities.

  ## Setting Up the Environment

  To follow along with this guide, you'll need a Windows 11 virtual machine. Set up your environment as described in the video.

  ## Understanding Antivirus Exclusions

  Malware, hackers, thread actors, adversaries, or penetration testers might look for small spots on your file system where antivirus engines won't scan them. These exclusions are set by default in the Windows Defender threat protection settings under Real-time protection > Exclusions.

  ## Adding an Exclusion

  As a local admin, you can add an exclusion to the antivirus engine. For example, adding a folder for your current desktop:

  ```powershell
  Add-MpPreference -ExclusionPath "C:\Users\YourUsername\Desktop"
  ```

  ## Viewing Exclusions

  To view the exclusions, open PowerShell with high privileges (Ctrl + Shift + Enter) and run:

  ```powershell
  Get-MpPreference | Select-Object -ExpandProperty ExclusionPath
  ```

  This will list all exclusion paths. You need admin privileges to view these exclusions.

  ## Tracking Exclusions in Event Logs

  Security experts recommend tracking exclusions through the Windows Event logs. You don't need admin privileges to do this:

  ```powershell
  Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Windows Defender/Operational'; ID=4688}
  ```

  This command will help you detect when new processes are started, which might indicate an attempt to bypass antivirus exclusions.

  ## Conclusion

  Understanding how low-privileged users can access Windows Defender antivirus exclusions is crucial for maintaining system security. By following these steps and monitoring event logs, you can detect and mitigate such activities.