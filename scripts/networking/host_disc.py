from sys import exit
from scapy.all import ARP, sr, conf
from colorama import Fore
import msvcrt
import socket

from ..parse_target import ParseTarget


"""
It's a class that sends an ARP packet to a given IP address and returns the MAC address of the host
if it's online.
"""
class HostDisc:
    
    def __init__(self):
        self.__conf()
        self.__send_packet()


    """
    It disables the verbose mode.
    """
    def __conf(self):
        conf.verb = 0


    """
    It's sending an ARP packet to a given IP address and returning the MAC address of the host if
    it's online
    """
    def __send_packet(self):

        try:
            self.dst_ip = str(input(Fore.LIGHTBLACK_EX + "\nTarget (" + Fore.WHITE + "Ex: 10.0.0.0" + Fore.LIGHTBLACK_EX + "): "))
            self.target = ParseTarget(data=self.dst_ip).identify()

            self.timeout = str(input(Fore.LIGHTBLACK_EX + "\nTimeout (" + Fore.WHITE + "[1-9]s" + Fore.LIGHTBLACK_EX + "): "))                
            self.timeout = self.__timeout_to_int(self.timeout)

            
            # It's checking if the destination IP address is 127.0.0.1. If the destination IP address
            # is 127.0.0.1, then it will get the own IP address and it will send an ARP packet to the
            # own IP address.
            if self.dst_ip == "127.0.0.1":
                own_ip = socket.gethostbyname_ex(socket.gethostname())[2][-1]
                self.results, self.unanswered = sr(ARP(pdst=own_ip), timeout = self.timeout)
                self.__answer_validation("127.0.0.1")
                
            else:
                
                # It's sending an ARP packet to a given IP address and returning the MAC address of
                # the host if it's online.
                if self.target["type"] == "IS_IP":
                    
                    self.results, self.unanswered = sr(ARP(pdst=self.target["result"]), timeout = self.timeout)
                    self.__answer_validation(self.dst_ip)

                # It's sending an ARP packet to every host in the network.
                elif self.target["type"] == "HAS_PREFIX":
                    host_num = self.target["result"]["start_in"]
                        
                    while host_num < self.target["result"]["end_in"]:
                            
                        # It's checking if the user pressed the "q" key. If the user pressed the "q" key,
                        # then it will break the loop. 
                        if msvcrt.kbhit() and msvcrt.getwch()=='q':
                            print(f"\n\n\t{Fore.LIGHTBLACK_EX}[{Fore.GREEN}+{Fore.LIGHTBLACK_EX}] Exiting!\n")
                            break
                            
                        # It's checking if the host number is 255. If the host number is 255, then it
                        # will break the loop.
                        if host_num == 255:
                            break
                            
                        dst_ip = f"{self.target['result']['network']}.{host_num}"
                        self.results, self.unanswered = sr(ARP(pdst=dst_ip), timeout = self.timeout)
                        self.__answer_validation(dst_ip)
                        host_num += 1
                        
                        print(f"\t{Fore.LIGHTBLACK_EX}Press {Fore.WHITE}q{Fore.LIGHTBLACK_EX} to stop and exit")
                        
                        
                # It's checking if the IP address is a range.
                elif self.target["type"] == "IS_RANGE":
                            
                    host_num = self.target["result"]["start_in"]
                            
                    # Send an ARP packet to every target
                    while host_num <= self.target["result"]["end_in"]:
                                
                        # then it will break the loop.
                        # It's checking if the user pressed the "q" key. If the user pressed the "q" key,
                        if msvcrt.kbhit() and msvcrt.getwch()=='q':
                            print(f"\n\n\t{Fore.LIGHTBLACK_EX}[{Fore.GREEN}+{Fore.LIGHTBLACK_EX}] Exiting!\n")
                            break
                                
                        # It's checking if the host number is 255. If the host number is 255, then it
                        # will break the loop.
                        if host_num == 255:
                            break
                                
                        dst_ip = f"{self.target['result']['network']}.{host_num}"    
                        self.results, self.unanswered = sr(ARP(pdst=dst_ip), timeout = self.timeout)
                        self.__answer_validation(dst_ip)
                        host_num += 1
                        print(f"\t{Fore.LIGHTBLACK_EX}Press {Fore.WHITE}q{Fore.LIGHTBLACK_EX} to stop and exit")
                                    
                else:
                    print(f"\n\t{Fore.LIGHTBLACK_EX}[{Fore.RED}!{Fore.LIGHTBLACK_EX}] {Fore.RED}Invalid target!\t{self.dst_ip}\n")
                    exit(1)
                    
        except KeyError:
            print(f"\n\t{Fore.LIGHTBLACK_EX}[{Fore.RED}!{Fore.LIGHTBLACK_EX}] {Fore.RED}{self.target['error']}\n")
            exit(1)    
        
        except OSError:
            print(f"\n\t{Fore.LIGHTBLACK_EX}[{Fore.RED}x{Fore.LIGHTBLACK_EX}] {Fore.RED}Must be executed as \"Admin-Only Mode\"{Fore.LIGHTBLACK_EX}\n")
            exit(1)

        except KeyboardInterrupt:
            print(f"\n\n\t{Fore.LIGHTBLACK_EX}[{Fore.GREEN}+{Fore.LIGHTBLACK_EX}] Exiting!\n")
            exit(0)

    """
    It's checking if the destination IP address is not responding to the ARP request. If the
    destination IP address is not responding to the ARP request, then print a message saying
    that the destination IP address is down. Otherwise, print a message saying that the
    destination IP address is up.
    """
    def __answer_validation(self, dst_ip):
        
        if self.unanswered:
            print(f"\n\t{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}!{Fore.LIGHTBLACK_EX}] {dst_ip}: {Fore.RED}DOWN!{Fore.LIGHTBLACK_EX}\n")
        else:
            result = self.results[0]
            dst_mac = str(result)[str(result).find("hwsrc"):str(result).find("hwsrc")+23].strip().split("=")[1]
            print(f"\n\t{Fore.LIGHTBLACK_EX}[{Fore.GREEN}+{Fore.LIGHTBLACK_EX}] {dst_ip} [{Fore.WHITE}{dst_mac}{Fore.LIGHTBLACK_EX}]: {Fore.GREEN}ON!{Fore.LIGHTBLACK_EX}\n")


    """
    It converts a timeout value to an integer
    :param timeout: The timeout in seconds
    """
    def __timeout_to_int(self, timeout):
        timeout_default = 5

        # It's checking if the user didn't enter a timeout value. If the user didn't enter a timeout
        # value, then it will print a message saying that it will use the default timeout value.
        if timeout.strip() == "":
            print(f"\n{Fore.YELLOW}Default: using by default timeout value => 5{Fore.LIGHTBLACK_EX}")
            return timeout_default
        else:
            # It's checking if the user entered a timeout value that is not in the range of 1 to 9. If
            # the user entered a timeout value that is not in the range of 1 to 9, then it will print
            # a message saying that it will use the default timeout value. Otherwise, it will return
            # the timeout value.
            try:
                if not int(self.timeout) in range(1,9):
                    print(f"\n{Fore.YELLOW}Value out of range: using by default timeout value => 5{Fore.LIGHTBLACK_EX}")
                    return timeout_default
                else:
                    return int(self.timeout)
            except ValueError:
                print(f"\n{Fore.YELLOW}Invalid value: using by default timeout value => 5{Fore.LIGHTBLACK_EX}")
                return timeout_default