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

def web_enum(domain):
    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')
    banner()
    print(f"{Fore.RED}\n[-] Selected Domain : {domain.upper()}\n")
    print(f"{Fore.YELLOW}[*] Fetching initial info...\n")

    domain_info(domain)
    print('\n')
    
    print(f"{Fore.YELLOW}[*] Running Host Diagnostic...\n")
    print(f"{Fore.LIGHTGREEN_EX}[+] PING")

    if name == 'nt':
        _ = system(f'ping {domain}')

    else:
        _ = system(f'ping -c 4 {domain}')

    print('\n')
    print(f"{Fore.LIGHTGREEN_EX}[+] TRACEROUTE")

    if name == 'nt':
        _ = system(f'tracert {domain}')

    else:
        _ = system(f'traceroute {domain}')
    print('\n')
    
    print(f"{Fore.YELLOW}[*] Whois info...")
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
    print("\n")
    
    print(f"{Fore.YELLOW}[*] Enumerating Sub-domain...\n")
    
def sub_enum(sub, domain):
    sub_url = f'https://{sub}.{domain}'
    
    try:
        sub_try = requests.get(sub_url)
        if sub_try.status_code == 200:
            print(Fore.CYAN+'[+] Discovered sub-domain', ':', Fore.GREEN+sub_url)

    except requests.exceptions.ConnectionError:
        pass
    
def main():
    print(f'{Fore.LIGHTCYAN_EX}[*] Usage: Enter the domain name without <http> or <https>')
    print(f'{Fore.LIGHTCYAN_EX}[*] Example: google.com')
    print(f'{Fore.LIGHTCYAN_EX}[*] Enter the domain name :\n')
    domain = input(f"{Fore.LIGHTMAGENTA_EX}-> ").lower()
    start = time.time()
    web_enum(domain)
    
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
