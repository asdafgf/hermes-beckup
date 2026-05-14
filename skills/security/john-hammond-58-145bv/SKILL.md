# Skill: Port Scanning and Enumeration

## Description
This skill guide covers the initial steps in penetration testing, focusing on port scanning and basic enumeration techniques.

## Body
### Step 1: Setup and Preparation
1. **Create Project Directory**: 
   - Create a new directory for your project.
   ```bash
   mkdir gaming_server_room
   cd gaming_server_room
   ```
2. **Initialize README**:
   - Create a simple README file to keep track of notes and observations.
   ```bash
   echo "# Gaming Server Room" > README.md
   ```

### Step 2: Port Scanning
1. **Run Nmap for Open Ports**:
   - Use `nmap` to scan the target IP address and identify open ports.
   ```bash
   nmap -sV <target_ip>
   ```
   - Example output might show ports 22 (SSH) and 80 (HTTP) are open.

### Step 3: Automatic Enumeration
1. **Run Nikto**:
   - Perform a web server scan using `nikto`.
   ```bash
   nikto -h <target_ip>
   ```
2. **Run GoBuster**:
   - Use `gobuster` to perform directory and file enumeration.
   ```bash
   gobuster dir -u http://<target_ip> -w /usr/share/wordlists/dirb/common.txt
   ```

### Step 4: Manual Enumeration
1. **Web Browser Exploration**:
   - Open the target IP in a web browser to explore the website.
   - Example URL: `http://<target_ip>`
2. **Source Code and Static Files**:
   - Inspect the HTML source code for any hidden comments or content.
   - Check static files like CSS, JavaScript, and images for interesting content.

### Step 5: Identify Potential Vulnerabilities
1. **Review Nikto and GoBuster Output**:
   - Analyze the output from `nikto` and `gobuster` to identify potential vulnerabilities.
2. **Check for Hidden Content**:
   - Look for hidden pages, videos, or files that might contain sensitive information.

### Step 6: Document Findings
1. **Update README**:
   - Add findings and observations to the README file.
   ```markdown
   ## Findings
   - Open ports: 22 (SSH), 80 (HTTP)
   - Nikto scan results: [Insert details]
   - GoBuster scan results: [Insert details]
   ```

### Step 7: Next Steps
1. **Further Enumeration**:
   - Based on findings, decide on the next steps for further enumeration or exploitation.
2. **Exploitation Attempts**:
   - If vulnerabilities are identified, attempt to exploit them.

## Category
Security