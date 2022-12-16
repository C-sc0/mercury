from colorama import Fore
from scripts.networking.os_disc import OSDisc
from scripts.networking.host_disc import HostDisc
from scripts.web.basic_info_web import BasicInfoWeb
from scripts.web.services_in_web import ServicesInWeb
from scripts.os.extract_wpass import ExtractWLANPassword
# from scripts.osint.insta_disc import InstaDisc


# It takes a command as an argument and then executes the corresponding function
class ExecScript:

    def __init__(self, command, *args, **kwargs):

        self.command = command
        self.__exec_script()

    def __exec_script(self):
        if self.command == "0":
            HostDisc()
        elif self.command == "1":    
            OSDisc()
        elif  self.command == "2":
            BasicInfoWeb()
        elif self.command == "3":    
            ServicesInWeb()
        elif self.command == "4":    
            ExtractWLANPassword()
        else:
            print(Fore.RED + "\nWrong script!\n\n\t" + Fore.BLUE + "Print all scripts: " + Fore.LIGHTBLACK_EX + "\n\t\tpython main.py -S\n")