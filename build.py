from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible import context
from sys import argv

from collections import namedtuple

import requests
import json
import yaml
import os

build_type = argv[1]
gns3_server = "192.168.59.130"
gns3_port = "3080"


class GNS3:
    def __init__(self, project_name):
        #self.config = yaml.load(self.config_file)
        self.url = "http://{0}:{1}/v2".format(gns3_server, gns3_port)
        self.project_name = project_name
        self.project_id = None

    def open_project(self, project_id=None):
        if project_id is None:
            project_id = self.project_id

        resp = requests.post("{0}/projects/{1}/open".format(self.url, project_id))
        if resp.status_code == 201:
            return 201
        else:
            print("project does not exist")
            print("code: {0}, reason: {1}".format(resp.status_code, resp.text))
            exit(0)

    def start_nodes(self, project_id):
        if project_id is None:
            project_id = self.project_id

        resp = requests.post("{0}/projects/{1}/nodes/start".format(self.url, project_id))
        if resp.status_code > 400 < 404:
            print("Cannot start the nodes within the project")
            print(resp.status_code)
            print(resp.text)
            exit(0)
        elif resp.status_code == 204:
            print("Nodes have been started")
            return 204

    def find_project_id(self, project_name=None):
        if project_name is None:
            project_name = self.project_name

        resp = requests.get("{0}/projects".format(self.url))
        if resp.status_code == 404:
            print("No project found. Please make sure the project is loaded into GNS3")
            exit(0)

        for i in json.loads(resp.text):
            if i["name"] == project_name:
                self.project_id = i['project_id']
                return i["project_id"]

        print("Project id not found, make sure the project is loaded into GNS3")
        exit(0)


print("Starting Build process")

print("Checking build type")


class BuildAnsible():
    def __init__(self, host_file, ):
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])()
        self.host_file = host_file
        self.inventory = Inventory(loader=self.loader,
                                   variable_manager=self.variable_manager,
                                   host_list=self.host_file)


if build_type.upper() == 'LAN':
    print("Running Lan network deployment")
    print("Opening GNS3 Lab and powering on nodes")

    g = GNS3("basenetwork1")
    id = g.find_project_id()
    print(g.open_project(id))
    print(g.start_nodes(id))

    print("Running ansible_files scripts")

    ansible = BuildAnsible()

    pass
elif build_type.upper() == 'CLOUD':
    print("Running Cloud network deployment")
    pass