import random
from colorama import Fore


# It opens the "docs/help.txt" file, reads it, and then closes it
class DisplayIcon:
    
    def __init__(self):
        self.__open()
        self.__read()
        self.__close()
    
    def __open(self):
        icon_file = random.randint(1,3)
        self.file = open(f"docs/icons/icon{icon_file}.txt", mode="r", encoding="utf-8")
    
    def __read(self):
        print(f"\n{Fore.RED}{self.file.read()}{Fore.WHITE}\n")
    
    def __close(self):
       self.file.close()

