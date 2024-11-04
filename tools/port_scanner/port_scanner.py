import socket
import threading

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

        if port == 80 or port == 443:
            sock.sendall(b"HEAD / HTTP/1.1\r\nHost: " + bytes(ip, 'utf-8') + b"\r\n\r\n")
        elif port == 21:
            sock.sendall(b"HELP\r\n")

        banner = sock.recv(1024).decode("utf-8").strip()
        return banner
    except Exception:
        return None
    finally:
        sock.close()

# Function to scan a port and format the output
def scan_port(ip, port, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((ip, port))
        if result == 0:
            # Port is open
            service = COMMON_PORTS.get(port, "Unknown Service")
            print(f"Port {port} - OPEN   - {service}")
            
            # Try to grab a banner and display additional protocol information
            banner = grab_banner(ip, port)
            if banner:
                print(f"  Common Port: {service}")
                print(f"  Banner Grabbing: {banner}")
                
                # Extract additional details if it's HTTP
                if "Date:" in banner:
                    for line in banner.splitlines():
                        if line.startswith("Date:") or line.startswith("Server:") or line.startswith("X-Powered-By:"):
                            print(f"  Protocol Detection: {line}")
            else:
                print(f"  Common Port: {service}")
                print("  Banner Grabbing: No banner retrieved")
        else:
            print(f"Port {port} - CLOSED")
    finally:
        sock.close()

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
    
    # Run scan with multithreading
    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port, timeout))
        threads.append(thread)
        thread.start()
        
        # Control the number of active threads
        if len(threads) >= thread_count:
            for t in threads:
                t.join()
            threads = []
    
    # Ensure all remaining threads complete
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()