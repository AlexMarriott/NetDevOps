import pprint
import sys
from collections import namedtuple

import requests
import json
import yaml
import os
import subprocess

build_type = sys.argv[1]
gns3_server = "192.168.137.129"
gns3_port = "3080"

def build_path(*argv):
    full_path = os.getcwd()
    given_path = ""
    for i in argv:
        print(i)
        given_path = os.path.join(given_path, i)
    return os.path.join(full_path, given_path)

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

class BuildAnsible():
    def __init__(self, host_file, ):
        self.host_file = host_file

    def run_script(self, script_name, parameters=None):
        ansible_path = build_path("ansible_files")
        #https://stackoverflow.com/questions/57763068/how-to-run-ansible-playbooks-with-subprocess
        if parameters is not None:
            new_parameters = "{0}{1}.yaml --extra-vars {0}".format(ansible_path, script_name, parameters)
        else:
            new_parameters = "{0}{1}.yaml".format(ansible_path, script_name)

        print("Running ansible script")
        print(new_parameters)
        try:
            os.system("ansible-playbook -i {0}{1} {2} -vvvv".format(ansible_path, self.host_file, new_parameters))
        except Exception as e:
            print(e)


print("Starting Build process")

print("Checking build type")

if build_type.upper() == 'LAN':
    print("Running Lan network deployment")
    print("Opening GNS3 Lab and powering on nodes")

    g = GNS3("basenetwork1")
    id = g.find_project_id()
    print(g.open_project(id))
    print(g.start_nodes(id))

    ansible = BuildAnsible("hosts")

    print("Running the deployment scripts")

    ansible.run_script("mini-lan-ssh")

    print("Running base test case")
    base_test = '{"hosts": "deployerserver", "script": "{0} --ips 192.168.12.1 192.168.12.2 192.168.12.3"}'.format(build_path("testcases", "connectivity_check.py"))

    ansible.run_script("base-test", parameters=base_test)

    #This part will be running pyATS to test the topology of the new network.
    print("Running the python network tests")
    pass
elif build_type.upper() == 'CLOUD':
    print("Running Cloud network deployment")
    pass