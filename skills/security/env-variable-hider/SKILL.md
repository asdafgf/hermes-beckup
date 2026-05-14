name: env-variable-hider
description: A Hermes Agent skill to hide or obfuscate PowerShell code by representing different characters as an index inside of an environment variable.
version: 1.0
category: security
source: https://youtu.be/8CiNx4nNqQ0
tags:
  - cybersecurity
  - powershell
  - environment-variables
  - obfuscation

body: |
  ## Guide to Create a Hermes Agent Skill for Environment Variable Hiding in PowerShell

  ### Introduction
  In this guide, we will create a Hermes Agent skill that allows you to hide or obfuscate PowerShell code by representing different characters as an index inside of an environment variable. This technique can be useful for evading detection and maintaining persistence on compromised systems.

  ### Prerequisites
  - Basic knowledge of PowerShell scripting.
  - Access to a Windows system with administrative privileges.
  - Sublime Text Editor or any other text editor for creating the Python script.

  ### Step-by-Step Guide

  #### Step 1: Research Default Windows Environment Variables
  Start by researching and listing the default environment variables in Windows. You can use PowerShell commands like `Get-ChildItem Env:` to get a list of all environment variables.

  ```powershell
  Get-ChildItem Env:
  ```

  Identify variables that are unlikely to change, such as `CommonProgramFiles`, `AppData`, or `ComSpec`.

  #### Step 2: Create the Python Script
  Create a new Python script named `envh_hi.py` in a directory of your choice.

  ```bash
  mkdir envh_hi
  cd envh_hi
  subl envh_hi.py
  ```

  Open the `envh_hi.py` file and import the necessary modules:

  ```python
  import os
  ```

  Define a list of environment variables that you want to use for hiding or obfuscation. Avoid variables that are likely to change, such as user-specific variables.

  ```python
  env_vars = [
      'CommonProgramFiles',
      'AppData',
      'ComSpec'
  ]
  ```

  Create a function to hide or obfuscate PowerShell code using the selected environment variable:

  ```python
  def hide_powershell_code(powershell_code, env_var):
      hidden_code = ''
      for char in powershell_code:
          index = ord(char) % len(env_var)
          hidden_code += f'${{{env_var}[{index}]}'
      return hidden_code

  if __name__ == "__main__":
      # Example PowerShell code to hide
      powershell_code = "Get-Process"
      env_var = 'CommonProgramFiles'
      hidden_code = hide_powershell_code(powershell_code, env_var)
      print(hidden_code)
  ```

  This script defines a function `hide_powershell_code` that takes a PowerShell command and an environment variable as input. It then obfuscates the command by replacing each character with its index in the environment variable.

  #### Step 3: Test the Script
  Run the script to test if it works correctly:

  ```bash
  python envh_hi.py
  ```

  You should see the obfuscated PowerShell code printed in the console.

  ### Conclusion
  By following this guide, you have created a Hermes Agent skill that allows you to hide or obfuscate PowerShell code using environment variables. This technique can be useful for maintaining persistence and evading detection on compromised systems. Remember to use such techniques responsibly and only in authorized environments.

  For more information on cybersecurity and PowerShell scripting, refer to the following resources:
  - [Microsoft Docs: Environment Variables](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/set)
  - [Hermes Agent Documentation](https://hermes-agent.io/docs)

  Happy coding!