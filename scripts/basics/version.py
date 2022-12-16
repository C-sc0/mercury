from colorama import Fore


# It opens the "docs/version.txt" file, reads it, and closes it
class Version:
    
    def __init__(self):
        self.__open()
        self.__read()
        self.__close()
    
    def __open(self):
        self.file = open("docs/version.txt", mode="r")
    
    def __read(self):
        print(Fore.LIGHTBLACK_EX + self.file.read())
        
    def __close(self):
       self.file.close()