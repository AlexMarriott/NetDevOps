"""
This is the main build python file for the network deplyoment
"""

import os
import requests

access_token = ""
url = "https://api.digitalocean.com/v2/"
headers = {"Authorization": "Bearer {0}".format(access_token)}
print(headers)
data = {
  "name":[
    "R1.ain.test"
  ],
  "region": "lon1",
  "size": "s-1vcpu-1gb",
  "image": "ubuntu-18-04-x64",
  "backups": False,
  "ipv6": True,
  "private_networking": True,
}
resp = requests.post("{0}".format(url)  + "droplets", data=data, headers=headers)
print(resp.text)
print(resp.status_code)
