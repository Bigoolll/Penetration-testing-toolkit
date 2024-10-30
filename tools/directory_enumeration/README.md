# Directory Enumerator Tool

The Directory Enumerator Tool attempts to find hidden directories or files on a web server by making HTTP requests to a target URL with various common directory names. This tool is useful for web application reconnaissance to discover accessible directories that may reveal additional functionality or sensitive information.

## Purpose
The Directory Enumerator is used in penetration testing to identify accessible directories and files on a web server. It can help locate unprotected or hidden areas of a web application that might contain sensitive information or further entry points.

## Usage
Run the tool from the command line, specifying the target URL and a wordlist of common directory names.

```bash
python directory_enum.py --url <TARGET_URL> --wordlist <WORDLIST_FILE>
