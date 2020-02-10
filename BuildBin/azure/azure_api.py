from .azure_credentials import get_credentials, get_subscription
from azure.mgmt.resource.resources.models import DeploymentMode
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode
import requests
import random
import os
import time
import json
def parameterise_values(parameters):
    return {k: {'value': v} for k, v in parameters.items()}


class AzureApi():

    def __init__(self):
        self.credentials = get_credentials()
        self.subscription = get_subscription()
        self.resource_group = "TestNetwork"

        self.compute_client = ComputeManagementClient(self.credentials, self.subscription)
        self.network_client = NetworkManagementClient(self.credentials, self.subscription)
        self.resource_client = ResourceManagementClient(self.credentials, self.subscription)

        self.vm_template = self.get_templates(os.path.abspath("BuildBin/azure/templates/create_linux.json"))
        self.nic_template = self.get_templates(os.path.abspath("BuildBin/azure/templates/create_nic.json"))
        self.rg_template = self.get_templates(os.path.abspath("BuildBin/azure/templates/create_rg.json"))

    def create_node(self, nic_name=None, vmname="R1TestNode", subnet="Office1"):
        if nic_name is None:
            nic_name = vmname + str(random.randint(1, 100) * 5)
        resource_group = "{0}-rg".format(vmname)
        parameters = {'networkInterfaceName': nic_name, 'location': 'uksouth', 'subnetId': 'Office1'}
        parameters = parameterise_values(parameters)
        # Create a resource group for node
        self.resource_client.resource_groups.create_or_update(resource_group, parameters={'location':'uksouth'})
        # Dirtylittle fix since I need to poll thhe resource group being created.
        time.sleep(5)


        # Create network interface card for the node
        nic_deployment_async_operation = self.network_client.network_interfaces.create_or_update(resource_group, nic_name,
                                                                self.prepare_nic_template(
                                                                    resource_group,
                                                                    network_interface_name=parameters[
                                                                        'networkInterfaceName']))
        nic_deployment_async_operation

        deployment_async_operation = self.compute_client.virtual_machines.create_or_update(resource_group, vmname,
                                                                                   self.prepare_vm_template(resource_group,
                                                                                                            nic_name,
                                                                                                            vmname))
        deployment_async_operation.wait()

        return self.resource_client.resource_groups.get(resource_group)

    def get_templates(self, template):
        with open(template, 'r') as template_file_fd:
            return json.load(template_file_fd)

    def prepare_nic_template(self,
                             resource_group,
                             network_interface_name='test_nice_' + str(random.randint(1, 10) * 5),
                             location="uksouth",
                             subnet="Office1",
                             ip_assigmnet_method="Dynamic"):
        return {
            "location": "{0}".format(location),
            "type": "Microsoft.Network/networkInterfaces",
            "name": "{0}".format(network_interface_name),
            "properties": {
                "ipConfigurations": [
                    {
                        "name": "ipconfig1",
                        "properties": {
                            "privateIpAddressVersion": "IPv4",
                            "privateIPAllocationMethod": "{0}".format(ip_assigmnet_method),
                            "subnet": {
                                "id": "/subscriptions/8da87477-14ec-488c-a181-1dbdcc25525e/resourceGroups/TestNetwork/providers/Microsoft.Network/virtualNetworks/TestNetwork/subnets/{1}".format(
                                    resource_group,
                                    subnet)
                            }
                        }
                    }
                ]
            }
        }

    def prepare_vm_template(self, resource_group, nic_name, vmname='test_vm_' + str(random.randint(1, 10) * 5)):
        # Nic must have a value.
        if nic_name is None or "":
            return False
        return {
            "location": "uksouth",
            "hardwareProfile": {
                "vmSize": "Standard_B1s"
            },
            "storageProfile": {
                "imageReference": {
                    "sku": "18.04-LTS",
                    "publisher": "Canonical",
                    "version": "latest",
                    "offer": "UbuntuServer"
                }
            },
            "osDisk": {
                "caching": "ReadWrite",
                "managedDisk": {
                    "storageAccountType": "Standard_LRS"
                },
                "name": "{0}".format(vmname),
                "createOption": "FromImage"
            },

            "osProfile": {
                "adminUsername": "amarriott",
                "computerName": "{0}".format(vmname),
                "adminPassword": "Movingonup2016"
            },
            "networkProfile": {
                "networkInterfaces": [
                    {
                        "id": "/subscriptions/8da87477-14ec-488c-a181-1dbdcc25525e/resourceGroups/{0}/providers/Microsoft.Network/networkInterfaces/{1}".format(resource_group,nic_name),
                        "properties": {
                            "primary": "true"
                        }
                    }
                ]
            }
        }
