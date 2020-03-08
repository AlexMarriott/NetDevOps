from gns3.deplyoment_copy import create_project
import requests
import json
import yaml

class GNS3:

    def __init__(self):
        self.config_file = open("gns3/network.yaml")
        self.config = yaml.load(self.config_file)
        self.url = "http://{0}:{1}/v2/".format(self.config["gns3_server"], self.config["gns3_port"])

    def create_project(self, name):
        """
        Checking if a project with a given name already exists; if yes, deleting it.
        Then the function (re)creates the project and returns the project ID.
        """

        ### Finding the project ID if a project with the given name exists.
        url = str(self.url + "projects")
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            body = response.json()
            project = next((item for item in body if item["name"] == self.config["project_name"]), None)
        else:
            print("Received HTTP error {0} when checking if the project already exists! error: {1}".format(
                response.status_code, response.text))
            exit(1)

        ### Deleting the project if it already exists.
        if project != None:
            delete_project_id = project["project_id"]

            del_url = str(url + "/" + delete_project_id)
            print(del_url)
            response = requests.delete(del_url)
            if response.status_code != 204:
                print("Received HTTP error {0} when checking if the project already exists! error: {1}".format(
                    response.status_code, response.text))
                exit(1)

        ### (Re)creating the project
        data = {"name": name}
        data_json = json.dumps(data)
        response = requests.post(url, data=data_json)
        if response.status_code == 201:
            body = response.json()
            # Adding the project ID to the config
            self.config["project_id"] = body["project_id"]
        else:
            print("Received HTTP error {0} when creating the project. error: {1}".format(
                response.status_code, response.text))
            exit(1)

    def add_nodes(self):
        """
        This function adds a node to the project already created.
        """
## curl http://localhost:3080/v2/projects/b8c070f7-f34c-4b7b-ba6f-be3d26ed073f/nodes -d '{"symbol": ":/symbols/router.svg",
        # "name": "R1", "properties": {"platform": "c7200", "nvram": 512, "image": "c7200-adventerprisek9-mz.124-24.T8.image",
        # "ram": 512, "slot3": "PA-GE", "system_id": "FTX0945W0MY", "slot0": "C7200-IO-FE", "slot2": "PA-GE", "slot1": "PA-GE",
        # "idlepc": "0x606e0538", "startup_config_content": "hostname %h\n"}, "compute_id": "local", "node_type": "dynamips"}'
        ### Adding nodes

        node_url = str(self.url + "projects/{0}/nodes".format(self.config['project_id']))
        for instance in self.config["nodes"]:
                print(instance)
                data = {"symbol": ":/symbols/router.svg","compute_id":"local", "name": instance["name"],"node_type": "dynamips",
                        "properties":{"idlepc": instance["idlepc"] ,"image": instance["image"],
                                       "platform":instance["platform"],"ram":instance["ram"],"slot0":instance["slot0"],
                                      "slot1":instance["slot1"]},
                        "x": instance["x"], "y": instance["y"]}

                data_json = json.dumps(data)
                response = requests.post(node_url, data=data_json)
                if response.status_code == 201:
                    print("Added node: {0}".format(instance["dynamips_name"]))
                else:
                    print("Received HTTP error {0} when creating node: {1}. error: {2}".format(
                        response.status_code,instance["name"], response.text))
                    exit(1)

        ### Retrieving all nodes in the project, the assigning node IDs and console port numbers
        ### by searching the node's name, then appending the config with them.
        '''
        url = "http://%s:%s/v2/projects/%s/nodes" % \
              (CONFIG["gns3_server"], CONFIG["gns3_port"], CONFIG["project_id"])
        response = get(url)

        if response.status_code == 200:
            body = response.json()
            for appliance in CONFIG["nodes"]:
                for instance in appliance["instances"]:
                    instance["node_id"] = next((item["node_id"] \
                                                for item in body if item["name"] == instance["name"]), None)
                    instance["console"] = next((item["console"] \
                                                for item in body if item["name"] == instance["name"]), None)
        else:
            print("Received HTTP error %d when retrieving nodes! Exiting." % response.status_code)
            exit(1)
        '''

    def get_project_id(self, name):
        pass

    def get_nodes(self, project_id):
        url = self.url + "projects/{0}/nodes".format(project_id)
        print(url)
        r = requests.get(url)

        if r.status_code == 200:
            body = r.json()
            for i in body:
                print(i)


gns3 = GNS3()

gns3.create_project(gns3.config['project_name'])

gns3.add_nodes()

r = gns3.get_nodes("659a8010-15f7-4019-b19c-bd9d6801b4db")

if r.status_code == 200:
    body = r.json()

    for i in body:
        print(i)
else:
    print("respones code was {0}, encountered an error {1}".format(r.status_code, r.text))
