name: net-sh-persistence
description: "Learn how to use the 'net sh' Windows command line utility for code execution or persistence, including a guide on setting up Sliver for C2."
version: 1.0
category: security
source: https://youtu.be/lMihdys4jw8
tags:
  - net-sh
  - living-off-the-land
  - code-execution
  - persistence
  - cybersecurity
  - sliver
  - C2-framework

body: |
  ## Introduction to 'net sh' for Code Execution and Persistence

  The 'net sh' command line utility in Windows is a low bin or living off the land technique that can be used for code execution or persistence. This guide will walk you through how this technique works, including setting up Sliver as a C2 framework.

  ## What is 'net sh'?

  'net sh' is a built-in command in Windows that allows for network-related operations. It can be used to execute commands on remote machines or within the same machine's context. This utility has been known for some time and is covered in the MITRE ATT&CK framework.

  ## Setting Up Sliver

  Sliver is a modern C2 (Command and Control) framework that is freely available and accessible. It is built using Go and can be used to manage implants, sessions, and beacons.

  ### Installation

  To get started with Sliver, you can download it using the following command:

  ```bash
  curl -sSL https://raw.githubusercontent.com/BishopFox/sliver/master/install.sh | bash
  ```

  This will install Sliver on your system. Once installed, you can start the Sliver server.

  ### Running the Sliver Server

  To run the Sliver server, use the following command:

  ```bash
  sliver-server
  ```

  This will start the Sliver server and allow you to manage your C2 operations.

  ## Using 'net sh' with Sliver

  Once you have Sliver set up, you can use it to execute commands on remote machines. Here’s a step-by-step guide:

  1. **Spin Up an Agent**: Use Sliver to spin up an agent on the target machine.
  
     ```bash
     sliver-client -t <target-ip> -p <port>
     ```

  2. **Execute Commands**: Once the agent is connected, you can execute commands using Sliver.

     ```bash
     sliver-client -t <target-ip> -p <port> exec "net sh command"
     ```

  ## Conclusion

  The 'net sh' utility in Windows provides a powerful way to perform code execution and persistence. By combining this with a modern C2 framework like Sliver, you can effectively manage your operations and maintain control over target systems.

  For more information on Sliver and its features, refer to the official documentation: [Sliver GitHub Repository](https://github.com/BishopFox/sliver)