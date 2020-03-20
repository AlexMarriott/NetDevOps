import json

import requests


class GNS3:
    def __init__(self, gns3_server, gns3_port, project_name):
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