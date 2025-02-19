import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import socket
import threading
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
def scan_port(ip, port, timeout, output_text):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((ip, port))

        if result == 0:  # Only show open ports
            banner = grab_banner(ip, port)
            if banner and banner != "No response":
                result_text = f"Port {port} - OPEN - Detected: {banner}\n"
            else:
                service = COMMON_PORTS.get(port, "Unknown Service")
                result_text = f"Port {port} - OPEN - {service}\n"

            # Insert result into GUI output box
            output_text.insert(tk.END, result_text)
            output_text.see(tk.END)  # Auto-scroll

    finally:
        sock.close()

# Function to run the scan
def run_scan(ip, start_port, end_port, timeout, thread_count, output_text):
    output_text.insert(tk.END, f"Scanning {ip} from port {start_port} to {end_port}...\n")
    output_text.see(tk.END)

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, ip, port, timeout, output_text)

    output_text.insert(tk.END, "Scan complete!\n")
    output_text.see(tk.END)

# Function to start scanning when the button is clicked
def start_scan(ip_entry, start_port_entry, end_port_entry, speed_var, output_text):
    ip = ip_entry.get().strip()
    try:
        start_port = int(start_port_entry.get().strip())
        end_port = int(end_port_entry.get().strip())
    except ValueError:
        messagebox.showerror("Input Error", "Ports must be valid numbers!")
        return

    if start_port < 1 or end_port > 65535 or start_port > end_port:
        messagebox.showerror("Input Error", "Invalid port range!")
        return

    # Convert speed selection to timeout & thread count
    speed_settings = {
        "Slow": (1.0, 20),
        "Fast": (0.75, 50),
        "Ultra Fast": (0.25, 100),
    }
    timeout, thread_count = speed_settings.get(speed_var.get(), (1.0, 20))

    # Clear previous results
    output_text.delete(1.0, tk.END)

    # Run scan in a new thread (to keep GUI responsive)
    threading.Thread(target=run_scan, args=(ip, start_port, end_port, timeout, thread_count, output_text), daemon=True).start()

# Function to create the GUI for the Port Scanner
def port_scanner_gui(main_menu):
    root = tk.Toplevel()  # Create a new window
    root.title("Port Scanner")
    root.geometry("500x400")

    # Labels & Input Fields
    tk.Label(root, text="Target IP:").grid(row=0, column=0)
    ip_entry = tk.Entry(root, width=30)
    ip_entry.grid(row=0, column=1)

    tk.Label(root, text="Start Port:").grid(row=1, column=0)
    start_port_entry = tk.Entry(root, width=10)
    start_port_entry.grid(row=1, column=1)

    tk.Label(root, text="End Port:").grid(row=2, column=0)
    end_port_entry = tk.Entry(root, width=10)
    end_port_entry.grid(row=2, column=1)

    # Scan Speed Dropdown
    tk.Label(root, text="Scan Speed:").grid(row=3, column=0)
    speed_var = tk.StringVar(value="Fast")
    speed_menu = ttk.Combobox(root, textvariable=speed_var, values=["Slow", "Fast", "Ultra Fast"])
    speed_menu.grid(row=3, column=1)

    # Output Display
    output_text = scrolledtext.ScrolledText(root, width=60, height=10)
    output_text.grid(row=4, column=0, columnspan=2)

    # Back Button
    def go_back():
        root.destroy()  # Close this window
        main_menu.deiconify()  # Show the main menu

    # Buttons
    tk.Button(root, text="Start Scan", width=15, 
              command=lambda: start_scan(ip_entry, start_port_entry, end_port_entry, speed_var, output_text)).grid(row=5, column=0, pady=10)

    tk.Button(root, text="Back", command=go_back, width=15).grid(row=5, column=1, pady=10)

    root.mainloop()

# Run GUI if executed directly
if __name__ == "__main__":
    port_scanner_gui(None)  # Pass None when running standalone
