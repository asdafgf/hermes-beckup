markdown
# SKILL.md

name: install-domain-controller
description: A step-by-step guide to installing a Domain Controller on Windows Server 2022.

body:
1. **Set Up Virtualization Environment**: Ensure you have a virtualization software like VMware Workstation running.
   
2. **Create a Server Folder**: Open your hypervisor and create a new folder named "servers" to organize your virtual machines.

3. **Clone Windows Server 2022 VM**: Clone your existing Windows Server 2022 machine into the "servers" folder, naming the new instance as "dc1" (Domain Controller 1).

4. **Start the VM**: Power on the cloned VM to begin the installation of the Domain Controller.

5. **Install VMware Tools** (Optional): If not already installed, consider installing VMware Tools on the server for better performance and functionality.

6. **Access the Command Line**: Log in to the Domain Controller VM and access the command line for further setup.

7. **Explore Remote Access Options**: Optionally, consider setting up SSH or Powershell Remoting for easier management of the Domain Controller.

8. **Run the Domain Controller Installation**: Execute the setup command for the Domain Controller using the command line to initiate the installation process.

9. **Complete Installation**: Follow the on-screen prompts to complete the installation of the Domain Controller on your Windows Server 2022.

category: security