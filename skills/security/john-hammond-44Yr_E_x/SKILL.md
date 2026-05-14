markdown
# SKILL.md

- name: malware-analysis
- description: A step-by-step guide to analyzing Visual Basic script malware using a Linux virtual machine.
- body: 
  1. Setup a Linux virtual machine where you'll perform the analysis.
  2. Download or obtain the malware sample files, ensuring they are in Visual Basic Script format (.vbs).
  3. Organize your workspace by creating directories for each sample you are analyzing.
  4. Open the first .vbs file using a text editor to examine its contents.
  5. Identify key elements in the script such as ‘WScript’ shells and any indications of PowerShell usage in the code.
  6. Reverse engineer any obfuscated strings found in the script, noting that they could be manipulating PowerShell commands.
  7. Use syntax highlighting in an editor to help you visualize the structure of the script.
  8. Clean the script by removing unnecessary elements or concatenations, which may help clarify the code.
  9. Prepare the script for execution by adding necessary commands that could allow it to run in an isolated environment.
  10. Execute the script in a controlled setting with monitoring tools in place to observe its behavior and effects on the system.
- category: security