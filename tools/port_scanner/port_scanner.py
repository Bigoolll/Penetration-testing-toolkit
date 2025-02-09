import socket
import threading
import time
import re
from concurrent.futures import ThreadPoolExecutor

# Common ports and their typical services
COMMON_PORTS = {
    20: "FTP (Data Transfer)",
    21: "FTP (Control)",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3389: "RDP",
    3306: "MySQL",
}

# Function to grab a banner from a port
def grab_banner(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, port))

        # Send a simple newline to trigger a response
        sock.sendall(b"\r\n")

        banner = sock.recv(1024).decode("utf-8").strip()
        return banner if banner else "No response"
    except Exception:
        return "No response"
    finally:
        sock.close()

# Function to scan a port and determine status
def scan_port(ip, port, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((ip, port))

        if result == 0:  # Only show open ports
            banner = grab_banner(ip, port)
            
            if banner and banner != "No response":
                print(f"Port {port} - OPEN - Detected: {banner}")
            else:
                service = COMMON_PORTS.get(port, "Unknown Service")
                print(f"Port {port} - OPEN - {service}")

    finally:
        sock.close()

# Main function to handle input and scanning
def main():
    ip = input("Enter the IP address to scan: ")
    start_port = int(input("Enter the start port: "))
    end_port = int(input("Enter the end port: "))

    # Speed options with corresponding timeout values
    print("\nSelect scan speed:")
    print("1. Slow (default)")
    print("2. Fast (25% faster)")
    print("3. Ultra Fast (75% faster)")
    choice = input("Choose (1/2/3): ")

    if choice == '2':
        timeout = 0.75  # 25% faster (0.75 seconds timeout)
        thread_count = 50
    elif choice == '3':
        timeout = 0.25  # 75% faster (0.25 seconds timeout)
        thread_count = 100
    else:
        timeout = 1.0   # Slow (1 second timeout)
        thread_count = 20

    print(f"\nStarting scan on {ip} from port {start_port} to {end_port} with timeout {timeout}s...\n")

    # Use ThreadPoolExecutor for better threading
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, ip, port, timeout)

if __name__ == "__main__":
    main()
