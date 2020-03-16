import json
import os
import requests



def create_project(project_name):
    pass

def list_projects():
    pass

def get_project(project_id):
    pass

def import_project(project_id, project_zip):
    pass

def power_on_all_node(project_id):
    pass

def jank():

    resp = r.post(url, json={"name": project_name})
    if resp.status_code == 409:
        print("project already exists, getting the project id")
        resp_project = r.get(url)
        for i in json.loads(resp_project.text):
            if i['name'] == project_name:
                project_id = i['project_id']

    elif resp.status_code == 201:
        print("project created")
        resp = json.loads(resp.text)
        project_id = resp['project_id']
    else:
        print("Something went wrong")
        print(resp.status_code)
        print(resp.text)
        exit(0)

    print("Importing a the project file")
    print("{0}/{1}/import".format(url, project_id))

    resp1 = r.post("{0}/{1}/import".format(url, project_id), files=project_file)
    #breakpoint()
    if resp1.status_code == 200:
        print("project imported correctly")
    else:
        print("Something went wrong")
        print(resp1.status_code)
        print(resp1.text)
        print(resp1.reason)
        exit(0)

if __name__ == "__main__":
    url = "http://192.168.1.129:3080/v2/projects"
    project_name = "basenetwork1"
    project_file = {"file": open("projects/basenetwork1.gns3project", "rb")}
    r = requests
    print("Creating the project file")


