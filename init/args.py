import sys
import getopts
from colorama import Fore

from .exec_script import ExecScript
from scripts.basics.help import Help
from scripts.basics.version import Version
from scripts.basics.show_scripts import ShowScripts
from scripts.basics.display_icon import DisplayIcon



# The class is called Arguments and it's a class that parses the command line arguments
class Arguments:

    def __init__(self) -> None:


        # It's a dictionary that contains the command line arguments and their values.
        opts = {
            "h" : 0,        "help"          : 0,
            "v" : 0,        "version"       : 0,
            "S" : 0,        "show-scripts"  : 0,
            "e" : 0,        "execute"       : 0,
        }
                
        self.getopt = getopts.getopts(sys.argv, opts)
    
        #It's a for loop that iterates over the command line arguments.
        for option in self.getopt:
         
            
            if option in ("h", "help"):
                Help()
                sys.exit(0)
            
            elif option in ("v", "version"):
                Version()
                sys.exit(0)
            
            elif option in ("S", "show-scripts"):
                ShowScripts()
                sys.exit(0)
            
            elif option in ("e", "execute"):
                self.__display_panel()
                
                try:
                    command = str(input(f"{Fore.LIGHTBLACK_EX}Choose a tool: {Fore.WHITE}"))
                    ExecScript(command)
                except KeyboardInterrupt:
                    print(f"\n\n\t{Fore.LIGHTBLACK_EX}[{Fore.GREEN}+{Fore.LIGHTBLACK_EX}] Exiting!\n")
                    
                sys.exit(0)

    def __display_panel(self):
        
        DisplayIcon()
        
        file = open(f"docs/panels/scripts_panel.txt", mode="r", encoding="utf-8")
    
    
        for line in file.readlines():
            if line.strip()[0:1] == "[":
                print(f"{Fore.BLUE}{line[0:-3]}{Fore.LIGHTBLACK_EX}")
            else:
                print(f"{Fore.LIGHTBLACK_EX}{line[0:-3]}")
        file.close()