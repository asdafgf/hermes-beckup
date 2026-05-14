markdown
# ExtractMaliciousCodeFromZip

## Description
This skill demonstrates how to analyze a suspicious zip file containing a JavaScript script, identify obfuscated malicious code, and extract it using tools like Remnux, Sublime Text, and Meld.

## Body
1. **Identify the Suspicious Zip File**: A user finds a strange zip file in their downloads folder named "non-compete agreement installment sale 38907 opening agreement". The zip file contains a `.js` script.
2. **Set Up Analysis Environment**:
   - Avoid using Windows for analysis to prevent potential malware execution.
   - Use a Linux distribution and open the terminal.
   - Install Remnux if not already available, as it provides tools for reverse engineering and malware analysis.
3. **Extract the JavaScript File**:
   - Navigate to the directory containing the zip file.
   - Unzip the file using the command `unzip non-compete-agreement-installment-sale-38907-opening-agreement.zip`.
4. **Analyze the JavaScript Script**:
   - Open the extracted `.js` file (e.g., `installmentsale.js`) in Sublime Text.
   - Observe that the script appears to be a legitimate JavaScript library, specifically backbone.js version 1.41.
5. **Identify Malicious Code**:
   - Scroll through the code and notice unusual functions or variables with random names.
   - These are likely obfuscated malicious code inserted into the legitimate library.
6. **Compare with Original Source Code**:
   - Download the original backbone.js version 1.41 from a trusted source (e.g., [backbonejs.org](https://backbonejs.org/)).
   - Use Meld to compare the original and modified files side by side.
7. **Extract Malicious Code**:
   - Identify lines that are present in the modified file but not in the original.
   - Save these differences as a patch file using Meld's "Save As" option.

## Category
Security