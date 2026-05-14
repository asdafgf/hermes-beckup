---
name: extract-hostname-from-filename
description: Extracts hostname from a filename to identify source machine.
version: 1.0
category: security
source: https://youtu.be/PEy-l6fduHo
tags:
  - cybersecurity
  - malware-detection
  - forensic-analysis
  - Velociraptor
body: |
  ## Guide: Extract Hostname from Filename

  ### Introduction
  This guide demonstrates how to extract a hostname from a filename using Velociraptor, a scalable endpoint detection and response (EDR) tool. The extracted hostname can help identify the source machine in scenarios where malware is suspected.

  ### Prerequisites
  - Access to a Velociraptor server.
  - A target machine with Velociraptor agent installed.
  - Basic understanding of YARA rules and file analysis.

  ### Steps

  1. **Install and Configure Velociraptor Agent**
     Ensure that the Velociraptor agent is installed on the target machine. You can download it from the official Velociraptor GitHub repository or use a package manager if available.

  2. **Create a YARA Rule**
     Create a YARA rule to identify files with hostnames in their filenames. Here’s an example rule:

     ```yara
     rule ExtractHostnameFromFilename {
         meta:
             description = "Extracts hostname from filename"
             author = "Your Name"
             date = "2023-10-01"

         strings:
             $hostname = /([a-zA-Z0-9.-]+)\.exe/

         condition:
             $hostname
     }
     ```

  3. **Configure Velociraptor Hunt**
     Create a hunt in Velociraptor to run the YARA rule across multiple machines.

     ```json
     {
       "name": "Extract Hostname from Filename",
       "description": "Hunt to extract hostname from filenames on target machines.",
       "flows": [
         {
           "flow_name": "Velociraptor.Flow.Yara",
           "args": {
             "yara_rules": [
               "path/to/your/yara/rule.yar"
             ]
           }
         }
       ],
       "tags": ["malware-detection", "forensic-analysis"]
     }
     ```

  4. **Run the Hunt**
     Execute the hunt on your target machines using Velociraptor’s web interface or command-line tool.

  5. **Analyze Results**
     Review the results to identify any files with hostnames in their filenames. The extracted hostnames can help determine the source machine of the malware.

  ### Example Output

  ```json
  {
    "hostname": "example.com",
    "filename": "malware_example.exe"
  }
  ```

  ### Conclusion
  By following this guide, you can effectively extract hostnames from filenames using Velociraptor. This information is crucial for identifying the source machine of malware and can aid in forensic analysis and incident response.

  For more detailed information on Velociraptor and its capabilities, refer to the official documentation: [Velociraptor Documentation](https://velociraptor.readthedocs.io/)
```

This YAML frontmatter and guide provide a structured approach to extracting hostnames from filenames using Velociraptor, which can be useful in cybersecurity scenarios.