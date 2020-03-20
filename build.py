import sys
import os

from BuildBin.buildansible import BuildAnsible
from BuildBin.gns3 import GNS3
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
    pass