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





if __name__ == "__main__":
    url = "http://192.168.137.129:3080/v2/projects"
    project_name = "basenetwork1"
    os.
    r = requests
    print("Creating the project file")

    resp = r.post(url, json={"name": project_name})
    if resp.status_code == 409:
        print("project already exists, getting the project id")
        resp_project = r.get(url)
        for i in json.loads(resp_project.text):
            if i['name']:
                project_id = i['project_id']
        print(project_id)
    elif resp.status_code == 201:
        print("project created")
        for i in json.loads(resp.text):
            print(i)
            if i['name'] == project_name:
                id = i['project_id']
                break
        print(id)
    else:
        print("Something went worng")
        print(resp.status_code)
        print(resp.text)
        exit(0)

    print("Importing a the project file")

    resp1 = r.post("{0}/{1}/import".format(url,id))

    if resp1.status_code == 200:
        print("project imported correctly")
    else:
        print("Something went worng")
        print(resp1.status_code)
        print(resp1.text)
        exit(0)


