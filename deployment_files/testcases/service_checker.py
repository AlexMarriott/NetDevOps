#!/usr/bin/env python3

from ftplib import FTP

import argparse
import requests

"""
This file check two services, HTTP and FTP and is used during the testing stage of the network CI/CD pipeline.
"""

def webserver_check(ip):
    """
    The webserver_check checks to see if a webserver on the given ip address is running via checking the status code and respone-reson
    :param ip: the ip address to check the web service of.
    :return: True if the service is running or False if the service isn't running or cannot be reached
    """
    resp = requests.get("http://{0}".format(ip))
    if 200 >= resp.status_code <= 204 and resp.reason == "OK":
        print("Can connect to {0} via HTTP".format(ip))
        return True
    else:
        print("Cannot connect to {0}".format(ip))
        print("returned status is {0}".format(resp.status_code))
        return False

def ftp_check(ip):
    """
    The ftp_service checks to see if a FTP server on the given ip address is running via checking the status code and respone-reson
    :param ip: the ip address to check the FTP service of.
    :return: True if the service is running or False if the service isn't running or cannot be reached
    """
    ftp = FTP(ip)
    check = ftp.login(user="", passwd="")

    if str(check).split(" ")[0] == str(230):
        print("Can connect to the FTP server {0}".format(ip))
        return True
    else:
        print("Cannot connect to FTP server {0}".format(ip))
        return False

if __name__ == "__main__":
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
                for services in parameters.__dict__['services']:
                    service_block = services.split(",")
                    for x in service_block:
                        if x.upper() == "FTP":
                            if ftp_check(i) is False:
                               print("{0} ftp server cannot be connected to".format(i))
                               exit(1)
                        elif x.upper() == "HTTP":
                            if webserver_check(i) is False:
                               print("{0} ftp server cannot be connected to".format(i))
                               exit(1)
                        else:
                            print("No services were passed in or we dont support we was given: {0}".format(parameters.__dict__['services']))
    else:
        print("No Ip addresses were passed into the script.")
