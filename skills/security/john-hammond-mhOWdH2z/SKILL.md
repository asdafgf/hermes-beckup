markdown
# SKILL.md for Hermes Agent

## Name
hermes-agent

## Description
This skill allows users to analyze JScript files, identify potential threats, and understand the operation of malicious scripts in a virtualized environment. 

## Body
### Overview
The Hermes Agent skill provides a practical guide on how to investigate JScript artifacts found on Windows systems. The following steps outline how to leverage this skill effectively.

### Steps to Analyze JScript:

1. **Setting Up Your Environment**
    - Ensure you have a terminal or command line interface ready.
    - Use modern code editors like Sublime Text or Visual Studio Code for better visibility of code.

2. **Identifying the Artifact**
    - Locate the suspicious JScript file (e.g., `notepad.js`) in your working directory. This file is not JavaScript, but JScript, which is a scripting language running natively on Windows.

3. **Initial Assessment**
    - Use the `file` command in your terminal to determine the file type and check the encoding.
    - Open the file in your code editor to analyze its contents. Look for unusual variable names and structures that signify obfuscation.

4. **De-obfuscation Process**
    - Create a backup of the original file for reference.
    - Save a copy of the file as `de-obfuscated.js` to edit the contents.
    - Begin to decode or simplify the code to understand its purpose and functionality.

5. **Understanding the Code Structure**
    - Look for variable initializations and string manipulations that may include cryptic or nonsensical data.
    - Check if the script combines strings or utilizes certain operations that look like Powershell commands.

6. **Running the Code in a Safe Environment**
    - If you have a virtual machine with Windows, launch your Powershell instance on it.
    - Alternatively, set up a Linux environment that supports running Powershell scripts.
    - Execute portions of the JScript safely to monitor for any unusual behavior or outputs.

7. **Documentation and Results**
    - Document your findings systematically. Note any unexpected behaviors or functions.
    - Keep track of any command outputs, especially those that appear to manipulate or affect the system state.

### Conclusion
This skill focuses on enhancing your ability to dissect and analyze potentially harmful scripts. By understanding the underlying structure and running the code ethically within a controlled environment, you can mitigate risks and improve your cybersecurity posture.

## Category
security