# Brute Force Tool

This tool performs brute force attacks on specified services like HTTP login forms. It uses a wordlist of username-password combinations to attempt access, helping test the strength of login credentials. **This tool is intended for educational purposes and ethical use only.**

## Purpose
The Brute Force Tool is designed to help penetration testers assess the security of login systems by trying multiple username-password pairs. It’s useful for identifying weak passwords on services where login credentials may be vulnerable.

## Usage
Run the tool from the command line, specifying the target IP, port, service, and wordlist file.

```bash
python brute_force.py --target <TARGET_IP> --port <PORT> --service <SERVICE> --wordlist <WORDLIST_FILE>
