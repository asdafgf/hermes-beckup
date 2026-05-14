---
name: social-engineering-download
description: Learn how to create a simple HTML file with JavaScript to automatically download a file when visited.
version: 1.0
category: security
source: https://youtu.be/KTxsBW9SkOU
tags:
  - cybersecurity
  - social engineering
  - phishing
  - penetration testing
---

## Guide to Creating a Social Engineering Download Script

### Introduction
Have you ever encountered a pop-up while browsing the internet that automatically downloads a file onto your computer without any user interaction? This technique is often used for social engineering and phishing. In this video, we'll show you how to create such a script using HTML and JavaScript.

### Step-by-Step Guide

1. **Set Up Your Environment**
   - Open a Windows 11 virtual machine.
   - Create a new text document on your desktop and rename it `index.html`.
   - Change the view options in File Explorer to show file name extensions.

2. **Create the HTML File**
   - Open `index.html` with a text editor like Visual Studio Code.
   - Start by writing the basic HTML structure:
     ```html
     <!DOCTYPE html>
     <html lang="en">
     <head>
         <meta charset="UTF-8">
         <meta name="viewport" content="width=device-width, initial-scale=1.0">
         <title>Download File</title>
     </head>
     <body>
         <!-- Your content here -->
     </body>
     </html>
     ```

3. **Add JavaScript for Auto-Download**
   - Inside the `<body>` tag, add a script that will trigger the file download when the page loads:
     ```html
     <script>
         window.onload = function() {
             var link = document.createElement('a');
             link.href = 'path/to/your/file.ext'; // Replace with your file path
             link.download = 'file.ext'; // Replace with your desired file name
             document.body.appendChild(link);
             link.click();
             document.body.removeChild(link);
         };
     </script>
     ```

4. **Test Your Script**
   - Open `index.html` in a web browser like Google Chrome, Internet Explorer, or Firefox.
   - Ensure that the file downloads automatically when you visit the page.

### Conclusion
By following these steps, you can create a simple HTML file with JavaScript to automatically download a file when visited. This technique is useful for practicing social engineering and penetration testing skills in a controlled environment.

### Additional Resources
- [YouTube Video](https://youtu.be/KTxsBW9SkOU)
- [HTML Documentation](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [JavaScript Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

Feel free to modify the script and explore different file types for your testing purposes. Always ensure you have permission before performing any actions on someone else's computer.