import concurrent.futures
import requests
import random
import os
import time

red = '\033[91m'  # merah
green = '\033[92m'  # hijau
cyan = '\033[96m'  # cyan
blank = '\033[0m'  # default

print(
    green
    + """
  ____                                    
 |  _ \ _ __ _____  ___   _               
 | |_) | '__/ _ \ \/ / | | |              
 |  __/| | | (_) >  <| |_| |              
 |_|   |_|_ \___/_/\_\\__, |_             
      / ___| |__   ___|___/| | _____ _ __ 
     | |   | '_ \ / _ \/ __| |/ / _ \ '__|
     | |___| | | |  __/ (__|   <  __/ |   
      \____|_| |_|\___|\___|_|\_\___|_|   
                                          
"""
    + blank
)

print(
    cyan
    + """
[ GitHub : https://github.com/mza-xxdv ]
"""
    + blank
)

def import_file(name_file):
    try:
        with open(name_file, 'r') as f_open:
            file = f_open.readlines()
            list = [x.strip() for x in file]
    except:
        print("FILENYA GA ADA BLOKK...\n")
    return list

ua = import_file('ua.txt')
url = "https://www.speedtest.net/"

session = requests.Session()


def get_proxy_type(proxy):
    proxy_types = ["http", "https", "socks4", "socks5"]
    for proxy_type in proxy_types:
        try:
            response = requests.get(
                "http://ip-api.com/json",
                proxies={proxy_type: proxy_type + "://" + str(proxy)},
                timeout=5,
            )
            if response.status_code == 200:
                return proxy_type
        except requests.exceptions.RequestException:
            continue
    return None


def check(proxy, idx, total, filename):
    rand_ua = random.choice(ua)
    session.headers.update({"User-Agent": rand_ua})

    proxy_type = get_proxy_type(proxy)
    if proxy_type is None:
        print(f"{red}[x] [{idx}/{total}] {proxy} Proxy is invalid or unreachable.{blank}")
        return

    try:
        start_time = time.time()
        response = session.get(
            url, proxies={proxy_type: proxy_type + "://" + str(proxy)}, timeout=10
        )
        elapsed_time = round((time.time() - start_time) * 1000)

        if response.status_code == 200:
            print(f"{green}[#] [{idx}/{total}] {proxy} | Type: {proxy_type} | 200 OK! | Exec: {elapsed_time}ms {blank}")
            with open(filename, 'a') as file:
                filepath = filename
                if not os.path.isfile(filepath) or proxy not in open(filepath).read():
                    with open(filepath, 'a') as file:
                        file.write(f"{proxy}\n")

    except requests.exceptions.Timeout:
        if elapsed_time > 2000:
            return
        print(f"{red}[x] [{idx}/{total}] {proxy} | Type: {proxy_type} | Error 404!{blank}")

    except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout):
        print(f"{red}[x] [{idx}/{total}] {proxy} | Type: {proxy_type} | Error 404!{blank}")

def check_proxies_from_url():
    proxysource = input("Input the URL (Ex: https://raw.githubusercontent.com/....)\nURL: ")
    try:
        proxylist = requests.get(proxysource).text.splitlines()
        random.shuffle(proxylist)
        print(f"\n{cyan}Total number of proxies found from URL: {len(proxylist)}{blank}")
        time.sleep(2)
        with concurrent.futures.ThreadPoolExecutor(max_workers=1200) as executor:
            for idx, proxy in enumerate(proxylist, start=1):
                executor.submit(check, proxy, idx, len(proxylist), 'proxy.txt')
    except requests.exceptions.RequestException as e:
        print(f"{red}Unable to retrieve proxies from the URL. Please make sure the URL is correct and try again.{blank}")

def check_proxies_from_file():
    file_path = input("Enter a file name (with a .txt extension)\nFile Path: ")
    try:
        with open(file_path, 'r') as f:
            proxylist = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"{red}The file {file_path} does not exist.{blank}")
        return

    random.shuffle(proxylist)
    print(f"\n{cyan}Total number of proxies found from file: {len(proxylist)}{blank}")
    time.sleep(2)
    with concurrent.futures.ThreadPoolExecutor(max_workers=1200) as executor:
        for idx, proxy in enumerate(proxylist, start=1):
            executor.submit(check, proxy, idx, len(proxylist), 'new-proxy.txt')

def main():
    while True:
        print("Please select a method to check the proxy: ")
        print("1. Check from URLs")
        print("2. Check from .txt file")

        choice = input("\nEnter your option (1/2): ")

        if choice == '1':
            check_proxies_from_url()
            break
        elif choice == '2':
            check_proxies_from_file()
            break
        else:
            print(f"{red}Invalid choice! Please try again.{blank}\n")

    print("\nDone!\n")


if __name__ == "__main__":
    main()
