---
name: php-directory-traversal
description: "Learn how to exploit PHP's Directory Traversal vulnerability to retrieve the flag."
version: 1.0
category: security
source: https://youtu.be/zK4VsJp3WGQ
tags:
  - php
  - directory traversal
  - cybersecurity
  - ctf
  - bug bounty
body: |
  # PHP Directory Traversal Exploit

  ## Introduction

  PHP is a widely used language for web development, but it has its quirks and edge cases. One such quirk can be exploited to perform a Directory Traversal attack. This video will showcase how you can use this vulnerability in a Capture The Flag (CTF) competition or during penetration testing.

  ## Overview

  In the video, we recreate a challenge from DEFCON 30 where a flag was hidden in a file with a name that matched a specific regular expression pattern. The application allowed users to input a directory path via a GET parameter and then loop through each directory using a `DirectoryIterator` object.

  ## Steps to Exploit

  1. **Understand the Vulnerability**:
     - The flag is stored in a file with a name that matches a regular expression pattern.
     - The application uses a `DirectoryIterator` to traverse directories, which can be exploited if not properly sanitized.

  2. **Recreate the Challenge**:
     - Set up a temporary directory and create a PHP script that mimics the vulnerable application.
     - Host this script on an Apache or Nginx web server.

  3. **Exploit the Vulnerability**:
     - Use a GET parameter to input a path that traverses directories to reach the flag file.
     - The pattern for the flag file name is `flag_[0-9a-f]{15}\.txt`.

  4. **Retrieve the Flag**:
     - Submit the correct directory path to the application, and it will return the contents of the flag file.

  ## Example

  Suppose the flag is stored in a file named `flag_abc123.txt`. To exploit this vulnerability, you would input a GET parameter like:

  ```
  http://example.com/vulnerable.php?dir=../../../../../../etc/passwd
  ```

  This path traversal will allow you to access files outside the web root directory.

  ## Conclusion

  Understanding and exploiting vulnerabilities like Directory Traversal is crucial for cybersecurity professionals. By following these steps, you can learn how to identify and mitigate such risks in your applications.