**name:** analyze-malware

**description:** A step-by-step guide on how to analyze a malicious software sample.

**body:**
1. **Download the Malware Sample**: Start by downloading the `booking ID verification.exe` file from the fake booking.com interface.
2. **Initial Analysis**: Use a static analysis tool like VirusTotal or an offline antivirus scanner to get an initial assessment of the malware. This will help you understand if it's malicious and what type of malware it is.
3. **Disassembly with Ghidra**: Open the `booking ID verification.exe` file in Ghidra, a reverse engineering tool. Analyze the main function to understand the flow of the program and identify any suspicious operations or API calls.
4. **Behavioral Analysis**: Run the malware in a sandbox environment like Cuckoo Sandbox or Volatility to observe its behavior. This will help you see how it interacts with the system, network, and files.
5. **File Inspection**: Check for any embedded resources or hidden files within the executable that might contain additional payloads or configuration data.
6. **Registry Analysis**: Look at the registry keys created by the malware. Commonly, malware may create entries in `HKEY_CURRENT_USER\Software` or `HKEY_LOCAL_MACHINE\SOFTWARE`.
7. **Network Traffic**: Analyze network traffic using tools like Wireshark to see if the malware attempts to communicate with external servers or download additional components.
8. **Persistence Mechanisms**: Identify any persistence mechanisms used by the malware, such as modifying startup entries in the registry or creating scheduled tasks.
9. **Flag Location**: Search for the `flag.ext` file within the system or on network shares that the malware might have accessed during its execution.
10. **Cleanup and Reporting**: Once you locate the flag, clean up any traces of the malware and document your findings for further analysis.

**category:** security