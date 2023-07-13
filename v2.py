import concurrent.futures
import requests
import random
import os
import time

red = '\033[91m'  # merah
green = '\033[92m'  # hijau
yellow = '\033[33m' # kuning
cyan = '\033[96m'  # cyan
light_grey = '\033[37m' # putih abu
janda = '\033[35m' # ungu
blank = '\033[0m'  # default

proxy_live = 0
invalid_proxies = 0
total_proxies = 0
live_proxy_types = {"http": 0, "https": 0, "socks4": 0, "socks5": 0}

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
# url = "https://www.speedtest.net/"
# url = "https://ns.cloudflare.com/"
url = "http://api.ipify.org?format=json"

session = requests.Session()


def get_proxy_type(proxy):
    proxy_types = ["http", "https", "socks4", "socks5"]
    for proxy_type in proxy_types:
        try:
            start_time = time.time()
            response = requests.get(
                "http://api.ipify.org?format=json",
                proxies={proxy_type: proxy_type + "://" + proxy},
                timeout=5,
            )
            elapsed_time = round((time.time() - start_time) * 1000)
            if response.status_code == 200 and response.json().get('ip') != None:
                return proxy_type, elapsed_time
        except requests.exceptions.RequestException:
            continue
    return None, None




def check(proxy, idx, total, filename):
    global proxy_live, total_proxies, invalid_proxies
    rand_ua = random.choice(ua)
    session.headers.update({"User-Agent": rand_ua})

    proxy_type, elapsed_time = get_proxy_type(proxy)
    if proxy_type is None:
        print(f"{janda}[x] [{idx}/{total}] {proxy} Proxy is invalid or unreachable.{blank}")
        invalid_proxies += 1
        return

    total_proxies += 1
    try:
        response = session.get(
            url, proxies={proxy_type: proxy_type + "://" + proxy}, timeout=10
        )

        if response.status_code == 200:
            print(f"{green}[#] [{idx}/{total}] {proxy} | {proxy_type.upper()} | 200 OK! | Exec: {elapsed_time}ms {blank}")
            with open(filename, 'a') as file:
                filepath = filename
                if not os.path.isfile(filepath) or proxy not in open(filepath).read():
                    with open(filepath, 'a') as file:
                        file.write(f"{proxy}\n")
            proxy_live += 1
            live_proxy_types[proxy_type] += 1
    except (requests.exceptions.Timeout, requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout):
        print(f"{red}[x] [{idx}/{total}] {proxy} | {proxy_type.upper()} | Error, Bad Proxy!{blank}")




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

def print_elapsed_time(elapsed_time):
    if elapsed_time < 60:
        print(f"Takes time: {round(elapsed_time)} seconds")
    else:
        minutes = round(elapsed_time // 60)
        seconds = round(elapsed_time % 60)
        print(f"Takes time: {minutes} minutes {seconds} seconds")

def main():
    try:
        while True:
            print("Please select a method to check the proxy: ")
            print("1. Check from URLs")
            print("2. Check from .txt file")

            choice = input("\nEnter your option (1/2): ")

            start_time = time.time()

            if choice == '1':
                check_proxies_from_url()
                break
            elif choice == '2':
                check_proxies_from_file()
                break
            else:
                print(f"{red}Invalid choice! Please try again.{blank}\n")

            end_time = time.time()
            elapsed_time = end_time - start_time
            print_elapsed_time(elapsed_time)

    except KeyboardInterrupt:
        proxy_die = total_proxies - proxy_live
        print(f"{cyan}\nDone! Proxy Checked: {total_proxies}")
        print(f"{janda}Invalid Proxies: {invalid_proxies}{blank}")
        print(f"{green}Proxy Live: {proxy_live}{blank}")
        print(f"{red}Proxy Die: {proxy_die}{blank}\n")
        print(f"HTTP: {live_proxy_types['http']}")
        print(f"HTTPS: {live_proxy_types['https']}")
        print(f"SOCKS4: {live_proxy_types['socks4']}")
        print(f"SOCKS5: {live_proxy_types['socks5']}\n")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print_elapsed_time(elapsed_time)

    finally:
        proxy_die = total_proxies - proxy_live
        print(f"{cyan}\nDone! Proxy Checked: {total_proxies}")
        print(f"{janda}Invalid Proxies: {invalid_proxies}{blank}")
        print(f"{green}Proxy Live: {proxy_live}{blank}")
        print(f"{red}Proxy Die: {proxy_die}{blank}\n")
        print(f"HTTP: {live_proxy_types['http']}")
        print(f"HTTPS: {live_proxy_types['https']}")
        print(f"SOCKS4: {live_proxy_types['socks4']}")
        print(f"SOCKS5: {live_proxy_types['socks5']}\n")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print_elapsed_time(elapsed_time)
        print('\n')

if __name__ == "__main__":
    main()
