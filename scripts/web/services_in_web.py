import requests
from scapy.all import *
from colorama import Fore
from Wappalyzer import Wappalyzer, WebPage
import webeye


class ServicesInWeb:

    def __init__(self) -> None:
        self.target     = str(input(f"\n{Fore.LIGHTBLACK_EX}Target [{Fore.WHITE}example.com{Fore.LIGHTBLACK_EX}] > {Fore.WHITE}"))
        
        
        if self.target.split(".")[0] == "www":
            print(f'\n\t{Fore.RED}Invalid target:{Fore.LIGHTBLACK_EX} re-write target name and remove \"www.\"')
            print(f'\n\t{Fore.GREEN}Usage:{Fore.LIGHTBLACK_EX} example.com\n')
            exit(1)
        elif self.target.split("//")[0] == "https:" or self.target.split("//")[0] == "http:":
            print(f'\n\t{Fore.RED}Invalid target:{Fore.LIGHTBLACK_EX} re-write target name and remove \"{self.target.split("//")[0]}//\"')
            print(f'\n\t{Fore.GREEN}Usage:{Fore.LIGHTBLACK_EX} example.com\n')
            exit(1)
        else:
            self.is_https   = str(input(f"\n{Fore.LIGHTBLACK_EX}Does it have {Fore.LIGHTCYAN_EX}HTTPS{Fore.LIGHTBLACK_EX}? [{Fore.WHITE}y/n{Fore.LIGHTBLACK_EX}] > {Fore.WHITE}"))
            if self.is_https == "y" or self.is_https == "Y":
                self.target = f"https://{self.target}"
                self.__draw_data()
            elif self.is_https == "n" or self.is_https == "N":
                self.target = f"http://{self.target}"    
                self.__draw_data()
            else:
                print(f"\n\t{Fore.RED}Wrong answer:{Fore.LIGHTBLACK_EX} {self.is_https}\n")
                exit(1)

    
    def __get_running_services(self):

        webpage = WebPage.new_from_url(self.target)
        wappalyzer = Wappalyzer.latest().analyze_with_versions_and_categories(webpage)
        
        running_services = []
        
        for value in wappalyzer:
            
            running_services.append({
                "Software"  : value,
                "Version"   : wappalyzer[value]["versions"],
                "Category"  : wappalyzer[value]["categories"]
            })

        return running_services
    
    
    def __draw_data(self):
        
        running_services = self.__get_running_services()

        if running_services:
            
            res = requests.get(self.target)
            status_code, url = res.status_code, res.request.url
            target_ip = webeye.geoip(host=self.target.split("//")[1])["query"]
            print(f"\n\t{Fore.LIGHTBLACK_EX}[{Fore.GREEN}{status_code}{Fore.LIGHTBLACK_EX}] {Fore.LIGHTBLACK_EX}{url}{Fore.WHITE} > {Fore.GREEN}{target_ip}{Fore.LIGHTBLACK_EX}\n")
            
            print(f"\n{Fore.LIGHTBLACK_EX}[\t{Fore.GREEN}SERVICES RUNNING{Fore.LIGHTBLACK_EX}\t]", )

            for service in running_services:
                if len(service['Version']) > 0:
                    print(f"\n\t{Fore.WHITE}{service['Category'][0]}{Fore.LIGHTBLACK_EX} > {Fore.LIGHTBLUE_EX}{service['Software']} {service['Version'][0]}{Fore.LIGHTBLACK_EX}")
                else:
                    print(f"\n\t{Fore.WHITE}{service['Category'][0]}{Fore.LIGHTBLACK_EX} > {Fore.LIGHTBLUE_EX}{service['Software']}{Fore.LIGHTBLACK_EX}")
            print()
        else:
            print(f"\n\t{Fore.YELLOW}It couldn't detect any service here, Try with other website{Fore.WHITE}\n")
            exit(1)