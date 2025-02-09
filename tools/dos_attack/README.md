# DoS Attack Tool

This tool simulates a **SYN Flood attack** by sending a high volume of requests to a specified target IP and port.  
It is intended for **educational purposes only** and should **only be used on networks you own or have explicit permission to test**.

## Purpose
The **DoS Attack Tool** is designed to stress-test systems and observe how they handle a flood of requests, helping in understanding network and service limits.

## Usage
```bash
python3 Dos.py --target <IP> --port <PORT> --count <NUM> --threads <THREADS> --rate <RATE>
