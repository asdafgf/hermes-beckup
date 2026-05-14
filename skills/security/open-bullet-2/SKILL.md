name: open-bullet-2
description: A guide on how to use Open Bullet 2 for credential stuffing attacks.
version: 1.0
category: security
source: https://youtu.be/oWv50EF0juc
tags:
  - cybersecurity
  - hacking
  - brute-force
  - credential-stuffing
  - automation

body: |
  ## Introduction to Credential Stuffing Attacks

  Credential stuffing attacks involve hackers using stolen username and password credentials from a data breach to attempt to gain unauthorized access to accounts. They automate this process using scripts, tools, or utilities that loop through each username and password combination to see which ones work.

  ## Open Bullet 2 Overview

  Open Bullet 2 is a cross-platform automation suite powered by .NET. It can send requests to target web applications for scraping data, automated parsing, and penetration testing. The tool has a well-documented wiki and can be installed on Windows with either a web client or a desktop application.

  ## Installation and Setup

  - **Windows Installation**: You can install Open Bullet 2 as a web client or a desktop application.
    - Web Client: Provides more flexibility, including remote access.
    - Desktop Application: Offers a more straightforward interface for local use.

  - **Starting the Server**:
    - After installation, start the server. It will serve on port 5000.
    - Open your web browser and navigate to `http://localhost:5000` to see the admin interface.

  ## Configuring Open Bullet 2

  - **Preparing Configurations**: You need to prepare configurations that define how the tool should interact with the target web application.
  - **Creating a Configuration**:
    - Define a configuration that can run like C code, allowing you to add different blocks for solving captchas, having logic, or conditions using different functions.
    - Interact with the browser using utilities like Puppeteer or Selenium.

  ## Workflow and Automation

  - **Drag-and-Drop Workflows**: You can drag and drop workflows to automate tasks such as brute-forcing passwords, scanning websites, and parsing content.
  - **Starting Jobs**: Use these configurations to start jobs for brute-forcing passwords, scanning, or automated penetration testing.

  ## Important Notes

  - **Legal Considerations**: Performing credential stuffing attacks or any malicious activities against systems you do not own is illegal. Always ensure you have permission before conducting such tests.