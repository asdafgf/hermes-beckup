markdown
# skill
name: local-admin-setup
description: This skill focuses on creating local admin accounts in an Active Directory environment to enhance security and manageability.
body: |
  ## Introduction
  In this guide, we will explore how to create local admin accounts in a Windows environment. This is particularly useful for penetration testers and system administrators looking to manage access levels within their Active Directory.

  ## Setting Up Your Environment
  1. **Log into Your Virtual Machine**: Start by accessing your management client VM where you have administrative privileges.
  2. **Open PowerShell**: Launch PowerShell with administrative rights to begin modifying user accounts.

  ## Creating Local Admin Accounts
  1. **Using PowerShell Script**:
     - We will tweak our existing PowerShell script to add a domain user to the local admin group.
     - Use the following PowerShell snippet:
       ```powershell
       param (
           [string]$DomainUser,
           [string]$LocalGroup = "Administrators"
       )

       Add-LocalGroupMember -Group $LocalGroup -Member $DomainUser
       ```
     - Replace `$DomainUser` with the actual username you want to grant local admin rights to.

  2. **Executing the Script**:
     - Run the script by supplying the domain user you are adding to the local admin group.
     - Example:
       ```powershell
       .\YourScript.ps1 -DomainUser "DOMAIN\username"
       ```

  ## Testing and Verification
  - Once executed, verify that the user has been added successfully by checking the local groups.
  - You can check the groups with:
    ```powershell
    Get-LocalGroupMember -Group "Administrators"
    ```

  ## Conclusion
  In this skill, we learned how to create and manage local admin accounts within an Active Directory environment using PowerShell. This process can help to ensure that users have the necessary permissions without compromising security.
category: security