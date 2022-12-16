from colorama import Fore


# It opens the "docs/help.txt" file, reads it, and then closes it
class Help:
    
    def __init__(self):
        self.__open()
        self.__read()
        self.__close()
    
    def __open(self):
        self.file = open("docs/help.txt", mode="r")
    
    def __read(self):
        print(Fore.LIGHTBLACK_EX + self.file.read())
    
    def __close(self):
       self.file.close()