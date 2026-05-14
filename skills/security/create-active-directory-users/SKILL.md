---
name: create-active-directory-users
description: A guide to creating Active Directory groups and users for domain management.
version: 1.0
category: security
source: https://youtu.be/59VqS6wMn6w
tags: [Active Directory, cybersecurity, domain users, PowerShell, IT management]
---

# Step-by-Step Guide to Creating Active Directory Users

1. **Access the Domain Controller**  
   - Ensure you are logged into a management client that can remotely access the domain controller (DC).

2. **Open PowerShell**  
   - Launch PowerShell as an administrator.
   - This will ensure you have the necessary permissions to create users and groups.

3. **Connect to the Active Directory Module**  
   - Import the Active Directory module by running the following command:  
     ```powershell
     Import-Module ActiveDirectory
     ```

4. **Create Organizational Units (Optional)**  
   - If you want to organize users logically, consider creating Organizational Units (OUs). Use the following command:  
     ```powershell
     New-ADOrganizationalUnit -Name "OU_Name" -Path "DC=yourdomain,DC=com"
     ```

5. **Create an Active Directory Group**  
   - To create a new group, execute the following command:  
     ```powershell
     New-ADGroup -Name "Group_Name" -Path "OU=OU_Name,DC=yourdomain,DC=com" -GroupScope Global
     ```

6. **Add Users to the Group**  
   - Create individual users or add existing users to the newly created group:  
     ```powershell
     Add-ADGroupMember -Identity "Group_Name" -Members "User_Name"
     ```

7. **Creating Active Directory Users**  
   - To create a new user, use the following command:  
     ```powershell
     New-ADUser -Name "User_Name" -GivenName "First_Name" -Surname "Last_Name" -SamAccountName "username" -UserPrincipalName "username@yourdomain.com" -Path "OU=OU_Name,DC=yourdomain,DC=com" -AccountPassword (ConvertTo-SecureString "Password" -AsPlainText -Force) -Enabled $true
     ```

8. **Verify User and Group Creation**  
   - To confirm users and groups have been created successfully, you can run:  
     ```powershell
     Get-ADUser -Filter *
     Get-ADGroup -Filter *
     ```

9. **Documentation and Future Extensions**  
   - Keep a documentation file (JSON or plain text) for reference on group and user structures, enabling future modifications and enhancements.

10. **Exploring Vulnerable Environments**  
    - Optionally, consider exploring a vulnerable Active Directory setup to better understand different attack vectors and how to mitigate them.
   
11. **Final Notes**  
    - Remember to adhere to security best practices when managing user credentials and permissions. Utilize secure passwords and consider user roles within the domain.

By following these steps, you will successfully create and manage Active Directory users and groups, enhancing your domain's functionality and security posture.