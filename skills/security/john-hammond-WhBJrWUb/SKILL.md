**name:** create-local-admins-on-multiple-workstations

**description:** A PowerShell script to create local administrators on multiple workstations within a domain.

**body:**
1. **Prepare Your Environment:**
   - Ensure you have administrative privileges on your management client.
   - Install necessary PowerShell modules if not already installed (e.g., Active Directory module).

2. **Create JSON Configuration File:**
   - Define the schema for your users in a JSON file.
   - Specify which users should be local administrators and assign them to specific workstations.

   Example JSON configuration:
   ```json
   {
     "users": [
       {
         "username": "user1",
         "password": "P@ssw0rd!",
         "local_admin": true,
         "workstation": "ws01"
       },
       {
         "username": "user2",
         "password": "P@ssw0rd!",
         "local_admin": false,
         "workstation": ""
       }
     ]
   }
   ```

3. **Write the PowerShell Script:**
   - Use the JSON configuration file to create local administrators on specified workstations.

   Example PowerShell script:
   ```powershell
   # Import necessary modules
   Import-Module ActiveDirectory

   # Load JSON configuration
   $config = Get-Content -Path "C:\path\to\your\config.json" | ConvertFrom-Json

   # Loop through each user in the configuration
   foreach ($user in $config.users) {
     if ($user.local_admin) {
       # Create local admin account on specified workstation
       Invoke-Command -ComputerName $user.workstation -ScriptBlock {
         param($username, $password)
         net user $username $password /add
         net localgroup administrators $username /add
       } -ArgumentList $user.username, $user.password
     }
   }
   ```

4. **Run the Script:**
   - Execute the PowerShell script on your management client.

5. **Verify Results:**
   - Log in to each specified workstation and verify that the local administrator accounts have been created successfully.

**category:** security