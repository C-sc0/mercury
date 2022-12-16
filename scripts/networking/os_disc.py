from sys import exit
from re import findall
from scapy.all import IP, ICMP, conf, sr1
from colorama import Fore


# The above class is used to discover the OS of a given IP address.
class OSDisc:

    def __init__(self):
        self.dst_ip = str(input(Fore.LIGHTBLACK_EX + "\nTarget (" + Fore.WHITE + "Ex: 10.0.0.0" + Fore.LIGHTBLACK_EX + "): "))
        self.timeout = str(input(Fore.LIGHTBLACK_EX + "\nTimeout (" + Fore.WHITE + "[1-9]s" + Fore.LIGHTBLACK_EX + "): "))                
        self.timeout = self.__timeout_to_int(self.timeout)
        
        
        self.__conf()
        self.__os_disc()


    def __conf(self):
        # Disabling Verbose Mode
        conf.verb = 0


    """
    It takes a string and returns a list of all the IP addresses found in the string
    :return: A list of IP addresses.
    """
    def __ip_validation(self):

        ip_reg_exp = r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b'
        ip_validation = findall(ip_reg_exp, self.dst_ip)

        return ip_validation


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


    """
    It sends an ICMP packet to the target and then checks the TTL value of the response and deduce the Operating System
    """
    def __os_disc(self):
        
        if len(self.__ip_validation()) != 0:

            packet = IP(dst = self.dst_ip)/ICMP()
            
            ans = sr1(packet, timeout=self.timeout)
            
            if ans:
                if IP in ans:
                    ttl_number = ans.getlayer(IP).ttl
                    
                    if ttl_number <= 64:
                        print(f"\n\t{Fore.LIGHTBLACK_EX}[{Fore.GREEN}+{Fore.LIGHTBLACK_EX}] May be some {Fore.WHITE}Linux{Fore.LIGHTBLACK_EX} distribution: TTL {Fore.YELLOW}{ttl_number}{Fore.LIGHTBLACK_EX}\n")
                    elif ttl_number > 64:
                        print(f"\n\t{Fore.LIGHTBLACK_EX}[{Fore.GREEN}+{Fore.LIGHTBLACK_EX}] May be some {Fore.WHITE}Windows{Fore.LIGHTBLACK_EX} version: TTL {Fore.YELLOW}{ttl_number}{Fore.LIGHTBLACK_EX}\n")
                    else:
                        print(f"\n\t{Fore.LIGHTBLACK_EX}[{Fore.RED}!{Fore.LIGHTBLACK_EX}] Unknowed host: TTL {Fore.WHITE}{ttl_number}{Fore.LIGHTBLACK_EX}\n")
            else:
                print(f"\n\t{Fore.LIGHTBLACK_EX}[{Fore.RED}!{Fore.LIGHTBLACK_EX}] {Fore.RED}host {Fore.WHITE}{self.dst_ip} {Fore.RED}could be down: {Fore.LIGHTBLACK_EX}\n")

        else:
            print(f"\n\t{Fore.LIGHTBLACK_EX}[{Fore.RED}x{Fore.LIGHTBLACK_EX}] {Fore.RED}wrong target: {Fore.WHITE}{self.dst_ip}{Fore.LIGHTBLACK_EX}\n")