markdown
# SKILL.md

## name
create-active-directory-users

## description
A guide to creating Active Directory groups and users on a Windows Server domain controller.

## body
1. **Set Up Your Environment**: Ensure your Windows Server 2022 is configured as a Domain Controller and that you have a workstation joined to the domain.
2. **Access the Management Client**: From your workstation, open the management client capable of connecting to your Domain Controller (DC1).
3. **Navigate to User Management**: Open Active Directory Users and Computers from the server manager to manage users and groups.
4. **Create an Organizational Unit (OU)**: Right-click on your domain and select 'New' > 'Organizational Unit' to organize your users.
5. **Create Groups**: 
   - Right-click on the newly created OU.
   - Select 'New' > 'Group'.
   - Name your group and set the group type (Security or Distribution).
6. **Add Users**:
   - Right-click on the OU again.
   - Select 'New' > 'User'.
   - Fill in the required user attributes (like first name, last name, user logon name).
   - Set a password and configure account options.
7. **Assign Users to Groups**: 
   - Right-click on the group you created.
   - Select 'Add to Group' and add the newly created user.
8. **Test User Access**: Log into a workstation using the new user credentials to verify that the account was set up correctly.
9. **External Resources**: Consider utilizing existing scripts or resources like PowerShell scripts for bulk user creation to streamline the process further.

## category
security