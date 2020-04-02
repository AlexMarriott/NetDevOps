import argparse
import socket

def webserver_check(i):
    pass

def ftp_check(i):
    pass

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    parser = argparse.ArgumentParser(description="List of ip addresses")
    parser.add_argument("--ips", nargs="*",
                        help="Ip addresses which will be tested for connectivity")
    parser.add_argument("--services", nargs="*",
                        help="service which need to tested for connectivity, Example: FTP, HTTP")
    parameters = parser.parse_args() if not None else None
    if parameters.__dict__['ips'] is not None:
        for ip in parameters.__dict__['ips']:
            # this is trash but idc
            ip_block = ip.split(",")
            for i in ip_block:
                print(i)
                for services in parameters.__dict__['services']:
                    print(services)
                    if services.upper() == "FTP":
                        ftp_check(i)
                    elif services.upper() == "HTTP":
                        webserver_check(i)
                    else:
                        print("No services were passed in or we don't support we was given: {0}".format(parameters.__dict__['services']))
    else:
        print("No Ip addresses were passed into the script.")