name: jack-b-nimble
description: A privilege escalation challenge where you need to use Nimble, the package manager for the Nim programming language, to gain root privileges and retrieve the contents of the /root flag.
version: 1.0
category: security
source: https://youtu.be/CbceSV5krYQ
tags:
  - privilege-escalation
  - nimble
  - capture-the-flag
body: |
  ## Overview

  This challenge is titled "Jack B Nimble" and falls under the miscellaneous category with a medium difficulty level. Only 86 people solved it during its runtime on NCON Capture The Flag.

  ## Challenge Description

  Jack B is trying to learn Nim, one of the hottest new programming languages, and he's giving you access to his development box. He wants you to learn Nim too and retrieve the contents of the `/root` flag without hacking it.

  ## Steps to Solve

  1. **SSH into the Development Box**:
     - Use SSH to log in to the development box.
     - Credentials: `user/pass`
     - Example command: `ssh user@localhost -p 22`

  2. **Check Permissions**:
   - List your permissions using `pseudo tac L`.
   - You should be able to run commands without a password for another user, Jack.

  3. **Use Nimble**:
   - The challenge name "Jack B Nimble" is a hint that you need to use Nimble.
   - Nimble is the package manager for the Nim programming language.
   - You can initialize a project using `nimble init nimr`.
   - Navigate into the project directory and create a simple Nim file (e.g., `main.nim`) with a "hello world" program.

  4. **Run Nimble**:
   - Use `nimble run` to execute your Nim code as user Jack.
   - This will give you the necessary permissions to escalate your privileges.

  5. **Retrieve the Flag**:
   - Once you have the necessary permissions, retrieve the contents of the `/root` flag.

  ## Example Commands

  ```bash
  ssh user@localhost -p 22
  pseudo tac L
  nimble init nimr
  cd nimr
  echo 'echo "Hello, Nim!"' > main.nim
  nimble run
  ```

  ## Conclusion

  By following these steps, you should be able to escalate your privileges and retrieve the contents of the `/root` flag in this challenge.