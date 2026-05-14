---
name: fake-notification-hermes-agent
description: A Hermes Agent skill to demonstrate how a hacker might fake notifications on your computer.
version: 1.0
category: security
source: https://youtu.be/wrAFZLa1TAk
tags:
  - cybersecurity
  - hacking
  - notifications
body: |
  ## Introduction

  How often do you get notifications on your computer? You trust them, right? After all, it's your computer from applications you installed. So, they wouldn't be malicious, would they? But, what if a hacker could fake notifications?

  ## The Scenario

  I'm on my Windows 11 virtual machine and I'm going to open up the terminal to have access to PowerShell here.

  ```powershell
  # Accessing the Windows registry using PowerShell
  Get-ChildItem -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Notifications"
  ```

  This will list applications that are able to send notifications. I can see Microsoft Defender, Microsoft Edge, and Cursor installed.

  ## Faking a Notification

  Let's write a script to fake an alert that looks like a regular genuine Microsoft Windows Defender antivirus alert saying, "Ooh, you have malware on your computer."

  ```powershell
  # Importing necessary assemblies for creating toast notifications
  Add-Type -AssemblyName System.Runtime.WindowsRuntime
  [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("YourAppName")

  # Creating the notification content
  $xml = @"
  <toast>
    <visual>
      <binding template="ToastGeneric">
        <text>Your antivirus has detected malware on your computer.</text>
        <text>Click here to scan and remove it.</text>
      </binding>
    </visual>
    <actions>
      <action content="Scan Now" arguments="scan"/>
    </actions>
  </toast>
  "@

  # Creating the toast notification
  $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
  [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastGeneric).ImportXml($xml)

  # Showing the toast notification
  [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("YourAppName").Show($toast)
  ```

  This script uses C# managed assembly capabilities to create a toast notification. The `Add-Type` cmdlet is used to import necessary assemblies, and the `ToastNotificationManager` class is used to create and show the notification.

  ## Conclusion

  By understanding how notifications are registered and faking them, you can better protect your system from potential threats.