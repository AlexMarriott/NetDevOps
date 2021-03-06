#!/usr/bin/env python3
import socket
import platform
import subprocess
import argparse

"""
This file pings network devices and is used during the testing stage of the network CI/CD pipeline.
"""
def ping_ip(ip):
    """
    The ping_ip script takes in a ip address and ping the ip.
    :param ip: Ip address of the device you want to ping
    """
    #TODO add messuring of the packets.
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ["ping", param, "5", ip]
    rep = subprocess.call(command)
    if rep == 0:
        print("node is up", ip)
    else:
        print("node cannot be pinged", ip)

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    parser = argparse.ArgumentParser(description="List of ip addresses")
    parser.add_argument("--ips", nargs="*",
                        help="Ip addresses which will be tested for connectivity")
    ips = parser.parse_args() if not None else None
    if ips.__dict__['ips'] is not None:
        for ip in ips.__dict__['ips']:
            # this is trash but idc
            ip_block = ip.split(",")
            for i in ip_block:
                print(i)
                ping_ip(i)
    else:
        print("No Ip addresses were passed into the script.")

