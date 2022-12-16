from colorama import Fore


# It opens the "docs/show_scripts.txt" file, reads it, and then closes it
class ShowScripts:
    
    def __init__(self):
        self.__open()
        self.__read()
        self.__close()
    
    def __open(self):
        self.file = open("docs/show_scripts.txt", mode="r")
    
    def __read(self):
        print(Fore.LIGHTBLACK_EX + self.file.read())
    
    def __close(self):
       self.file.close()