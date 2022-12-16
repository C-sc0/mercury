#!/bin/python
from init.args import Arguments
from os import system
    

class Mercury:
    
    def __init__():
        Arguments()


if __name__ == "__main__":
    while True:
        Arguments()
        restart = str(input("Continue? "))
        if restart == "y":
            system("python ./main.py -e")
        else:
            break