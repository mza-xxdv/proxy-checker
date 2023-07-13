import concurrent.futures
import requests
import random
import os
import time
from colorama import Fore, Style

'''
SC untuk cek proxy live or die dan diwrite/disimpan di suatu file .txt
U know lah proxy fungsi nya buat apaan
Buat kejar jam tayang yutub contoh nya
Bila blm ada modul yg terinstall bisa install manual
Pip install "nama modul"
Sementara tested vscode, kga tau klo via termux
'''

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

# url = "https://www.aparat.com/v/SGc8T" # '''Ganti ini untuk cek website yg lain'''
# url = "https://ns.cloudflare.com/" # '''Ganti ini untuk cek website yg lain'''
url = "http://api.ipify.org?format=json" # '''Ganti ini untuk cek website yg lain'''
proxysource = "https://raw.githubusercontent.com/Bardiafa/Proxy-Leecher/main/proxies.txt" #'''Ganti ini untuk cek proxy yg lain'''


session = requests.Session()
session.headers.update({"User-Agent": 'Mozilla/5.0 (Linux; Android 11; vivo 1918) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.62 Mobile Safari/537.36'})


def check(proxy, idx, total):
    try:
        response = session.get(url, proxies={"http": "http://" + str(proxy), "https": "http://" + str(proxy)}, timeout=10)
        if response.status_code == 200:
            print(f"{Fore.LIGHTGREEN_EX}[#] [{idx}/{total}] Proxy {proxy} 200 OK!{Style.RESET_ALL}")

            ip = proxy.split(":")[0]
            reqview = requests.get('http://ip-api.com/json/' + ip).json()
            ipsaya = reqview['query']
            provider = reqview['as']
            country = reqview['country']
            countrycode = reqview['countryCode']

            # '''write all proxy live file.write(f"{proxy};{country};{provider}\n")'''
            # with open('proxy-live.txt', 'a') as file:
            #     filepath = 'proxy-live.txt'
            #     if not os.path.isfile(filepath) or proxy not in open(filepath).read():
            #         with open(filepath, 'a') as file:
            #             file.write(f"{proxy};{country};{provider}\n")

            # '''write all proxy live only'''
            with open('proxy-only.txt', 'a') as file:
                filepath = 'proxy-only.txt'
                if not os.path.isfile(filepath) or proxy not in open(filepath).read():
                    with open(filepath, 'a') as file:
                        file.write(f"{proxy}\n")
            
            # if country in ["Indonesia", "Singapore", "South Korea"]:
            #     filepath = 'proxy-live.txt'
            #     if not os.path.isfile(filepath) or proxy not in open(filepath).read():
            #         with open(filepath, 'a') as file:
            #             file.write(f"{proxy};{country};{provider}\n")

            # '''ind singapore only'''
            # if country in ["Indonesia", "Singapore"]:
            #     filepath = 'proxy-sg.txt'
            #     if not os.path.isfile(filepath) or proxy not in open(filepath).read():
            #         with open(filepath, 'a') as file:
            #             file.write(f"{proxy}\n")

            # if country in ["Indonesia", "Singapore", "South Korea"]:
            #     with open('proxy-live.txt', 'a') as file:
            #         file.write(f"{proxy};{country}\n")

            # if country in ["Indonesia", "Singapore", "South Korea"]:
            #     filepath = 'proxy-live.txt'
            #     if not os.path.isfile(filepath) or proxy not in open(filepath).read():
            #         with open(filepath, 'a') as file:
            #             file.write(f"{proxy};{country};{provider}\n")

    except (requests.exceptions.ProxyError, requests.exceptions.Timeout, requests.exceptions.ConnectTimeout):
        print(f"{Fore.RED}[x] [{idx}/{total}] Proxy {proxy} Error 404!{Style.RESET_ALL}")

def main():
    proxylist = requests.get(proxysource).text.splitlines()
    random.shuffle(proxylist)
    print(f"\n{cyan}Total number of proxies found: {len(proxylist)}{blank}")
    time.sleep(2)
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        for idx, proxy in enumerate(proxylist, start=1):
            executor.submit(check, proxy, idx, len(proxylist))

    print(os.linesep)
    print("Done!")  

if __name__ == "__main__":
    main()

