name: detect-scheduled-tasks-persistence
description: A Hermes Agent skill to detect scheduled tasks that may be used for persistence by threat actors.
version: 1.0
category: security
source: https://youtu.be/GguO_Oc0h5A
tags:
  - cybersecurity
  - malware-detection
  - scheduled-tasks
  - persistence
body: |
  # Detect Scheduled Tasks Persistence

  ## Overview
  This skill helps in identifying scheduled tasks that may be used for persistence by threat actors. These tasks are often placed in the Windows system directory and executed automatically when the computer starts or a user logs in.

  ## Steps to Detect
  1. **Identify Suspicious Files**:
     - Look for files in the `C:\Windows\System32` directory that end with `.ps1`.
     - These files are likely PowerShell scripts used for persistence.

  2. **Analyze Script Content**:
     - Use a text editor like Sublime Text to open and analyze the content of these `.ps1` files.
     - Look for common patterns such as script blocks, aliases (e.g., `ICM`, `GP`), and regular expressions.

  3. **Check Scheduled Tasks**:
     - Verify if any scheduled tasks are set to run at startup or user login.
     - Use PowerShell commands like `Get-ScheduledTask` to list all scheduled tasks and check their triggers and actions.

  ## Example Analysis
  ```powershell
  # List all scheduled tasks
  Get-ScheduledTask

  # Check specific task details
  Get-ScheduledTask -TaskName "SuspiciousTask"

  # Analyze script content of a suspicious file
  Get-Content C:\Windows\System32\ab95.ps1
  ```

  ## Recommendations
  - Regularly review scheduled tasks and their scripts.
  - Implement security policies to restrict the creation and execution of scripts in critical system directories.
  - Monitor for unusual activity related to scheduled tasks.

  ## References
  - [Microsoft Documentation on Scheduled Tasks](https://docs.microsoft.com/en-us/windows-server/administration/task-scheduler/)
  - [Hermes Agent Documentation](https://hermes-agent.io/docs)
```

This YAML frontmatter and guide format skill provides a structured approach to detecting potential persistence mechanisms through scheduled tasks, leveraging common patterns in PowerShell scripts.