---
name: create-admin-accounts
description: A guide to creating local admin accounts in an Active Directory environment.
version: 1.0
category: security
source: https://youtu.be/yIXTPpluHVo
tags: [active-directory, powershell, admin-accounts, cybersecurity, red-team]
---

# Step-by-Step Guide to Creating Local Admin Accounts

1. **Initialize the Environment**
   - Open your management client for the Active Directory environment.
   - Ensure you are logged in as an administrator to have the necessary privileges.

2. **Access PowerShell**
   - Launch PowerShell with administrative rights to modify the Active Directory settings.

3. **Modify Existing Scripts**
   - Navigate to the PowerShell script you have been using to generate your Active Directory users.
   - Open the script in a code editor like Visual Studio Code for easy modifications.

4. **Add Functionality to Create Local Admin Accounts**
   - Update your script to include a function or property that allows the addition of domain users to a local admin group.

5. **Define Parameters**
   - Utilize PowerShell parameters to customize the number of users and groups you wish to create. 
   - Example syntax to add parameters:
     ```powershell
     param (
         [int]$NumberOfUsers = 8,
         [int]$NumberOfGroups = 1
     )
     ```

6. **Generate User Accounts**
   - Implement logic in your script to create the specified number of users.
   - Ensure these users are configured as local admin accounts on the designated machines.

7. **Test the Setup**
   - Test the script to verify users are created successfully and added to local admin groups.
   - Utilize commands like `Get-LocalGroupMember` to check the local group memberships.

8. **Clean Up the Environment**
   - If needed, remove any test users or modify your Active Directory environment as required.
   - Ensure that the environment setup is as intended for your future testing or exploration.

9. **Documentation and Cleanup**
   - Document any changes made to the scripts for future reference.
   - Ensure your Active Directory environment remains secure and organized after modifications.

10. **Further Exploration**
    - Dive deeper into scripting with PowerShell and explore further modifications or tools that can enhance the management of your Active Directory environment.