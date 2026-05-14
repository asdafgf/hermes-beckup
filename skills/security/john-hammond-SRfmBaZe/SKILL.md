**name:** Extract and Decode PowerShell Script

**description:** This skill demonstrates how to extract, decode, and analyze a hidden PowerShell script from a seemingly benign file.

**body:**
1. **Identify Suspicious Files**: Begin by identifying files that appear normal but may contain malicious content. In this case, the video shows a directory containing various files including `.exe`, `.ps1`, and `.ini` files.
   
2. **Check File Types**: Use the `file` command to determine the actual type of each file. For example:
   ```bash
   file *.exe
   file *.ps1
   file *.ini
   ```
   This helps in identifying if any files are not what they seem.

3. **Inspect Temporary Files**: Pay special attention to temporary or unusual-named files, such as `.tmp` or `.temp`. In the video, a `.tmp` file is identified as Visual Basic Script code.

4. **Set Syntax Highlighting**: Open the suspicious `.tmp` file in an editor like Sublime Text and set the syntax highlighting to Visual Basic Script. This makes it easier to read and understand the script.

5. **Decode Base64 Content**: Look for any base64-encoded strings within the script. The video shows a comment with seemingly random base64 content that doesn’t decode to anything useful, but it’s good practice to check all encoded data.

6. **Analyze Script Logic**: Identify functions and variables in the script. For example, look for functions like `wdnz tn` or `hjbxz`. Rename these functions and variables for clarity.

7. **Extract File Path**: The script likely contains a file path that needs to be decoded. In the video, a string is identified as a file system path with unusual formatting (e.g., `c:qdd`). Decode this path correctly.

8. **Recreate in Python**: To decode and understand the script better, recreate it in Python. For example:
   ```python
   import base64

   encoded_string = "your_encoded_string_here"
   decoded_string = base64.b64decode(encoded_string).decode('utf-8')
   print(decoded_string)
   ```
   This helps in verifying the decoded content.

9. **Decode PowerShell Script**: If the script contains a command to bypass execution policy and run another script, decode it accordingly. For example:
   ```powershell
   $path = "C:\Path\To\Script.ps1"
   powershell -ExecutionPolicy Bypass -File $path
   ```
   Ensure that any decoded scripts are safe to execute.

10. **Review and Execute**: Review the decoded script for any malicious activity. If it appears benign, you can execute it in a controlled environment.

**category:** security