import json

import requests


class GNS3:
    """
    This Class is the uses to connect and interface with a GNS3 server.
    https://www.gns3.com/
    """
    def __init__(self, gns3_server, gns3_port, project_name):
        """
        The init function takes the necessary parameters to instantiate an instance of the GNS3 object
        :param gns3_server: String, the hostname for the gns3 server.
        :param gns3_port: int, the port number of the gns3 server
        :param project_name: String, the project saved on the gns3 server
        """
        self.url = "http://{0}:{1}/v2".format(gns3_server, gns3_port)
        self.project_name = project_name
        self.project_id = None

    def open_project(self, project_id=None):
        """
        The open_project functions opens a saved project on the remote gns3 server
        :param project_id: int, the project id related to the saved project on the server
        :return: 201 if the project was opened successfully or 404 if the server could not be reached
        """
        if project_id is None:
            project_id = self.project_id

        resp = requests.post("{0}/projects/{1}/open".format(self.url, project_id))
        if resp.status_code == 201:
            return 201
        else:
            print("project does not exist")
            print("code: {0}, reason: {1}".format(resp.status_code, resp.text))
            return 404

    def start_nodes(self, project_id):
        """
        The start_nodes functions starts the network nodes within the running project.
        :param project_id: int, the project id related to the saved project on the server
        :return: 204 if the nodes were started successfully or 404 if the server could not be reached
        """
        if project_id is None:
            project_id = self.project_id

        resp = requests.post("{0}/projects/{1}/nodes/start".format(self.url, project_id))
        if resp.status_code > 400 < 404:
            print("Cannot start the nodes within the project")
            print(resp.status_code)
            print(resp.text)
            return 404
        elif resp.status_code == 204:
            print("Nodes have been started")
            return 204

    def find_project_id(self, project_name=None):
        """
        The find_project_id functions returns the id of the passed in project name
        or returns the objects assigned default project.
        :param project_name: String, the project name
        :return: project id if the project was found or 404 if the server could not be reached or the project id could not be found.
        """
        if project_name is None:
            project_name = self.project_name

        resp = requests.get("{0}/projects".format(self.url))
        if resp.status_code == 404:
            print("No project found. Please make sure the project is loaded into GNS3")
            return 404

        for i in json.loads(resp.text):
            if i["name"] == project_name:
                self.project_id = i['project_id']
                return i["project_id"]

        print("Project id not found, make sure the project is loaded into GNS3")
        return 404