# coding: utf-8

import sys
from colorama import Fore,Back,Style,init
init(autoreset = True)

def write(msg):
    print(msg)

error = lambda msg:write(Fore.RED+"[-] "+Style.RESET_ALL+msg)
info = lambda msg:write(Fore.GREEN+"[+] "+Style.RESET_ALL+msg)
warning = lambda msg:write(Fore.YELLOW+Style.BRIGHT+"[!] "+Style.RESET_ALL+msg)
wait = lambda msg:write(Fore.YELLOW+"[~] "+Style.RESET_ALL+msg)
okey = lambda msg:write(Fore.GREEN+Style.BRIGHT+"[+] "+Style.RESET_ALL+msg)
