markdown
# Path Variable Manipulation

## Description
Path variable manipulation is a technique used to escalate privileges by altering system environment variables.

## Body
### Step 1: Setup Environment
- Ensure you are connected to the Try Hack Me network.
- Deploy the machine and wait for it to be ready.

### Step 2: Scanning the Machine
- Open a terminal and navigate to your project directory.
- Run an Nmap scan with the following command:
  ```bash
  nmap -sV -T5 -A -p- <IP_ADDRESS>
  ```
  Replace `<IP_ADDRESS>` with the actual IP address of the machine.

### Step 3: Analyze Scan Results
- Review the Nmap output to identify open ports and services.
- Look for any services that might be vulnerable, such as FTP or SSH.

### Step 4: Exploit Vulnerabilities
- If ProFTPD is running an old version, attempt to exploit it using a known vulnerability. For example:
  ```bash
  ftp <IP_ADDRESS>
  ```
  Try logging in with default credentials or use a brute force tool if necessary.

### Step 5: Escalate Privileges
- Once logged in, check for any misconfigurations or vulnerabilities that can be exploited to escalate privileges.
- Modify the system's PATH environment variable to include directories controlled by an attacker. For example:
  ```bash
  export PATH=/path/to/attacker/directory:$PATH
  ```
  Replace `/path/to/attacker/directory` with a directory containing malicious binaries.

### Step 6: Verify Privilege Escalation
- Run a command that should now execute the attacker's binary due to the modified PATH variable.
- Confirm that you have gained higher privileges on the system.

## Category
Security
