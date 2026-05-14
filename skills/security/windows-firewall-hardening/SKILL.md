---
name: windows-firewall-hardening
description: A guide to hardening Windows firewall settings by blocking outbound connections from living off the land binaries.
version: 1.0
category: security
source: https://youtu.be/x7L-F4yDXvI
tags:
  - cybersecurity
  - windows-firewall
  - security-hardening
---

## Introduction

The local Windows firewall is often overlooked, but it can be a powerful tool for securing individual devices within a network. This guide will walk you through an experiment to block outbound connections from living off the land binaries (LOLBINs) on your Windows system.

### Prerequisites

- A Windows device with administrative privileges.
- Basic knowledge of PowerShell and command line operations.

## Experiment Overview

1. **Gather LOLBINs**: Use the [Living Off the Land Binaries](https://lolbas-project.github.io/) resource to identify potential programs that could be abused by attackers.
2. **Create a Block List**: Extract the names and paths of these binaries from the resource.
3. **Configure Windows Firewall**: Block outbound connections for the identified LOLBINs using PowerShell.

## Step-by-Step Guide

### 1. Gather LOLBINs

Visit the [Living Off the Land Binaries](https://lolbas-project.github.io/) website to browse through a catalog of potential programs that could be used by attackers.

### 2. Create a Block List

To create a block list, you can extract the names and paths from the resource. Here’s an example PowerShell script to fetch the data in JSON format:

```powershell
# Fetch the LOLBINs data from GitHub
$url = "https://raw.githubusercontent.com/lolbas-project/Lolbas/master/All.csv"
$csvData = Invoke-WebRequest -Uri $url -UseBasicParsing | ConvertFrom-Csv

# Extract relevant information (e.g., Name and Path)
$blockList = $csvData | Select-Object -Property Name, Path
```

### 3. Configure Windows Firewall

Now that you have your block list, you can configure the Windows firewall to block outbound connections for these programs.

```powershell
# Loop through each entry in the block list and add a rule to the firewall
foreach ($entry in $blockList) {
    $name = $entry.Name
    $path = $entry.Path

    # Create a new firewall rule
    New-NetFirewallRule -DisplayName "Block $name" `
                        -Direction Outbound `
                        -LocalAddress Any `
                        -RemoteAddress Any `
                        -Program $path `
                        -Action Block
}
```

### 4. Verify the Rules

After running the script, verify that the firewall rules have been created successfully.

```powershell
# Get all outbound firewall rules and filter for those related to blocked programs
Get-NetFirewallRule -Direction Outbound | Where-Object { $_.DisplayName -like "*Block*" }
```

## Conclusion

By following this guide, you can enhance the security of your Windows device by blocking outbound connections from living off the land binaries. This experiment provides a practical approach to hardening your firewall settings and making it more difficult for attackers to move laterally within your network.

### Disclaimer

This guide is intended for educational purposes only. Blocking outbound connections for essential programs may prevent normal functionality. Always ensure that you understand the implications of any changes before applying them to your production environment.