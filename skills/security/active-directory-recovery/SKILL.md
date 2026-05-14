---
name: active-directory-recovery
description: Guide on recovering an Active Directory environment after joining a new workstation.
version: 1.0
category: security
source: https://youtu.be/B8o6zEngpjk
tags:
  - cybersecurity
  - active-directory
  - recovery
---

# Introduction

In this video, we continue building our Active Directory home lab environment and encounter an issue where joining a new workstation to the domain or logging in with newly created domain accounts fails. We explore a potential solution by reverting the domain controller to a previous state before the new workstation joined the domain.

# Setting Up the Environment

1. **Revert Domain Controller**: 
   - Revert the domain controller (DC) to its initial state after creating the `xyz` domain.
   - Ensure that only one snapshot is available for the DC, which should be taken after the workstation has joined the domain.

2. **Disjoin Workstation**:
   - Disjoin and remove the workstation from the domain.
   - Get back into the domain to create new users and groups.

3. **Management Client Script**:
   - Modify the management client script to accommodate the changes in the Active Directory environment.

# Steps to Recover

1. **Revert DC Snapshot**:
   - Use a snapshot of the DC taken after the workstation has joined the domain.
   - This should allow you to retain the availability and option to log in with the newly created domain users.

2. **Modify Management Client Script**:
   - Update the script to handle any changes or configurations that may have been affected by the previous setup.

3. **Test New Setup**:
   - Join a new workstation to the domain.
   - Log in with the newly created domain accounts to verify that everything is working as expected.

# Conclusion

By reverting the domain controller to a previous state and modifying the management client script, we can recover our Active Directory environment and continue with our cybersecurity exercises. This approach ensures that we have a clean slate to work with while maintaining the ability to log in with the newly created domain users.

For more detailed instructions and code snippets, refer to the GitHub repository linked in the video.