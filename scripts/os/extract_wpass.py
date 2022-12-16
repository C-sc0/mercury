import subprocess
from colorama import Fore


class ExtractWLANPassword:
    
    def __init__(self) -> None:

        meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode("utf-8", errors="backslashreplace")
        results = meta_data.split("\n")
        ssids = []

        for i in results:
            x = i.strip().split(" : ")
            
            if len(x) > 1:
                ssids.append(x[1])

        print(f"\n{Fore.LIGHTBLACK_EX}------------------------------------------------------------------------------------------------------------{Fore.WHITE}")
        print (f"{Fore.LIGHTBLACK_EX}| {'SSID':<30} | {'HAS PASSWORD':<14} | {'PASSWORD':<35} | {'AUTHENTICATION':<16} |")
        print(f"{Fore.LIGHTBLACK_EX}|--------------------------------+----------------+-------------------------------------+------------------|")

        for ssid in ssids:
            
            meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles', 'name=', ssid, 'key=clear']).decode("latin-1", errors="backslashreplace")
            keys = meta_data.split("\n")
            for key in keys:
                if len(key.strip().split(" : ")) > 1:

                    if key.strip().split(" : ")[0].strip() == "Autenticaci¢n" or key.strip().split(" : ")[0].strip() == "Authentication":
                        authentication = key.strip().split(" : ")[1]
                    
                    if key.strip().split(" : ")[0].strip() == "Cifrado" or key.strip().split(" : ")[0].strip() == "Cirpher":
                        if key.strip().split(" : ")[1] == "Ninguna" or key.strip().split(" : ")[1] == "None":
                            print(f"| {Fore.WHITE}{ssid:<30}{Fore.LIGHTBLACK_EX} | {Fore.LIGHTRED_EX}{'False':<14}{Fore.LIGHTBLACK_EX} | {Fore.WHITE}{'':<35}{Fore.LIGHTBLACK_EX} | {Fore.WHITE}{authentication:<16} {Fore.LIGHTBLACK_EX}|")

                        
                    password = key.strip().split(" : ")[1]
                    if key.strip().split(" : ")[0].strip() == "Key Content" or key.strip().split(" : ")[0].strip() == "Contenido de la clave":
                    # key.strip().split(" : ")[0]
                        print(f"{Fore.LIGHTBLACK_EX}|{Fore.WHITE} {ssid:<30} {Fore.LIGHTBLACK_EX}|{Fore.LIGHTGREEN_EX} {'True':<14} {Fore.LIGHTBLACK_EX}|{Fore.WHITE} {password:<35} {Fore.LIGHTBLACK_EX}|{Fore.WHITE} {authentication:<16} {Fore.LIGHTBLACK_EX}|")

        print(f"------------------------------------------------------------------------------------------------------------\n{Fore.WHITE}")
