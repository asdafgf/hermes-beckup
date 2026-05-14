markdown
# Hermes Agent SKILL.md

## Name
hermes-agent

## Description
Hermes Agent is a malware analysis tool designed to analyze and dissect potentially harmful scripts and files, particularly focusing on Windows PowerShell scripts, in a secure and educational environment.

## Body
### Guide: Analyzing Malware Samples with Hermes Agent

Welcome to the Hermes Agent guide! This document will help you get started with analyzing malware samples safely and effectively. In this guide, we will outline some initial steps, tools, and strategies for analyzing malicious scripts, particularly those written for PowerShell.

#### Step 1: Environment Setup
- **Operating System**: It is highly recommended to use a Linux distribution for malware analysis. Distributions such as Remnux or Kali are tailored for this purpose.
- **Terminal Setup**: Use `zsh` as your shell for its enhanced features, such as syntax highlighting. The `exa` command can be used as an alternative to `ls` for a more visually appealing directory listing.
- Install necessary tools for reverse engineering and malware analysis, such as:
  - Ghidra or Radare2 for static analysis
  - Wireshark for packet analysis

#### Step 2: Initial File Inspection
- Begin by identifying the file type. For example, a `.ps1` extension indicates a PowerShell script.
- Execute an initial check using the `file` command in your terminal to understand the properties of the file you are dealing with.

#### Step 3: Static Analysis
- Display the contents of the PowerShell script using a text editor or commands like `cat`, `less`, or `nano`.
- Look for indicators of malicious behavior, such as suspicious function calls, obfuscated code, or commands indicative of exploitation.

#### Step 4: Dynamic Analysis (Virtual Environment)
- Always analyze potentially harmful scripts in a controlled environment such as a virtual machine (VM) to prevent accidental damage to your host operating system.
- Monitor the script's behavior — file changes, network connections, and system modifications — during execution.

#### Step 5: Reporting and Mitigation
- Document your findings, including potential vulnerabilities exploited by the malware, strategies used by the code, and any captured indicators of compromise (IOCs).
- Recommend mitigation strategies based on your analysis, which may include constant monitoring, increasing endpoint security measures, or educating users about potential threats.

#### Additional Learning Opportunities
- Participate in community events such as Capture The Flag (CTF) challenges to improve your skills in a friendly environment. Resources like Sneak's upcoming events can be beneficial for beginners and intermediates alike.

### Conclusion
Understanding malware and how to analyze it is crucial in today's cybersecurity landscape. With the help of Hermes Agent, users can safely explore, learn, and report on the behavior of maliciously crafted scripts. Stay updated and keep learning!

## Category
security
