name: bad-ransomware-analysis
description: A guide on how to analyze and de-obfuscate a ransomware document using OLE macros present.
version: 1.0
category: security
source: https://youtu.be/2wg4H9RMk3E
tags:
  - ransomware
  - cybersecurity
  - forensics
  - macro-analysis
  - de-obfuscation

body: |
  # Bad Ransomware Analysis Guide

  ## Introduction
  In this video, we'll explore a ransomware challenge from the Hack the Box Business CTF. The objective is to analyze and de-obfuscate a malicious document to find the flag.

  ## Video Content Overview
  - **Objective**: Identify and extract the flag from a ransomware-infected document.
  - **Tools Used**:
    - `ole macros present` for detecting macros in the document.
    - `vba` for examining and de-obfuscating macro code.
  - **Steps**:
    1. Download and unzip the ransomware document.
    2. Use `ole macros present` to detect macros.
    3. Extract the macro code using a text editor.
    4. Analyze and de-obfuscate the VBA code.

  ## Detailed Steps

  ### Step 1: Download and Unzip the Document
  - Download the ransomware document from the provided link.
  - Unzip the downloaded file into a directory named `youtube` within your project structure.

  ```bash
  mkdir -p ~/projects/hack-the-box-business/forensics/bad-ransomware/youtube
  unzip bad_ransomware.zip -d ~/projects/hack-the-box-business/forensics/bad-ransomware/youtube
  ```

  ### Step 2: Detect Macros Using `ole macros present`
  - Install the `ole macros present` tool if not already installed.
  - Use the tool to detect macros in the ransomware document.

  ```bash
  ole-macros-present ~/projects/hack-the-box-business/forensics/bad-ransomware/youtube/bad_ransomware.doc
  ```

  ### Step 3: Extract and Analyze Macro Code
  - Open the macro code using a text editor.
  - The macro code is typically stored in a `.vba` file within the document.

  ```bash
  nano ~/projects/hack-the-box-business/forensics/bad-ransomware/youtube/macro.vba
  ```

  ### Step 4: De-obfuscate the VBA Code
  - Analyze the VBA code to understand its functionality.
  - Look for obfuscated strings and de-obfuscate them if necessary.

  ```vba
  Private Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)
  ```

  The `Sleep` function is used to pause execution for a specified number of milliseconds. This can be useful in understanding the timing behavior of the ransomware.

  ## Conclusion
  By following these steps, you should be able to analyze and de-obfuscate the ransomware document to find the hidden flag. This guide provides a practical approach to handling similar challenges in cybersecurity forensics.

  For more information on cybersecurity and ransomware analysis, visit our [YouTube channel](https://www.youtube.com/channel/UC...).

  Happy hacking!