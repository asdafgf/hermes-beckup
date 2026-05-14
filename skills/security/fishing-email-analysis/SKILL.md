---
name: fishing-email-analysis
description: A detailed guide on analyzing a phishing email and its attachments for cybersecurity professionals.
version: 1.0
category: security
source: https://youtu.be/YWarpd4G5YM
tags: [phishing, malware analysis, cybersecurity, email security]
---

# Step-by-Step Guide to Analyzing a Phishing Email

1. **Setup Your Environment**
   - Use a virtual environment like Remnux, a Linux distribution tailored for reverse engineering malware.
   - Open a terminal using an appropriate shell (for example, Zshell) and split the terminal window for better visibility.

2. **Organize Your Workspace**
   - Create a directory for your analysis (e.g., `fish`) and navigate to it.
   - Ensure that you have all relevant files related to the phishing email in this directory, including screenshots, email content, and any attachments.

3. **Review the Email**
   - Open the email in question and document its content.
   - Take note of the sender's address, subject line, and any suspicious attachments, particularly focusing on any zip files or PDFs.

4. **Examine Attachments**
   - If the email includes a password-protected zip file, attempt to extract its contents using appropriate tools, keeping in mind ethical guidelines and consent if required.
   - For files that you extract, check if any files stand out as executable or potentially malicious.

5. **Scan with VirusTotal**
   - Run any questionable attachments through VirusTotal to see if any security vendors flagged the files as malicious.
   - Document the results to understand the current threat landscape regarding the files received.

6. **Analyze the Content of Attachments**
   - Open and analyze PDFs or documents in a controlled environment (preferably one isolated from your main OS).
   - Pay attention to macros, scripts, or embedded links that may execute malicious actions.

7. **Consult Additional Resources**
   - Research any unfamiliar domains or email addresses associated with the phishing attempt.
   - Check for known reports of similar phishing schemes or malware that may relate to this email.

8. **Record Your Findings**
   - Document the results of your analysis including any notable indicators of compromise (IOCs) and the methods used in the phishing attempt.
   - Consider reaching out to the original sender of the email (if applicable) to discuss your findings.

9. **Report the Phishing Attempt**
   - Inform the relevant authorities or your IT department about the phishing email.
   - Share your analysis to aid in better threat awareness and prevention strategies within your organization or community.

10. **Continuous Learning**
    - Follow industry trends and updates on new phishing tactics to refine your analysis techniques and improve detection rates for future analyses.