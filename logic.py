from bs4 import BeautifulSoup
from colorama import Fore
import colorama
import requests
import pyfiglet
import random
import socket

colorama.init(autoreset=True)

def banner():
    x = random.randint(0,9)
    
    if x == 0:
        result = pyfiglet.Figlet()
        print(Fore.BLUE + result.renderText("Web-Enum"))
    
    elif x == 1:
        result = pyfiglet.Figlet(font = "slant")
        print(Fore.CYAN + result.renderText("Web-Enum"))

    elif x == 2:
        result = pyfiglet.Figlet(font = "3-d")
        print(Fore.GREEN + result.renderText("Web-Enum"))
        
    elif x == 4:
        result = pyfiglet.Figlet(font = "doh")
        print(Fore.LIGHTBLUE_EX + result.renderText("W-E"))
        
    elif x == 5:
        result = pyfiglet.Figlet(font = "alligator")
        print(Fore.LIGHTYELLOW_EX + result.renderText("Web-E"))
        
    elif x == 6:
        result = pyfiglet.Figlet(font = "bubble")
        print(Fore.LIGHTMAGENTA_EX + result.renderText("Web-Enum"))
        
    elif x == 7:
        result = pyfiglet.Figlet(font = "digital")
        print(Fore.RED + result.renderText("Web-Enum"))
    
    elif x == 8:
        result = pyfiglet.Figlet(font = "isometric1")
        print(Fore.RED + result.renderText("Web-E"))
        
    else:
        result = pyfiglet.Figlet(font = "bulbhead")
        print(Fore.LIGHTRED_EX + result.renderText("Web-Enum"))

def domain_info(domain):
    host = f'https://iplogger.org/ip-tracker/?ip={socket.gethostbyname(domain)}'

    r = requests.get(host)
    soup = BeautifulSoup(r.text, "html.parser")

    data = soup.find_all(class_ = "info-about-ip")
    data = list(data)
    
    for d in data:
        print(Fore.CYAN+d.get_text().split("\n")[2]+"...")
        print(Fore.CYAN+d.get_text().split("\n")[5],'.........:',Fore.GREEN+d.get_text().split("\n")[6].strip())
        print(Fore.CYAN+d.get_text().split("\n")[9],'..........:',Fore.GREEN+d.get_text().split("\n")[10].strip())
        print(Fore.CYAN+d.get_text().split("\n")[13],'......:',Fore.GREEN+d.get_text().split("\n")[14].strip())
        print(Fore.CYAN+d.get_text().split("\n")[17],'.........:',Fore.GREEN+d.get_text().split("\n")[18].strip())
        print(Fore.CYAN+d.get_text().split("\n")[21],'...........:',Fore.GREEN+d.get_text().split("\n")[22].strip())
        print(Fore.CYAN+d.get_text().split("\n")[25],'..........:',Fore.GREEN+d.get_text().split("\n")[26].strip())
        print(Fore.CYAN+d.get_text().split("\n")[29],'...........:',Fore.GREEN+d.get_text().split("\n")[30].strip())
        print(Fore.CYAN+d.get_text().split("\n")[33],'.....:',Fore.GREEN+d.get_text().split("\n")[34].strip())
        print(Fore.CYAN+d.get_text().split("\n")[37],'..:',Fore.GREEN+d.get_text().split("\n")[38].strip())
        print(Fore.CYAN+d.get_text().split("\n")[41],'...........:',Fore.GREEN+d.get_text().split("\n")[42].strip())
        print(Fore.CYAN+d.get_text().split("\n")[45],'...........:',Fore.GREEN+d.get_text().split("\n")[46].strip())
        print(Fore.CYAN+d.get_text().split("\n")[49],'.........:',Fore.GREEN+d.get_text().split("\n")[50].strip())
        print(Fore.CYAN+d.get_text().split("\n")[53],'.....:',Fore.GREEN+d.get_text().split("\n")[54].strip())
        print(Fore.CYAN+d.get_text().split("\n")[57],'.......:',Fore.GREEN+d.get_text().split("\n")[58].strip())
        print(Fore.CYAN+d.get_text().split("\n")[61],'.........:',Fore.GREEN+d.get_text().split("\n")[62].strip())
        print(Fore.CYAN+d.get_text().split("\n")[65],'.....:',Fore.GREEN+d.get_text().split("\n")[66].strip())
        print(Fore.CYAN+d.get_text().split("\n")[69],'....:',Fore.GREEN+d.get_text().split("\n")[70].strip())
        return
        
