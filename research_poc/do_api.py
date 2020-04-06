import requests
import json
import time
import os
"""

"""
class DoApi:
    # TODO need to add this as an enviroment value during the bulid process.
    def __init__(self):
        self.access_token = os.environ['DO_access_token']
        self.session = requests.Session()
        self.session.headers = {"Authorization": "Bearer {0}".format(self.access_token)}
        self.url = "https://api.digitalocean.com/v2/"

    def poll_node(self, nodes, sleep=0):
        if sleep > 0:
            time.sleep(sleep)
        elif sleep > 30:
            # Waiting too long for droplets to be deployed, something has gone wrong.
            return False
        resp = self.session.get("{0}/actions/".format(self.url))

        actions = json.loads(resp.text)["actions"]
        node_actions = list(filter(lambda x: x["resource_id"] in nodes, actions))
        for i in node_actions:
            if i["completed_at"] is not None and i['type'] in ['create', 'delete']:
                nodes.remove(i['resource_id'])
        if not nodes:
            return True
        else:
            self.poll_node(nodes, sleep + 1)

    def create_droplet(self, name=None):
        if name is None:
            name = "R1.ain.test"
        data = {
            "names": name,
            "region": "lon1",
            "size": "s-1vcpu-1gb",
            "image": "ubuntu-18-04-x64",
            "ssh_keys[]": ["57:c0:a6:98:c8:d1:03:49:7b:2c:af:f0:23:ab:cb:5e"],
            "backups": "False",
            "ipv6": "False",
            "private_networking": "True",
        }
        resp = self.session.post("{0}/droplets/".format(self.url), data=data)
        if resp.status_code == 202:
            pass

    def create_droplets(self, names=None):
        if names is None:
            names = ["R1.ain.test", "R2.ain.test", "SW1.ain.test"]
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
        resp = self.session.post("{0}/droplets/".format(self.url), data=data)
        if resp.status_code == 202:
            nodes = []
            for node in json.loads(resp.text)['droplets']:
                nodes.append(node['id'])
            self.poll_node(nodes)
        return {"status_code": resp.status_code, "respone": resp.text}

    def list_droplets(self):
        droplets = []
        resp = self.session.get("{0}/droplets/".format(self.url))
        json_resp = json.loads(resp.text)

        for i in json_resp['droplets']:
            droplets.append(i)
        return droplets

    def delete_droplet(self, droplet):
        resp = self.session.delete("{0}/droplets/".format(self.url) + str(droplet))
        if resp.status_code == 204:
            if not self.poll_node([droplet]):
                return {"status_code": 400, "respone": resp.text}
        return {"status_code": resp.status_code}

    def droplet_ip(droplet):
        pass

    def get_droplet(self, droplet_name):
        nodes = self.list_droplets()
        for i in nodes:
            if i['name'] == droplet_name:
                return json.loads(self.session.get("{0}/droplets/{1}".format(self.url, i['id'])).text)

    def get_last_action(self, droplet_id):
        resp = self.session.get("{0}/droplets/{1}".format(self.url, droplet_id))
        pass
