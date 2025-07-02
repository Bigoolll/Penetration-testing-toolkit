import streamlit as st
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

st.set_page_config(page_title="Dir Enumerator", layout="wide")
st.title("⚡ Fast Directory Enumerator (Threaded)")

st.markdown("""
Enter a target URL and upload a `.txt` wordlist. The scanner uses **50 threads** and a **10-second timeout** per request.
""")

# Inputs
target = st.text_input("Target URL", placeholder="example.com or https://example.com")
wordlist_file = st.file_uploader("Upload wordlist (.txt)", type="txt")

def scan_url(base_url, path):
    url = base_url.rstrip("/") + "/" + path
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 404:
            return (url, resp.status_code)
    except requests.RequestException:
        pass
    return None

if st.button("Start Scan"):
    if not target:
        st.error("Please enter a target URL.")
    elif not wordlist_file:
        st.error("Please upload a wordlist file.")
    else:
        if not target.startswith(("http://", "https://")):
            target = "http://" + target

        st.info(f"Scanning {target} with 50 threads…")
        lines = wordlist_file.read().splitlines()
        paths = [line.decode("utf-8", errors="ignore").strip() for line in lines if line.strip()]
        total = len(paths)
        found = []

        progress = st.progress(0)
        results = []

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(scan_url, target, path): path for path in paths}
            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                if result:
                    found.append(result)
                progress.progress(i / total)

        if found:
            st.success(f"Found {len(found)} valid endpoints:")
            for url, code in found:
                st.write(f"• {url}  (`{code}`)")
        else:
            st.warning("No directories discovered.")

        st.balloons()

st.markdown("""
---
**Pro Tips:**
- Use a `requests.Session()` for better performance with keep-alive.
- Add headers or authentication if needed.
- For large scans, consider writing results to a file or database.
""")
