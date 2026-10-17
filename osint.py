#!/usr/bin/env python3
import socket
import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

init(autoreset=True)

class ReconSuite:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
        }
        self.platforms = {
            "GitHub": "https://github.com/{}",
            "Twitter/X": "https://x.com/{}",
            "Instagram": "https://www.instagram.com/{}/",
            "Reddit": "https://www.reddit.com/user/{}",
            "Pinterest": "https://www.pinterest.com/{}/",
            "Telegram": "https://t.me/{}",
            "Medium": "https://medium.com/@{}",
            "TikTok": "https://www.tiktok.com/@{}",
            "Steam": "https://steamcommunity.com/id/{}"
        }
        self.top_ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 1433, 3306, 3389, 8080, 8443]

    def _check_target(self, platform, url):
        try:
            r = requests.get(url, headers=self.headers, timeout=4, allow_redirects=True)
            if r.status_code == 200:
                print(f"  [{Fore.GREEN}+{Style.RESET_ALL}] Found: {platform} -> {url}")
        except Exception:
            pass

    def check_username(self, username):
        print(f"\n{Fore.CYAN}[*] Searching targets for: {username}{Style.RESET_ALL}")
        with ThreadPoolExecutor(max_workers=10) as executor:
            for platform, url_pattern in self.platforms.items():
                executor.submit(self._check_target, platform, url_pattern.format(username))

    def ip_recon(self, target):
        print(f"\n{Fore.CYAN}[*] Executing IP Lookup: {target}{Style.RESET_ALL}")
        try:
            res = requests.get(f"http://ip-api.com/json/{target}", timeout=5).json()
            if res.get("status") == "success":
                print(f"  [{Fore.GREEN}IP{Style.RESET_ALL}] {res.get('query')}")
                print(f"  [{Fore.GREEN}Country{Style.RESET_ALL}] {res.get('country')} ({res.get('countryCode')})")
                print(f"  [{Fore.GREEN}City{Style.RESET_ALL}] {res.get('city')}, {res.get('regionName')}")
                print(f"  [{Fore.GREEN}ISP{Style.RESET_ALL}] {res.get('isp')} / {res.get('org')}")
                print(f"  [{Fore.GREEN}ASN{Style.RESET_ALL}] {res.get('as')}")
                print(f"  [{Fore.GREEN}Coords{Style.RESET_ALL}] {res.get('lat')}, {res.get('lon')}")
            else:
                print(f"  [{Fore.RED}!{Style.RESET_ALL}] Failed to retrieve metadata for target.")
        except Exception as e:
            print(f"  [{Fore.RED}!{Style.RESET_ALL}] Connection error: {e}")

    def _scan_port(self, host, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.2)
            if s.connect_ex((host, port)) == 0:
                print(f"  [{Fore.GREEN}OPEN{Style.RESET_ALL}] Port {port}")
            s.close()
        except Exception:
            pass

    def port_scan(self, host):
        print(f"\n{Fore.CYAN}[*] Fast Scanning top ports for: {host}{Style.RESET_ALL}")
        try:
            resolved_ip = socket.gethostbyname(host)
            print(f"  [{Fore.YELLOW}i{Style.RESET_ALL}] Target IP: {resolved_ip}")
            with ThreadPoolExecutor(max_workers=15) as executor:
                for port in self.top_ports:
                    executor.submit(self._scan_port, resolved_ip, port)
        except socket.gaierror:
            print(f"  [{Fore.RED}!{Style.RESET_ALL}] Host resolution failed.")

def main():
    suite = ReconSuite()
    print(f"{Fore.MAGENTA}==========================================")
    print("      RECON-SUITE v2.4 // OSINT FRAMEWORK")
    print(f"=========================================={Style.RESET_ALL}")
    
    while True:
        print("\n1. Social Recon (Username)")
        print("2. IP / Domain Geolocation")
        print("3. Port Recon")
        print("0. Exit")
        
        cmd = input("\nrecon> ").strip()
        
        if cmd == "1":
            user = input("Target Username: ").strip()
            if user:
                suite.check_username(user)
        elif cmd == "2":
            target = input("Target IP/Domain: ").strip()
            if target:
                suite.ip_recon(target)
        elif cmd == "3":
            host = input("Target Host: ").strip()
            if host:
                suite.port_scan(host)
        elif cmd == "0":
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()