---
name: env-hide
description: A guide on using PowerShell and environment variables for obfuscation.
version: 1.0
category: security
source: https://youtu.be/8CiNx4nNqQ0
tags:
  - cybersecurity
  - powershell
  - environment-variables
  - obfuscation
body: |
  ## Introduction

  Hello! Today, we're going to explore a unique technique for hiding or obfuscating PowerShell code using environment variables. This method involves representing different characters as indices inside of an environment variable that has never changed or is unlikely to change.

  ## Understanding Environment Variables in PowerShell

  On Windows, environment variables can be configured and accessed through the PowerShell drive. You can list all environment variables by using the `Get-ChildItem` commandlet:

  ```powershell
  Get-ChildItem Env:
  ```

  This will display a list of all environment variables along with their values.

  ## Identifying Suitable Environment Variables

  Not all environment variables are suitable for obfuscation. Some, like `PATH`, `COMSPEC`, or user-specific variables like `APPDATA`, can change based on the user's configuration. We need to identify variables that remain constant across different environments.

  Common examples of such variables include:
  - `ProgramFiles`
  - `CommonProgramFiles`
  - `SystemRoot`

  ## Creating a PowerShell Script

  Let's create a simple PowerShell script to demonstrate this technique. We'll use Sublime Text Editor or any text editor of your choice.

  ```powershell
  # env-hide.ps1

  $envVariables = @(
      "ProgramFiles",
      "CommonProgramFiles",
      "SystemRoot"
  )

  foreach ($var in $envVariables) {
      $value = [System.Environment]::GetEnvironmentVariable($var)
      Write-Output "$var: $value"
  }
  ```

  This script retrieves and prints the values of specified environment variables.

  ## Obfuscating PowerShell Code

  To obfuscate a piece of PowerShell code, we can represent each character as an index into one of these constant environment variables. For example:

  ```powershell
  $char = [System.Environment]::GetEnvironmentVariable("ProgramFiles")[0]
  ```

  This will retrieve the first character from the `ProgramFiles` environment variable.

  ## Conclusion

  By using environment variables that remain constant across different environments, we can create a simple and effective method for hiding or obfuscating PowerShell code. This technique can be useful in various cybersecurity scenarios where code execution needs to be hidden or masked.