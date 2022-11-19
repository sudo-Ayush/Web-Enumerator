from os import name, system
from colorama import Fore
from tqdm import tqdm
from logic import *
import threading
import colorama
import requests
import time

colorama.init(autoreset=True)

if name == 'nt':
    _ = system('cls')

else:
    _ = system('clear')

banner()

for _ in tqdm(range(100),desc=f"{Fore.LIGHTCYAN_EX}Starting"):
    time.sleep(.01)

if name == 'nt':
    _ = system('cls')

else:
    _ = system('clear')

def initial_info(domain):
    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')
    banner()
    print(f"{Fore.RED}\n[-] Selected Domain : {domain.upper()}\n")
    print(f"{Fore.YELLOW}[*] Fetching initial info...\n")

    domain_info(domain)
    return

def host_diagnostics(domain):   
    print(f"{Fore.YELLOW}\n[*] Running Host Diagnostic...\n")

    if name == 'nt':
        print(f"{Fore.LIGHTGREEN_EX}[+] PING")
        _ = system(f'ping {domain}')
        print(f"{Fore.LIGHTGREEN_EX}\n[+] TRACEROUTE")
        _ = system(f'tracert {domain}')
        print(f"{Fore.LIGHTGREEN_EX}\n[+] NS_LOOKUP\n")
        _ = system(f'nslookup {domain}')

    else:
        print(f"{Fore.LIGHTGREEN_EX}[+] PING")
        _ = system(f'ping -c 4 {domain}')
        print(f"{Fore.LIGHTGREEN_EX}\n[+] TRACEROUTE")
        _ = system(f'traceroute {domain}')
        print(f"{Fore.LIGHTGREEN_EX}\n[+] NS_LOOKUP\n")
        _ = system(f'host {domain}')
    return

def whois_info(domain):
    print(f"{Fore.YELLOW}[*] Whois info...\n")
    whois = f"https://who.is/whois/{domain}"
    response = requests.get(whois)
    soup = BeautifulSoup(response.text , 'html.parser')
    r_info = soup.findAll("div",{"class": "col-md-12 queryResponseBodyValue"})[1]
    print(f'{r_info.text}\n')

    print(f"{Fore.YELLOW}[*] Enumerating Name Servers...\n")

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
    
    print(f"{Fore.YELLOW}\n[*] Enumerating Sub-domain...\n")
    print(f"{Fore.LIGHTCYAN_EX}[+] All Discovered Sub-Domains\n")
    print(f"{Fore.LIGHTMAGENTA_EX}[STATUS]   |     [SUB-DOMAIN]")
    print(f"{Fore.LIGHTWHITE_EX}-"*33)
    
def sub_enum(sub, domain):
    sub_url = f'https://{sub}.{domain}'
    try:
        sub_try = requests.get(sub_url)
        if sub_try.status_code >= 200 and sub_try.status_code < 300:
            print(f"{Fore.LIGHTGREEN_EX}   {sub_try.status_code}     |  ",f"{Fore.GREEN}{sub_url}")
            
        elif sub_try.status_code >= 300 and sub_try.status_code < 400:
            print(f"{Fore.LIGHTCYAN_EX}   {sub_try.status_code}     |  ",f"{Fore.CYAN}{sub_url}")
            
        elif sub_try.status_code >= 400 and sub_try.status_code < 599:
            print(f"{Fore.LIGHTRED_EX}   {sub_try.status_code}     |  ",f"{Fore.RED}{sub_url}")

    except requests.exceptions.ConnectionError:
        pass
    
def main():
    print(f'{Fore.LIGHTCYAN_EX}[*] Usage: Enter the domain name without <http> or <https>')
    print(f'{Fore.LIGHTCYAN_EX}[*] Example: google.com')
    print(f'{Fore.LIGHTCYAN_EX}[*] Enter the domain name :\n')
    
    domain = input(f"{Fore.LIGHTMAGENTA_EX}-> ").lower()
    
    start = time.time()
    initial_info(domain)
    host_diagnostics(domain)
    whois_info(domain)
    
    with open('domains.txt', 'r') as domains:
        domains = domains.readlines()
        
    for sub in domains:
        time.sleep(0.09)
        thread = threading.Thread(target=sub_enum, args= (sub.strip('\n'), domain))
        thread.start()
        
    time.sleep(10)
    done = (time.time()-start) / 60
    print(f"{Fore.LIGHTCYAN_EX}-"*50)
    print(f'{Fore.LIGHTMAGENTA_EX}[*] Finished | Scanned in {round(done - 0.17,2)} minutes...')
    
if __name__ == '__main__':
    main()
