name: avoid-iex-powershell
description: A guide on how to execute PowerShell code without using the iex or invoke-expression commands.
version: 1.0
category: security
source: https://youtu.be/Y3fi9pc81NY
tags:
  - cybersecurity
  - penetration-testing
  - vulnerability-assessment
  - offensive-security
body: |
  ## Introduction

  Twitter is an incredible resource for the information security community, where people share recent threat research, vulnerabilities, exploits, new tools, tips, and techniques. One of these great content creators is Al, who has recently been sharing some super cool nuggets that include syntax techniques and tricks you can use for penetration testing, vulnerability assessments, and offensive security.

  ## Avoiding iex or Invoke-Expression

  In this video, we will showcase a technique shared by Al on Twitter to avoid using the `iex` or `invoke-expression` commands within PowerShell. This method allows you to execute PowerShell code without it looking as glaringly obvious.

  ## Steps to Follow

  1. **Open PowerShell**: Start by opening your PowerShell session.
  
  2. **Use Alternative Commands**:
     - Instead of using `iex`, you can use the `[System.Diagnostics.Process]::Start` method to execute a new process that runs PowerShell with the desired command.

     ```powershell
     $command = "your_command_here"
     [System.Diagnostics.Process]::Start("powershell", "-NoProfile -Command ""$command""")
     ```

  3. **Example**:
     - If you want to run `Get-Process`, you can do so as follows:

     ```powershell
     $command = "Get-Process"
     [System.Diagnostics.Process]::Start("powershell", "-NoProfile -Command ""$command""")
     ```

  4. **Explanation**:
     - The `-NoProfile` parameter prevents the loading of the PowerShell profile, which can be useful to avoid any scripts or configurations that might affect your command execution.
     - The `-Command` parameter allows you to pass a string containing the PowerShell commands you want to execute.

  ## Conclusion

  By using alternative methods like `[System.Diagnostics.Process]::Start`, you can execute PowerShell code without relying on `iex` or `invoke-expression`. This method is less obvious and can be useful in scenarios where you need to avoid detection by security tools.

  ## Additional Resources

  - [Plex Track](https://jh.io/track) - A premier cyber security reporting and collaboration platform.
  - [Al Hasred's Twitter Profile](https://twitter.com/alhasred) - Follow Al for more cybersecurity tips and tricks.
```

This YAML frontmatter and body provide a structured guide on how to avoid using `iex` or `invoke-expression` in PowerShell, along with additional resources for further learning.