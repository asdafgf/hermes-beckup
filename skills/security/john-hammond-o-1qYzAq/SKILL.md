markdown
# hter Exploit Technique

## Description
The `hter` function is a command within vulnerable software that can be exploited to send shell code and establish a reverse shell connection back to the attacker.

## Body
1. **Set Up Environment**:
   - Install Volm server, which is a simple dot exe executable for creating a command-line server.
   - Run `bone_server.exe` to start the server on a Windows 7 virtual machine.

2. **Identify Target IP**:
   - Determine the IP address of the target machine where Volm server is running.

3. **Exploit the Vulnerability**:
   - Use the `hter` function within the vulnerable software.
   - Craft shell code that will send a reverse shell connection back to your attacker's machine.

4. **Establish Reverse Shell**:
   - Once the `hter` function executes, it should establish a reverse shell connection back to your attacker's host.
   - Use tools like netcat or similar to listen for incoming connections and interact with the compromised system.

5. **Post-Exploitation**:
   - Gain control of the machine as the victim and perform further actions based on the objectives of the attack.

## Category
security