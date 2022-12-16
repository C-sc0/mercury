import re


class ParseTarget:
    
    def __init__(self, data):
        
        self.data = data
        
    
    def identify(self) -> dict:
        
        def ip_validation(ip):
            is_ip_regexp        = r'\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b'
            is_ip               = re.match(is_ip_regexp, ip)
            return is_ip
        
        is_ip = ip_validation(self.data)
        
        has_prefix_regexp   = r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/(3[0-2]|[1-2][0-9]|[0-9]))$'
        has_prefix          = re.match(has_prefix_regexp, self.data)
        
        is_range            = self.data.split("-")

        def is_int(string):
            """
            It tries to convert the string to an integer, and if it can't, it returns False
            
            :param string: The string to be converted to an integer
            :return: The function is_int() is returning the integer value of the string if it is an
            integer, and False if it is not.
            """
            try:
                str_converted = int(string)
                return str_converted
            except ValueError:
                return False

        if is_ip:
            
            return {
                "type"      : "IS_IP",
                "result"    : is_ip[0],
            }
            
        elif has_prefix:
            
            result  = has_prefix[0].split("/")
            ip      = result[0]
            prefix  = result[1]
            
            # It's checking if the IP is valid.
            if ip_validation(ip):

                if prefix == "24":
                
                    start_in = int(ip.split(".")[-1])
                    prefix = int(prefix)

                    return {
                        "type"      : "HAS_PREFIX",
                        "result"    : {
                            "ip"        : ip,
                            "prefix"    : prefix,
                            "start_in"  : start_in,
                            "end_in"    : 255,
                            "network"   : f"{ip.split('.')[0]}.{ip.split('.')[1]}.{ip.split('.')[2]}"
                        }
                    }
            else:
                return {
                    "error"  : f"Invalid target: {is_range[0]}-{is_range[1]}"
                }

        # Checking if the input is a range of IPs.
        elif len(is_range) == 2 and is_int(is_range[1]):
            
            # It's checking if the first part of the range is a valid IP.
            if ip_validation(is_range[0]):
            
                start_in    = int(is_range[0].split(".")[-1])
                end_in      = int(is_range[1])
                ip          = is_range[0]
                
                # It's checking if the start of the range is minor than the end of the range.
                if start_in < end_in:
                    return {
                        "type"  : "IS_RANGE",
                        "result"      : {
                        "ip"        : ip,
                            "start_in"  : start_in,
                            "end_in"    : end_in,
                            "network"   : f"{ip.split('.')[0]}.{ip.split('.')[1]}.{ip.split('.')[2]}"
                        }
                    }

                else:
                    return {
                        "type"      : "ERROR",
                        "message"   : "Start port should not be major than end port",
                        "start_in"  : start_in,
                        "end_in"    : end_in
                    }

            else:
                return {
                    "error"  : f"Invalid target: {is_range[0]}-{is_range[1]}"
                }

        else:
            if self.data.strip() == "":
                return {
                    "error"  : f"Invalid target: EMPTY_FIELD"
                }
            else:
                return {
                    "error"  : f"Unknowed target: {self.data}"
                }
