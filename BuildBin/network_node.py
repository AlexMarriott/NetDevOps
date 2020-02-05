import requests
import json


class NetworkNode:
    # TODO need to add this as an enviroment value during the bulid process.
    def __init__(self):
        self.access_token = ""
        self.session = requests.Session()
        self.session.headers = {"Authorization": "Bearer {0}".format(access_token)}
        self.url = "https://api.digitalocean.com/v2/"

    @classmethod
    def create_droplet(cls, names=["R1.ain.test", "R2.ain.test", "SW1.ain.test"]):
        data = {
            "names[]": names,
            "region": "lon1",
            "size": "s-1vcpu-1gb",
            "image": "ubuntu-18-04-x64",
            "ssh_keys[]": ["57:c0:a6:98:c8:d1:03:49:7b:2c:af:f0:23:ab:cb:5e"],
            "backups": "False",
            "ipv6": "False",
            "private_networking": "True",
        }
        resp = self.session.post("{0}".format(url) + "droplets", data=data)
        return {"status_code": resp.status_code, "respone": resp.text}

    @classmethod
    def list_droplets():
        droplets = []
        resp = self.session.get("{0}".format(url) + "droplets")
        json_resp = json.loads(resp.text)

        for i in json_resp['droplets']:
            droplets.append(i)
        return droplets

    def delete_droplet(droplet):
        resp = sefl.session.delete("{0}/droplets/".format(url) + str(droplet))
        return {"status_code": resp.status_code}

    def droplet_ip(droplet):
        pass

    def get_droplet(droplet_name):
        pass
