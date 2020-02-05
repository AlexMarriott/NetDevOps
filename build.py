"""This is the main build python file for the network deplyoment."""

import os
import requests
import json

access_token = ""
url = "https://api.digitalocean.com/v2/"
headers = {"Authorization": "Bearer {0}".format(access_token)}

session = requests.Session()
session.headers = headers


def create_droplet():
    data = {
        "names[]": [
            "R1.ain.test",
            "R2.ain.test",
            "SW1.ain.test"
        ],
        "region": "lon1",
        "size": "s-1vcpu-1gb",
        "image": "ubuntu-18-04-x64",
        "ssh_keys[]": ["57:c0:a6:98:c8:d1:03:49:7b:2c:af:f0:23:ab:cb:5e"],
        "backups": "False",
        "ipv6": "True",
        "private_networking": "True",
    }
    print(data)
    resp = session.post("{0}".format(url) + "droplets", data=data)
    print(resp.json())
    print(resp.status_code)


def list_droplets():
    droplets = []
    resp = session.get("{0}".format(url) + "droplets", headers=headers)
    json_resp = json.loads(resp.text)
    for i in json_resp['droplets']:
        print(i)
        droplets.append(i)
    return droplets


def delete_droplet(droplet):
    resp = session.delete("{0}/droplets/".format(url) + str(droplet))
    return "{0}".format(resp.status_code)


create_droplet()

droplets = list_droplets()
for i in droplets:
    print(delete_droplet(i['id']))
