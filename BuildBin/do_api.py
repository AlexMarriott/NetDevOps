import requests
import json
import time

class DoApi:
    # TODO need to add this as an enviroment value during the bulid process.
    def __init__(self):
        self.access_token = ""
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
            if i["completed_at"] is not None and i['type'] == "create":
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
        #{'status_code': 202, 'respone': '{"droplets":[{"id":179457263,"name":"T1.ain.test","memory":1024,"vcpus":1,"disk":25,"locked":true,"status":"new","kernel":null,"created_at":"2020-02-08T17:47:51Z","features":[],"backup_ids":[],"next_backup_window":null,"snapshot_ids":[],"image":{"id":53893572,"name":"18.04.3 (LTS) x64","distribution":"Ubuntu","slug":"ubuntu-18-04-x64","public":true,"regions":["nyc1","sfo1","nyc2","ams2","sgp1","lon1","nyc3","ams3","fra1","tor1","sfo2","blr1"],"created_at":"2019-10-22T01:38:19Z","min_disk_size":20,"type":"snapshot","size_gigabytes":2.36,"description":"Ubuntu 18.04 x64 20191022","tags":[],"status":"available","error_message":""},"volume_ids":[],"size":{"slug":"s-1vcpu-1gb","memory":1024,"vcpus":1,"disk":25,"transfer":1.0,"price_monthly":5.0,"price_hourly":0.00744,"regions":["ams2","ams3","blr1","fra1","lon1","nyc1","nyc2","nyc3","sfo1","sfo2","sgp1","tor1"],"available":true},"size_slug":"s-1vcpu-1gb","networks":{"v4":[],"v6":[]},"region":{"name":"London 1","slug":"lon1","features":["private_networking","backups","ipv6","metadata","install_agent","storage","image_transfer"],"available":true,"sizes":["512mb","1gb","2gb","4gb","8gb","32gb","48gb","64gb","16gb","s-1vcpu-3gb","c-2","c-4","m-1vcpu-8gb","m-16gb","m-32gb","m-64gb","m-128gb","m-224gb","s-1vcpu-1gb","s-3vcpu-1gb","s-1vcpu-2gb","s-2vcpu-2gb","s-2vcpu-4gb","s-4vcpu-8gb","s-6vcpu-16gb","s-8vcpu-32gb","s-12vcpu-48gb","s-16vcpu-64gb","s-20vcpu-96gb","s-24vcpu-128gb","s-32vcpu-192gb","g-2vcpu-8gb","gd-2vcpu-8gb"]},"tags":[]},{"id":179457265,"name":"T2.ain.test","memory":1024,"vcpus":1,"disk":25,"locked":true,"status":"new","kernel":null,"created_at":"2020-02-08T17:47:51Z","features":[],"backup_ids":[],"next_backup_window":null,"snapshot_ids":[],"image":{"id":53893572,"name":"18.04.3 (LTS) x64","distribution":"Ubuntu","slug":"ubuntu-18-04-x64","public":true,"regions":["nyc1","sfo1","nyc2","ams2","sgp1","lon1","nyc3","ams3","fra1","tor1","sfo2","blr1"],"created_at":"2019-10-22T01:38:19Z","min_disk_size":20,"type":"snapshot","size_gigabytes":2.36,"description":"Ubuntu 18.04 x64 20191022","tags":[],"status":"available","error_message":""},"volume_ids":[],"size":{"slug":"s-1vcpu-1gb","memory":1024,"vcpus":1,"disk":25,"transfer":1.0,"price_monthly":5.0,"price_hourly":0.00744,"regions":["ams2","ams3","blr1","fra1","lon1","nyc1","nyc2","nyc3","sfo1","sfo2","sgp1","tor1"],"available":true},"size_slug":"s-1vcpu-1gb","networks":{"v4":[],"v6":[]},"region":{"name":"London 1","slug":"lon1","features":["private_networking","backups","ipv6","metadata","install_agent","storage","image_transfer"],"available":true,"sizes":["512mb","1gb","2gb","4gb","8gb","32gb","48gb","64gb","16gb","s-1vcpu-3gb","c-2","c-4","m-1vcpu-8gb","m-16gb","m-32gb","m-64gb","m-128gb","m-224gb","s-1vcpu-1gb","s-3vcpu-1gb","s-1vcpu-2gb","s-2vcpu-2gb","s-2vcpu-4gb","s-4vcpu-8gb","s-6vcpu-16gb","s-8vcpu-32gb","s-12vcpu-48gb","s-16vcpu-64gb","s-20vcpu-96gb","s-24vcpu-128gb","s-32vcpu-192gb","g-2vcpu-8gb","gd-2vcpu-8gb"]},"tags":[]},{"id":179457266,"name":"T3.ain.test","memory":1024,"vcpus":1,"disk":25,"locked":true,"status":"new","kernel":null,"created_at":"2020-02-08T17:47:51Z","features":[],"backup_ids":[],"next_backup_window":null,"snapshot_ids":[],"image":{"id":53893572,"name":"18.04.3 (LTS) x64","distribution":"Ubuntu","slug":"ubuntu-18-04-x64","public":true,"regions":["nyc1","sfo1","nyc2","ams2","sgp1","lon1","nyc3","ams3","fra1","tor1","sfo2","blr1"],"created_at":"2019-10-22T01:38:19Z","min_disk_size":20,"type":"snapshot","size_gigabytes":2.36,"description":"Ubuntu 18.04 x64 20191022","tags":[],"status":"available","error_message":""},"volume_ids":[],"size":{"slug":"s-1vcpu-1gb","memory":1024,"vcpus":1,"disk":25,"transfer":1.0,"price_monthly":5.0,"price_hourly":0.00744,"regions":["ams2","ams3","blr1","fra1","lon1","nyc1","nyc2","nyc3","sfo1","sfo2","sgp1","tor1"],"available":true},"size_slug":"s-1vcpu-1gb","networks":{"v4":[],"v6":[]},"region":{"name":"London 1","slug":"lon1","features":["private_networking","backups","ipv6","metadata","install_agent","storage","image_transfer"],"available":true,"sizes":["512mb","1gb","2gb","4gb","8gb","32gb","48gb","64gb","16gb","s-1vcpu-3gb","c-2","c-4","m-1vcpu-8gb","m-16gb","m-32gb","m-64gb","m-128gb","m-224gb","s-1vcpu-1gb","s-3vcpu-1gb","s-1vcpu-2gb","s-2vcpu-2gb","s-2vcpu-4gb","s-4vcpu-8gb","s-6vcpu-16gb","s-8vcpu-32gb","s-12vcpu-48gb","s-16vcpu-64gb","s-20vcpu-96gb","s-24vcpu-128gb","s-32vcpu-192gb","g-2vcpu-8gb","gd-2vcpu-8gb"]},"tags":[]}],"links":{"actions":[{"id":867527778,"rel":"batch","href":"https://api.digitalocean.com/v2/actions/867527778"}]}}'}

        return {"status_code": resp.status_code, "respone": resp.text}

    def list_droplets(self):
        droplets = []
        resp = self.session.get("{0}/droplets/".format(self.url))
        json_resp = json.loads(resp.text)

        for i in json_resp['droplets']:
            droplets.append(i)
        return droplets

    def delete_droplet(self,droplet):
        resp = self.session.delete("{0}/droplets/".format(self.url) + str(droplet))
        return {"status_code": resp.status_code}

    def droplet_ip(droplet):
        pass

    def get_droplet(self, droplet_name):
        nodes = self.list_droplets()
        for i in nodes:
            if i['name'] == droplet_name:
                return json.loads(self.session.get("{0}/droplets/{1}".format(self.url, i['id']).text))

    def get_last_action(self,droplet_id):
        resp = self.session.get("{0}/droplets/{1}".format(self.url, droplet_id))
