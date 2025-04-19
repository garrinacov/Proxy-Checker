import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

DEFAULT_PROXY_SOURCE_URL = {
    "http": "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "socks4": "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "socks5": "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt"
}

TEST_URL = "http://httpbin.org/ip"
TIMEOUT = 8
MAX_WORKERS = 50
OUTPUT_FILE = "live_proxies.txt"


def display_signature():
    print(Fore.CYAN + r"""
░█▀█░█▀▄░█▀█░█░█░█░█░░░░░█▀▀░█░█░█▀▀░█▀▀░█░█░█▀▀░█▀▄
░█▀▀░█▀▄░█░█░▄▀▄░░█░░▄▄▄░█░░░█▀█░█▀▀░█░░░█▀▄░█▀▀░█▀▄
░▀░░░▀░▀░▀▀▀░▀░▀░░▀░░░░░░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀░▀
                Created by Hades
""" + Style.RESET_ALL)


def choose_proxy_type():
    print("\nChoose the proxy type:")
    print("1. HTTP")
    print("2. SOCKS4")
    print("3. SOCKS5")
    print("4. Check ALL (HTTP, SOCKS4, SOCKS5)")

    choice = input("Enter your choice (1/2/3/4): ").strip()
    if choice == "1":
        return ["http"]
    elif choice == "2":
        return ["socks4"]
    elif choice == "3":
        return ["socks5"]
    elif choice == "4":
        return ["http", "socks4", "socks5"]
    else:
        print("Invalid choice, defaulting to HTTP.")
        return ["http"]


def fetch_proxy_list_from_url(url):
    r = requests.get(url, timeout=TIMEOUT)
    r.raise_for_status()
    return [line.strip() for line in r.text.splitlines() if line.strip()]


def fetch_proxy_list_custom():
    print("\nEnter your list of proxies (format: ip:port), type 'done' when finished:")
    proxies = []
    while True:
        entry = input(">> ").strip()
        if entry.lower() == "done":
            break
        if entry:
            proxies.append(entry)
    return proxies


def choose_proxy_source(proxy_type):
    print(f"\nChoose the source for {proxy_type.upper()} proxies:")
    print("1. Use default URL (GitHub)")
    print("2. Enter a custom proxy URL")
    print("3. Manually input proxy list")

    choice = input("Enter your choice (1/2/3): ").strip()
    if choice == "1":
        return fetch_proxy_list_from_url(DEFAULT_PROXY_SOURCE_URL[proxy_type])
    elif choice == "2":
        custom_url = input("Enter custom proxy URL: ").strip()
        return fetch_proxy_list_from_url(custom_url)
    elif choice == "3":
        return fetch_proxy_list_custom()
    else:
        print("Invalid choice, using default.")
        return fetch_proxy_list_from_url(DEFAULT_PROXY_SOURCE_URL[proxy_type])


def detect_proxy(proxy, proxy_type):
    proxy_url = f"{proxy_type}://{proxy}"
    proxies = {"http": proxy_url, "https": proxy_url}
    try:
        resp = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        if resp.status_code == 200:
            return proxy
    except Exception:
        pass
    return None


def main():
    display_signature()
    selected_types = choose_proxy_type()
    all_proxies = []

    for proxy_type in selected_types:
        proxies = choose_proxy_source(proxy_type)
        if not proxies:
            print(Fore.RED + f"The proxy list for {proxy_type} is empty. Skipping.")
            continue

        print(f"\n[+] Checking {len(proxies)} {proxy_type.upper()} proxies with {MAX_WORKERS} threads...\n")
        live = []

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(detect_proxy, p, proxy_type): p for p in proxies}
            for fut in as_completed(futures):
                result = fut.result()
                if result:
                    live.append(result)
                    ip, port = result.split(":", 1)
                    print(Fore.GREEN + f"[✅] {proxy_type} {ip} {port}")
                else:
                    print(Fore.RED + f"[❌] {proxy_type} proxy is not active")

        all_proxies.extend((proxy_type, p) for p in live)

    # Save results for all proxy types
    with open(OUTPUT_FILE, "w") as f:
        for proxy_type, item in all_proxies:
            ip, port = item.split(":", 1)
            f.write(f"{proxy_type} {ip} {port}\n")

    print(Fore.CYAN + f"\n[✓] Done! Found {len(all_proxies)} active proxies. See '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    main()
