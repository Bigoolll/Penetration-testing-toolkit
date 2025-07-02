import streamlit as st
import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def validate_ip(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

def grab_banner(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(2)
        sock.connect((ip, port))
        sock.sendall(b"\r\n")
        data = sock.recv(1024).decode(errors="ignore").strip()
        return data or None
    except:
        return None
    finally:
        sock.close()

def scan_port_line(ip, port, timeout):
    s = socket.socket()
    s.settimeout(timeout)
    try:
        if s.connect_ex((ip, port)) == 0:
            banner = grab_banner(ip, port)
            if banner:
                return f"Port {port} - OPEN - Detected: {banner}"
            svc = COMMON_PORTS.get(port, "Unknown Service")
            return f"Port {port} - OPEN - {svc}"
    finally:
        s.close()
    return None

def run_scan(ip, start_port, end_port, timeout, threads):
    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(scan_port_line, ip, port, timeout): port
            for port in range(start_port, end_port + 1)
        }
        for fut in as_completed(futures):
            line = fut.result()
            if line:
                results.append(line)
    return sorted(results, key=lambda l: int(l.split()[1]))

def main():
    st.title("🔍 Port Scanner (Batch Output)")
    ip = st.text_input("Target IP")
    col1, col2 = st.columns(2)
    start_port = col1.number_input("Start Port", min_value=1, max_value=65535, value=1)
    end_port   = col2.number_input("End Port",   min_value=1, max_value=65535, value=1024)
    speed = st.selectbox("Scan Speed", ["Slow","Fast","Ultra Fast"], index=1)

    if st.button("Start Scan"):
        # Input checks
        if not validate_ip(ip):
            st.error("❌ Invalid IP address!")
            return
        if start_port > end_port:
            st.error("❌ Start Port must be ≤ End Port!")
            return

        timeout, threads = {
            "Slow": (1.0, 20),
            "Fast": (0.75, 50),
            "Ultra Fast": (0.25, 100),
        }[speed]

        st.info(f"Scanning {ip}:{start_port}–{end_port} at **{speed}** speed…")
        with st.spinner("Scanning in progress…"):
            results = run_scan(ip, start_port, end_port, timeout, threads)

        # Batch display
        if results:
            st.subheader("Open Ports:")
            for line in results:
                st.text(line)
        else:
            st.warning("No open ports detected.")
        st.success("✅ Scan complete!")

if __name__ == "__main__":
    main()
