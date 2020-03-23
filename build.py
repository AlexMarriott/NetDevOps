import sys
import os

from BuildBin.buildansible import BuildAnsible
from BuildBin.gns3 import GNS3
from BuildBin.azure.models import AzureNode
from BuildBin.azure.azure_api import AzureApi
from BuildBin.common import build_path

build_type = sys.argv[1]
gns3_server = "192.168.137.129"
gns3_port = "3080"


print("Starting Build process")

print("Checking build type")

if build_type.upper() == 'LAN':
    print("Running Lan network deployment")
    print("Opening GNS3 Lab and powering on nodes")

    g = GNS3(gns3_server, gns3_port, "basenetwork1")
    id = g.find_project_id()
    print(g.open_project(id))
    print(g.start_nodes(id))

    ansible = BuildAnsible("hosts")

    print("Running the deployment scripts")

    deploy = ansible.run_script("mini-lan-ssh")
    if not deploy:
        print("Something went wrong")
        exit(1)

    print("Running base test case")
    base_test = "'script={0} ips=192.168.12.1,192.168.12.2,192.168.12.3'".format(build_path("testcases", "connectivity_check.py"))

    base = ansible.run_script("deploy_file", parameters=base_test)
    if not base:
        #Should put a exit handle function here.
        print("Something went wrong")
        exit(1)

    print("Test ran, job completed. Have a nice day :-)")


elif build_type.upper() == 'CLOUD':
    print("Running Cloud network deployment")
    # This will be a deployment into azure where we test the network secutriy groups along with the nodes which can run routing rules.

    print("Creating azure nodes")
    #Naming convention should be Subnet-vm-num
    vms = [{"vm_name": "Office1-VM", "ip_assignment_type":"Static", "ip_address":"192.168.11.10"},
           {"vm_name":"Office2-VM", "ip_assignment_type":"Static", "ip_address":"192.168.12.10"},
           {"vm_name":"Office3-VM", "ip_assignment_type":"Static", "ip_address":"192.168.13.10"}]
    azure_nodes = []
    azure_api = AzureApi()
    for vm in vms:
        node = azure_api.create_node(vmname=vm["vm_name"], subnet=vm["vm_name"].split("-")[0],
                                     ip_assignment_type=vm["ip_assignment_type"], ip_address=vm["ip_address"])
        
        azure_nodes.append(AzureNode(name=node['vm'].name, resource_group=node['resource_group'],
                                     nic_name=node['nic_name'], nic_ip=node['nic_ip'],
                                     disk_name=node['disk_name']))

    print("Cloud nodes deployed, moving on the base deployment")



    '''
    print("deleting the azure nodes")
    for vm in azure_nodes:
        status = azure_api.delete_node(vm)
        print(status)
        if status == "succeeded":
            print("{0} deleted".format(vm['name']))
        else:
            print("Something went wrong when deleting the node. ")
    '''
