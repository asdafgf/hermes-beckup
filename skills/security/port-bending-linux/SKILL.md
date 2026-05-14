---
name: port-bending-linux
description: A guide on how to perform port bending using Linux, a technique useful for cybersecurity testing and penetration.
version: 1.0
category: security
source: https://youtu.be/d6qtr-rYxXw
tags:
  - cybersecurity
  - linux
  - network
  - hacking
  - penetration-testing
body: |
  ## Introduction to Port Bending

  In the world of computer networking, understanding how IP addresses and ports work is crucial. An IP address can be likened to a physical street address for a house or building, while ports are like doors or windows through which you can interact with services on that host.

  This video will explore port bending, a technique where traffic destined for one port is redirected to another port. This can be useful in cybersecurity testing and penetration to assess vulnerabilities and exploit them effectively.

  ## Theoretical Background

  Port bending involves redirecting network traffic from one port to another. For example, you might want to redirect traffic from `127.0.0.1:80` (localhost on port 80) to `127.0.0.1:8080` (localhost on port 8080).

  ## Practical Example

  To perform port bending in Linux, you can use tools like `iptables`. Here’s a step-by-step guide:

  1. **Install iptables**: Ensure that `iptables` is installed on your system.
     ```bash
     sudo apt-get install iptables
     ```

  2. **Create a Rule for Port Bending**: Use the following command to redirect traffic from port 80 to port 8080.
     ```bash
     sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
     ```

  3. **Save the Rule**: To make sure the rule persists after a reboot, save it using `iptables-save`.
     ```bash
     sudo sh -c "iptables-save > /etc/iptables/rules.v4"
     ```

  ## Testing Port Bending

  After setting up the port bending rule, you can test it by accessing `http://127.0.0.1:80` in your web browser. The traffic should be redirected to port 8080.

  ## Conclusion

  Port bending is a powerful technique for cybersecurity testing and penetration. By redirecting network traffic from one port to another, you can assess vulnerabilities and exploit them effectively. This guide provides a basic introduction to performing port bending using Linux tools like `iptables`.

  For more advanced techniques and ethical hacking practices, consider exploring certifications like the Certified Penetration Tester (CPT) offered by Hack the Box.
```

This YAML frontmatter and body format provide a structured guide on how to perform port bending using Linux, suitable for cybersecurity enthusiasts and professionals.