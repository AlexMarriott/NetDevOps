import os
import sys
import paramiko
import time

from BuildBin.build_ansible import BuildAnsible
from BuildBin.gns3 import GNS3
from BuildBin.remote_connection import RemoteSSH
from BuildBin.azure.models import AzureNode
from BuildBin.azure.azure_api import AzureApi
from BuildBin.common import build_path

build_type = sys.argv[1]
gns3_server = "192.168.137.129"
gns3_port = "3080"
amarriott_password = "iKcc-KfeZR.!EEAZUZQi#Bed"

print("Starting Build process")

print("Checking build type")

if build_type.upper() == 'LAN':
    print("Running Lan network deployment")
    print("Opening GNS3 Lab and powering on nodes")

    g = GNS3(gns3_server, gns3_port, "basenetwork1")
    id = g.find_project_id()
    print(g.open_project(id))
    print(g.start_nodes(id))
    ansible = BuildAnsible(build_path("deployment_files", "ansible", "hosts"))

    print("Running the deployment scripts")

    deploy = ansible.run_script("mini-lan-ssh", script_path=build_path("deployment_files", "ansible", "ansible_lan"))
    if not deploy:
        print("Something went wrong")
        exit(1)

    print("Running base test case")
    base_test = "'script={0} ips=192.168.12.1,192.168.12.2,192.168.12.3'".format(build_path("deployment_files","testcases", "connectivity_check.py"))

    base = ansible.run_script("deploy_file", script_path=build_path("deployment_files", "ansible", "ansible_lan"), parameters=base_test)
    if not base:
        #Should put a exit handle function here.
        print("Something went wrong")
        exit(1)

    print("Test ran, job completed. Have a nice day :-)")


