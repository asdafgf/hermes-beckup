name: microsoft-365-device-code-fishing
description: A guide on how to perform a device code fishing attack on a Microsoft 365 account.
version: 1.0
category: security
source: https://youtu.be/iRmyJxTffSw
tags:
  - cybersecurity
  - device code authentication
  - phishing
  - microsoft-365
body: |
  ## Introduction

  In this guide, we will demonstrate how to perform a device code fishing attack on a Microsoft 365 account. This technique involves tricking a user into granting access by using the device code authentication method.

  ## Prerequisites

  - A developer tenant for Microsoft 365 (as created in previous videos)
  - Access to a victim's email and calendar
  - Basic knowledge of PowerShell and command-line tools

  ## Steps

  ### Step 1: Create a Developer Tenant

  Ensure you have a developer tenant set up. If not, refer to the previous video for instructions on how to create one.

  ### Step 2: Obtain a Session Token

  Use a social engineering scheme or another method to obtain a session token for the target account. This can be done through phishing emails or other means.

  ```powershell
  # Example PowerShell command to get a session token (hypothetical)
  $sessionToken = Get-M365SessionToken -Email "target@example.com" -Password "password"
  ```

  ### Step 3: Set Up Device Code Fishing

  Use the device code fishing technique to trick the victim into granting access. This involves sending a phishing email with a link that contains the device code.

  ```powershell
  # Example PowerShell command to send a device code fishing email (hypothetical)
  Send-DeviceCodeFishingEmail -TargetEmail "victim@example.com" -DeviceCode "123456"
  ```

  ### Step 4: Monitor for Device Code

  The victim will receive an email with a link. When they click on the link, they will be prompted to enter a device code. Capture this code and use it to authenticate.

  ```powershell
  # Example PowerShell command to capture the device code (hypothetical)
  $deviceCode = Read-Host "Enter the device code"
  ```

  ### Step 5: Authenticate Using Device Code

  Use the captured device code to authenticate as the victim.

  ```powershell
  # Example PowerShell command to authenticate using device code (hypothetical)
  $accessToken = Get-M365AccessToken -DeviceCode $deviceCode
  ```

  ## Conclusion

  This guide demonstrates how to perform a device code fishing attack on a Microsoft 365 account. It is important to understand and mitigate such risks in your organization to protect sensitive data.