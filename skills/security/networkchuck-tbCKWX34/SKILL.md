markdown
# SKILL.md for Hermes Agent

## Name
hermes-agent-guide

## Description
A comprehensive guide for securely setting up the Frigate surveillance system using Hermes Agent to enhance your privacy and prevent unauthorized access to your surveillance feeds.

## Body
### Introduction
In today's digital age, protecting your privacy is more critical than ever. With surveillance cameras being commonplace, it is essential to ensure that your feeds aren’t being accessed by anyone but you. This guide will cover how to set up the Frigate local surveillance system with Hermes Agent, ensuring your video feeds stay private and secure.

### What is Frigate?
Frigate is an open-source AI surveillance system that operates entirely locally. Unlike many cloud-based surveillance solutions, Frigate does not connect to the internet, ensuring that your data does not leave your premises. This setup offers facial recognition, license plate recognition, object detection, and semantic video search—all while keeping your feeds out of reach from prying eyes.

### Why Use Hermes Agent?
Hermes Agent complements the Frigate system by providing an extra layer of security and enhancing usability. It streamlines the integration of security cameras with the Frigate interface, ensuring smooth operation without compromising on security.

### Getting Started
1. **Install Frigate**:
   - You’ll need a local server; a Raspberry Pi or a laptop running a Linux system will work fine.
   - Install Docker on your chosen server as Frigate runs in a Docker container.

2. **Select Your Cameras**:
   - Choose security cameras that support RTSP. I'm using the RIOlink E1 Pro, which I purchased for its affordability and quick shipping.
   - Ensure that your camera's RTSP link is configured correctly.

3. **Set Up Hermes Agent**:
   - Install the Hermes Agent software on your local server.
   - Configure Hermes Agent to work with your Frigate setup to manage camera connections and enhance security.

4. **Configuration Steps**:
   - Access the Frigate web interface and add your camera feeds.
   - Make sure to test the feeds and ensure they are being recorded locally.
   - Configure notifications and alerts through Hermes Agent to monitor any unauthorized access attempts.

### Security Features
- **Local Processing**: All video processing occurs locally on your server, reducing the risk of your data being mishandled.
- **No Cloud**: Frigate and Hermes Agent do not rely on cloud services, minimizing the potential for hacking.
- **User Friendly**: The combined interfaces make monitoring and managing your surveillance system a breeze.

### Conclusion
By setting up Frigate alongside Hermes Agent, you take big strides toward securing your surveillance setup and enhancing your privacy. This guide serves to empower you to reclaim control over your personal security environment.

**Now go ahead, grab those surveillance cameras, and start securing your digital space!**

### Video Reference
For an in-depth visual walkthrough, check out the video [here](https://www.youtube.com/watch?v=tbCKWX34_G4).
