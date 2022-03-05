from requests.models import Response
from bs4 import BeautifulSoup
from os import system, name
from colorama import Fore
import colorama
import requests
import socket
import json
import time
import os
import asyncio
import aiohttp

session = aiohttp.ClientSession(trust_env=True)

async def run(name):

    colorama.init(autoreset=True)


    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')


    print(f"""{Fore.BLUE}
    __        __     _             _____                                             _               
    \ \      / /___ | |__         | ____| _ __   _   _  _ __ ___    ___  _ __  __ _ | |_  ___   _ __ 
     \ \ /\ / // _ \| '_ \  _____ |  _|  | '_ \ | | | || '_ ` _ \  / _ \| '__|/ _` || __|/ _ \ | '__|
      \ V  V /|  __/| |_) ||_____|| |___ | | | || |_| || | | | | ||  __/| |  | (_| || |_| (_) || |   
       \_/\_/  \___||_.__/        |_____||_| |_| \__,_||_| |_| |_| \___||_|   \__,_| \__|\___/ |_|   
    """)
    time.sleep(2)

    print(f'{Fore.LIGHTCYAN_EX}[*] Usage: Enter the domain name without <http> or <https>')
    print(f'{Fore.LIGHTCYAN_EX}[*] Example: google.com')
    print(f'{Fore.LIGHTCYAN_EX}[*] Enter the domain name :\n')
    domain = input(f"-> ").lower()

    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')

    print(f"{Fore.RED}[-] Selected Domain : {domain.upper()}\n")
    time.sleep(.5)

    t = time.time()
    print(f"{Fore.LIGHTBLUE_EX}[*] Fetching initial info...\n")

    host = socket.gethostbyname(domain)
    print(f"{Fore.GREEN}[+] The IP Address of {domain} is: {host}\n")


    r2 = requests.get('https://ipinfo.io/'+host+'/json')
    info = json.loads(r2.text)

    print(f"{Fore.GREEN}[+] Location...: "+info['loc'])
    print(f"{Fore.GREEN}[+] Region.....: "+info['region'])
    print(f"{Fore.GREEN}[+] City.......: "+info['city'])
    print(f"{Fore.GREEN}[+] Country....: "+info['country']+'\n')

    print(f"{Fore.LIGHTBLUE_EX}[*] Running Host Diagnostic...\n")
    print(f"{Fore.LIGHTGREEN_EX}[+] PING")

    if name == 'nt':
        _ = system(f'ping {host}')

    else:
        _ = system(f'ping -c 4 {host}')

    print('\n')
    print(f"{Fore.LIGHTGREEN_EX}[+] TRACEROUTE")

    if name == 'nt':
        _ = system(f'tracert {host}')

    else:
        _ = system(f'traceroute {host}')
    print('\n')

    print(f"{Fore.LIGHTBLUE_EX}[*] Whois info...")

    whois = f"https://who.is/whois/{domain}"

    response = requests.get(whois)
    soup = BeautifulSoup(response.text , 'html.parser')
    r_info = soup.findAll("div",{"class": "col-md-12 queryResponseBodyValue"})[1]
    print(f'{r_info.text}\n')

    print(f"{Fore.LIGHTBLUE_EX}[*] Enumerating Name Servers...\n")

    NS = f"https://who.is/dns/{domain}"

    NS_data = []
    NS_response = requests.get(NS)
    soup = BeautifulSoup(NS_response.text , 'html.parser')
    NS_info = soup.find("table",{"class": "table"})
    table_body = NS_info.find('tbody')

    rows = table_body.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        NS_data.append([ele for ele in cols if ele])
    print('\n'.join(map(str, NS_data))) 

    print("\n")

    print(f"{Fore.LIGHTBLUE_EX}[*] Enumerating Sub-domain...\n")

    file = open('domains.txt','r')

    name = file.read()
    subs = name.splitlines()
    task = [make_request(sub, domain) for sub in subs]
    await asyncio.gather(*task)
    file.close()
    print('\n')
    done = (time.time()-t) / 60
    print(f'{Fore.LIGHTCYAN_EX}[*] Finished | Scanned in {round(done,2)} minutes...')


async def make_request(sub, domain):
    url = f"https://{sub}.{domain}"
    print("trying url {}".format(url))
    try:
        await session.get(url, timeout=10)
    except requests.ConnectionError:
        print("exception for {}".format(url))
    else:
        print(f"{Fore.GREEN}[+] Discovered subdomain:", url)



if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run(name))