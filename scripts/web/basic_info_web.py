import requests
from scapy.all import *
import json
import webeye
from colorama import Fore
from Wappalyzer import Wappalyzer, WebPage


class BasicInfoWeb:

    def __init__(self) -> None:
        self.target     = str(input(f"\n{Fore.LIGHTBLACK_EX}Target [{Fore.WHITE}example.com{Fore.LIGHTBLACK_EX}] > {Fore.WHITE}"))
        self.is_https   = str(input(f"\n{Fore.LIGHTBLACK_EX}Does it have {Fore.LIGHTCYAN_EX}HTTPS{Fore.LIGHTBLACK_EX}? [{Fore.WHITE}y/n{Fore.LIGHTBLACK_EX}] > {Fore.WHITE}"))


        self.__conf()
        
        if self.target.split(".")[0] == "www":
            print(f'\n\t{Fore.RED}Invalid target:{Fore.LIGHTBLACK_EX} re-write target name and remove \"www.\"')
            print(f'\n\t{Fore.GREEN}Usage:{Fore.LIGHTBLACK_EX} example.com\n')
            exit(1)
        elif self.target.split("//")[0] == "https:" or self.target.split("//")[0] == "http:":
            print(f'\n\t{Fore.RED}Invalid target:{Fore.LIGHTBLACK_EX} re-write target name and remove \"{self.target.split("//")[0]}//\"')
            print(f'\n\t{Fore.GREEN}Usage:{Fore.LIGHTBLACK_EX} example.com\n')
            exit(1)
        else:
            if self.is_https == "y" or self.is_https == "Y":
                self.target = f"https://{self.target}"
                self.__draw_data()
            elif self.is_https == "n" or self.is_https == "N":
                self.target = f"http://{self.target}"    
                self.__draw_data()
            else:
                print(f"\n\t{Fore.RED}Wrong answer:{Fore.LIGHTBLACK_EX} {self.is_https}\n")
                exit(1)

    def __conf(self):
        conf.verb = 0
        
    def __get_server(self):
        res = requests.get(self.target)
        return res.status_code, res.request.url
    
    
    def __draw_data(self):
        

        try:
            status_code, url = self.__get_server()
            target_ip = webeye.geoip(host=self.target.split("//")[1])["query"]
            isp = webeye.geoip(host=self.target.split("//")[1])["isp"]
            org = webeye.geoip(host=self.target.split("//")[1])["org"]
            is_hosting_provider = webeye.geoip(host=self.target.split("//")[1])["hosting"]

            host_country = webeye.geoip(host=self.target.split("//")[1])["country"]
            host_region = webeye.geoip(host=self.target.split("//")[1])["regionName"]
            host_city = webeye.geoip(host=self.target.split("//")[1])["city"]
            host_continent = webeye.geoip(host=self.target.split("//")[1])["continent"]
            
            try:
                web_server = webeye.grab(host=self.target.split("//")[1])["Server"]
            except KeyError:
                web_server = "Not detected"
            
            subdomains = webeye.subenum(host=self.target.split("//")[1])

            if status_code in range(200,299):
                print(f"\n\t{Fore.LIGHTBLACK_EX}[{Fore.GREEN}{status_code}{Fore.LIGHTBLACK_EX}] {Fore.LIGHTBLACK_EX}{url}{Fore.WHITE} > {Fore.GREEN}{target_ip}{Fore.LIGHTBLACK_EX}\n")
                print(f"\n\t {Fore.BLUE}--- WEB SERVER INFORMATION --- {Fore.LIGHTBLACK_EX}\n")
                if web_server == "Not detected":
                    print(f"\t\t{Fore.LIGHTBLACK_EX}{'Web Server':30} {Fore.WHITE}>{Fore.RED}  {web_server}{Fore.LIGHTBLACK_EX}")                   
                else:
                    print(f"\t\t{Fore.LIGHTBLACK_EX}{'Web Server':30} {Fore.WHITE}>{Fore.GREEN}  {web_server}")
                    
                print(f"\n\t\t{Fore.BLUE}--- SUBDOMAINS --- {Fore.LIGHTBLACK_EX}\n")
                for subdomain in subdomains: print(f"\t\t\t{Fore.GREEN}  {subdomain}{Fore.LIGHTBLACK_EX}")
            
                print(f"\n\t {Fore.BLUE}--- IP INFORMATION --- {Fore.LIGHTBLACK_EX}\n")
                print(f"\t\t{Fore.LIGHTBLACK_EX}{'Host':30} {Fore.WHITE}>{Fore.GREEN}  {org}")            
                print(f"\t\t{Fore.LIGHTBLACK_EX}{'Internet Service Provider':30} {Fore.WHITE}>{Fore.GREEN}  {isp}")
                print(f"\t\t{Fore.LIGHTBLACK_EX}{'Is a hosting service provider':30} {Fore.WHITE}>{Fore.GREEN}  {is_hosting_provider}")
                print(f"\n\n\t\t {Fore.BLUE}--- HOST LOCATION --- {Fore.LIGHTBLACK_EX}\n")
                print(f"\t\t\t{Fore.LIGHTBLACK_EX}{'Country':15} {Fore.WHITE}>{Fore.GREEN}  {host_country}")
                print(f"\t\t\t{Fore.LIGHTBLACK_EX}{'Region':15} {Fore.WHITE}>{Fore.GREEN}  {host_region}")
                print(f"\t\t\t{Fore.LIGHTBLACK_EX}{'City':15} {Fore.WHITE}>{Fore.GREEN}  {host_city}")
                print(f"\t\t\t{Fore.LIGHTBLACK_EX}{'Continent':15} {Fore.WHITE}>{Fore.GREEN}  {host_continent}")
                # print(f"\t\t\t{Fore.LIGHTBLACK_EX}{'Continent':15} {Fore.WHITE}>{Fore.GREEN}  {host_continent}")

                print()
        except requests.exceptions.ConnectionError:
            print(f"\n{Fore.LIGHTBLACK_EX}Target > {Fore.WHITE}{self.target}\n")
            print(f"\n\t{Fore.RED}Sorry bad connection{Fore.LIGHTBLACK_EX}\n")
            