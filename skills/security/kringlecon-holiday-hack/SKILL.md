name: kringlecon-holiday-hack
description: A detailed guide to completing the Kerberos Roasting challenge during the KringleCon event.
version: 1.0
category: security
source: https://youtu.be/KcnVUV-Tsgo
tags: [kerberos, security, fail2ban, kringlecon, holiday-hack]
```

# Step-by-Step Guide to Completing the Kerberos Roasting Challenge

## Objective Overview
This challenge involves obtaining a secret research document from the elf university domain, utilizing a series of tasks focused on detecting malicious activity using Fail2Ban.

## Steps to Complete the Challenge

1. **Register as a Student:**
   - Access the Elf University portal.
   - Sign up and log in to your student account.

2. **Locate Eve Snowshoes:**
   - Navigate to Santa’s office within the Elf University domain.
   - Find Eve Snowshoes and interact with her to gather more information about your tasks.

3. **Understand the Requirements:**
   - Eve will require you to complete a terminal challenge related to Fail2Ban and log analysis.
   - Focus on identifying and blocking malicious IP addresses that engage in suspicious activity.

4. **Access the Cranberry Pie Challenge:**
   - Click on the Cranberry Pie terminal challenge to start.
   - Read through the prompt indicating the need to automate log analysis for elves.

5. **Configure Fail2Ban:**
   - You need to create a configuration to monitor log entries.
   - Set the monitoring path to `/var/log/hohono.log`.
   - Establish criteria: if an IP address generates **10 or more failure messages** within an hour, it needs to be added to the naughty list.

6. **Implement Commands:**
   - Use the following commands in the terminal to manage the naughty list:
     - To add an IP: `naughty list add [IP_ADDRESS]`
     - To remove an IP: `naughty list dell [IP_ADDRESS]`
     - To check the current list: `naughty list list`

7. **Monitor Log Entries:**
   - Ensure that Fail2Ban is configured to look for new log entries continuously.
   - Note: Fail2Ban will not rescan already processed logs after configuration changes.

8. **Perform Testing:**
   - Simulate or cause a few failed accesses to test if the IPs get flagged correctly.
   - Check the naughty list to verify that the correct IP addresses are being added.

9. **Complete the Challenge:**
   - Once you have configured Fail2Ban successfully and identified all malicious IPs, return to Eve with the information derived from your setup.
   - Upon successful completion, collect your hints regarding Kerberos and Active Directory permissions.

10. **Celebrate Your Success:**
    - After finishing the challenge, feel free to share your achievement and insights on social media or during the event.

By following these steps, you'll effectively complete the Kerberos Roasting challenge situated within the context of KringleCon, enhancing your cybersecurity skills while engaging in a fun and educational activity!