elif build_type.upper() == 'CLOUD':


    print("Uploading commonly used files to azure storage")
    azure_api = AzureApi()
    upload_files = [{"file_name": "install_ansible.sh", "file_path": build_path("deployment_files", "bash")},
                    {"file_name": "deploy_services.yaml", "file_path": build_path("deployment_files", "ansible", "ansible_cloud")},
                    {"file_name": "ansible.cfg", "file_path": build_path("deployment_files", "ansible")},
                    {"file_name": "hosts", "file_path": build_path("deployment_files", "ansible")},
                    {"file_name": "service_checker.py", "file_path": build_path("deployment_files", "testcases")},
                    {"file_name": "connectivity_check.py", "file_path": build_path("deployment_files", "testcases")}]

    for file in upload_files:
        upload = azure_api.file_upload(file_name=file['file_name'], local_path=file['file_path'])

    print("Running Cloud network deployment")
    # This will be a deployment into azure where we test the network secutriy groups along with the nodes which can run routing rules.

    print("Creating azure nodes")
    # Naming convention should be Subnet-vm-num
    vms = [{"vm_name": "Office1-VM", "ip_assignment_type": "Static", "ip_address": "192.168.11.10"},
           # {"vm_name": "Office2-VM", "ip_assignment_type": "Static", "ip_address": "192.168.12.10"},
           {"vm_name": "Office3-VM", "ip_assignment_type": "Static", "ip_address": "192.168.13.10"}]
    azure_nodes = []

    for vm in vms:
        node = azure_api.create_node(vmname=vm["vm_name"], subnet=vm["vm_name"].split("-")[0],
                                     ip_assignment_type=vm["ip_assignment_type"], ip_address=vm["ip_address"])

        azure_nodes.append(AzureNode(name=node['vm'].name, resource_group=node['resource_group'],
                                     nic_name=node['nic_name'], nic_ip=node['nic_ip'],
                                     disk_name=node['disk_name']))

    print("Cloud nodes deployed, moving on the base deployment")
    ssh = RemoteSSH(hostname='51.140.73.210', username="amarriott", password=amarriott_password, port=22)
    ssh.connect()

    print("running deployment files.")

    deployment_files = [
        {"file_name": "ansible.cfg",
         "url": "https://deploymentscriptsdiss.blob.core.windows.net/deploymentscripts/ansible.cfg?sp=r&st=2020-04-01T11:40:11Z&se=2030-01-01T20:40:11Z&spr=https&sv=2019-02-02&sr=b&sig=eiVkp9mjnLT43INs3EOS%2BwPQW6awalHp4MkhNrIrndI%3D"},
        {"file_name": "deploy_services.yaml",
         "url": "https://deploymentscriptsdiss.blob.core.windows.net/deploymentscripts/deploy_services.yaml?sp=r&st=2020-04-01T11:44:32Z&se=2030-05-30T19:44:32Z&spr=https&sv=2019-02-02&sr=b&sig=KKerdVfVu9KIW8VMiBXgOHWnV1Q5Kb9w3iymEBEhB2A%3D"},
        {"file_name": "hosts",
         "url": "https://deploymentscriptsdiss.blob.core.windows.net/deploymentscripts/hosts?sp=r&st=2020-04-01T11:45:11Z&se=2029-09-01T19:45:11Z&spr=https&sv=2019-02-02&sr=b&sig=W5ycHv2doCRT0m7seCU1%2BBmfxvGIue2NIIMdKCWT9rg%3D"},
        {"file_name": "install_ansible.sh",
         "url": "https://deploymentscriptsdiss.blob.core.windows.net/deploymentscripts/install_ansible.sh?sp=r&st=2020-04-01T11:45:35Z&se=2030-08-01T19:45:35Z&spr=https&sv=2019-02-02&sr=b&sig=2RScQbf5W1LlGQOB%2B4lYbS0iFXPriZCpq1VZAdUOSi4%3D"},
        {"file_name": "connectivity_check.py",
         "url": "https://deploymentscriptsdiss.blob.core.windows.net/deploymentscripts/connectivity_check.py?sp=r&st=2020-04-01T12:09:06Z&se=2030-12-10T21:09:06Z&spr=https&sv=2019-02-02&sr=b&sig=AgebusiqoTMTTBNbdGpkFOOUP9IWuWFzlk771K2%2F1ew%3D"},
        {"file_name": "service_checker.py",
         "url": "https://deploymentscriptsdiss.blob.core.windows.net/deploymentscripts/service_checker.py?sp=r&st=2020-04-01T12:10:03Z&se=2027-02-18T21:10:03Z&spr=https&sv=2019-02-02&sr=b&sig=wblGukcwtdnJAHoBS8K5PQt9Gtc5%2BTLdN7eLc4YkLfs%3D"}]

    print("Creating deployment folder")
    ssh.exec_command("mkdir -p deployment")
    ssh.exec_command("rm deployment/*")

    print("Installing any dos2unix the deployment files ")
    print(ssh.exec_command("echo {0} | sudo apt install dos2unix -y"))

    print("Downloading the deployment files.")
    for file in deployment_files:
        print(ssh.exec_command("cd deployment && curl '{0}' > {1} && chmod 777 {1} && dos2unix {1}".format(file["url"],
                                                                                                           file[
                                                                                                               "file_name"])))

    print("Running node setup script")
    print(ssh.exec_command("(cd deployment; echo {0} | sudo ./install_ansible.sh)".format(amarriott_password)))

    print("Running ansible playbook")
    ansible_command = ssh.exec_command(
        "echo {0} | sudo chmod 777 sshkey.pub sshkey; echo {0} | sudo -s; cd deployment; ansible-playbook -i hosts deploy_services.yaml".format(
            amarriott_password))
    print(ansible_command)
    if ansible_command[0] is False:
        print("The ansible scripts could not run correctly, ending bulid")
        exit(1)

    print("Running connectivity testing and service testing")
    for file in ["connectivity_check.py --ips 192.168.13.10,192.168.11.10",
                 "service_checker.py --ips 192.168.11.10,192.168.13.10 --services FTP,HTTP"]:
        print(ssh.exec_command("cd deployment; echo {0} | sudo python3 {1}".format(amarriott_password, file)))

    ssh.client.close()

    print("deleting the azure nodes")
    for vm in azure_nodes:
        status = azure_api.delete_node(vm)
        print(status)
        if status == "succeeded":
            print("{0} deleted".format(vm['name']))
        else:
            print("Something went wrong when deleting the node.")
