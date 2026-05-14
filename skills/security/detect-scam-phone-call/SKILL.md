---
name: detect-scam-phone-call
description: Detects and isolates potential scam phone calls based on unsaved Notepad notes.
version: 1.0
category: security
source: https://youtu.be/F4mXdm5dqrw
tags:
  - cybersecurity
  - phishing
  - notepad
  - remote-control
body: |
  ## Overview

  This skill is designed to detect and isolate potential scam phone calls by identifying unsaved Notepad notes that contain suspicious content. The skill leverages the Huntress Agent to monitor for such anomalies and take immediate action to prevent the spread of a potential scam.

  ## Steps to Implement

  1. **Monitor Notepad Activity**:
     - Use the Huntress Agent to continuously monitor Notepad activity on endpoints.
     - Identify any unsaved Notepad buffers that contain suspicious content, such as "do not talk to anyone else" or other phrases indicating a potential scam.

  2. **Isolate Infected Hosts**:
     - Upon detecting an infected host, the skill will automatically isolate it from the network using Huntress Agent capabilities.
     - This isolation prevents the scam from spreading to other endpoints on the network.

  3. **Notify Security Operations Team**:
     - The skill will alert the security operations team via Slack or another communication channel.
     - The team can then take further action, such as conducting a phone call to verify the situation and initiate an incident response.

  ## Example Workflow

  ```plaintext
  User receives a scam phone call while using Notepad.
  Huntress Agent detects unsaved Notepad buffer with suspicious content.
  Skill triggers host isolation.
  Security operations team is notified via Slack.
  Team investigates and takes appropriate action.
  ```

  ## Benefits

  - **Early Detection**: Identifies potential scams before they can cause significant damage.
  - **Immediate Isolation**: Prevents the spread of a scam to other endpoints on the network.
  - **Enhanced Security**: Reduces the risk of data loss or further exploitation by malicious actors.

  ## Conclusion

  By leveraging the Huntress Agent and this skill, organizations can enhance their cybersecurity posture and respond more effectively to potential scams. Regularly monitor Notepad activity and take immediate action to isolate infected hosts.
---