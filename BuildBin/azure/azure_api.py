from .azure_credentials import get_credentials, get_subscription
from azure.mgmt.resource.resources.models import DeploymentMode
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from msrestazure.azure_exceptions import CloudError
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
        self.blob_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=deploymentscriptsdiss;AccountKey=g1vYoqg06Ir5fM3dRW4kNBJFJV5DdqHR25EnNFS4ujin4df+oRL/bvxQcOCmK9IPMaB6eZ9ze1hS92HkkkijsA==;EndpointSuffix=core.windows.net")

        self.vm_template = self.get_templates(os.path.abspath("BuildBin/azure/templates/create_linux.json"))
        self.nic_template = self.get_templates(os.path.abspath("BuildBin/azure/templates/create_nic.json"))
        self.rg_template = self.get_templates(os.path.abspath("BuildBin/azure/templates/create_rg.json"))

    def file_upload(self, file_name, local_path):
        # Used for uploading the deployment files to azure blob storage

        # Create a file in local data directory to upload and download


        upload_file_path = os.path.join(local_path, file_name)

        # Create a blob client using the local file name as the name for the blob

        blob_client = self.blob_client.get_blob_client(container="deploymentscripts", blob=file_name)


        print("\nUploading to Azure Storage as blob:\n\t" + file_name)

        # Upload the created file
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        return blob_client.get_blob_properties()

    def create_node(self, vmname="R1TestNode", nic_name=None, subnet=None, ip_assignment_type=None, ip_address=None):
        if nic_name is None:
            nic_name = vmname + str(random.randint(1, 100) * 5)
        if subnet is None:
            subnet = "Office1"
        if ip_assignment_type is None or ip_address is None:
            ip_assignment_type = "Dynamic"
            ip_address = ''

        print(ip_assignment_type)
        print(ip_address)

        parameters = {'networkInterfaceName': nic_name, 'location': 'uksouth', 'subnetId': subnet}
        parameters = parameterise_values(parameters)

        # Create network interface card for the node
        print("Creating:{0}".format(nic_name))
        template = self.prepare_nic_template(
            self.resource_group,
            subnet=subnet,
            ip_assignment_type=ip_assignment_type,
            ip_address=ip_address)
        print(template)
        nic_deployment_async_operation = self.network_client.network_interfaces.create_or_update(self.resource_group,
                                                                                                 nic_name,
                                                                                                 self.prepare_nic_template(
                                                                                                     self.resource_group,
                                                                                                     subnet=subnet,
                                                                                                     ip_assignment_type=ip_assignment_type,
                                                                                                     ip_address=ip_address))
        # network_interface_name=parameters['networkInterfaceName']))
        nic_deployment_async_operation.wait()

        print("Creating:{0}".format(vmname))

        deployment_async_operation = self.compute_client.virtual_machines.create_or_update(self.resource_group, vmname,
                                                                                           self.prepare_vm_template(
                                                                                               self.resource_group,
                                                                                               nic_name,
                                                                                               vmname))
        deployment_async_operation.wait()
        vm = self.compute_client.virtual_machines.get(self.resource_group, vmname)
        nic_ip = self.network_client.network_interfaces.get(self.resource_group, nic_name)
        disk_name = vm.storage_profile.os_disk.name

        return {"vm": vm,
                "resource_group": self.resource_group,
                "nic_name": nic_name,
                "nic_ip": nic_ip.ip_configurations[0].private_ip_address,
                "disk_name": disk_name}

    def get_node(self, vmname, expand=""):
        return self.compute_client.virtual_machines.get(self.resource_group, vmname,
                                                        paramaters={"$expand={0}".format(expand)})

    def delete_node(self, node):
        try:
            print("deleting resource group :{0}".format(node.name))
            async_delete = self.compute_client.virtual_machines.delete(self.resource_group, node.name)
            async_delete.wait()
            print(async_delete.status())

            async_nic_delete = self.network_client.network_interfaces.delete(self.resource_group, node.nic_name)
            print("deleting nic :{0}".format(node.nic_name))

            async_nic_delete.wait()
            print(async_nic_delete.status())

            async_disk_delete = self.compute_client.disks.delete(self.resource_group, node.disk_name)
            print("deleting disk :{0}".format(node.disk_name))
            async_disk_delete.wait()
            print(async_disk_delete.status())

            return async_delete.status()

        except CloudError as e:
            print(e)
            return 404
        return 404

    def get_templates(self, template):
        with open(template, 'r') as template_file_fd:
            return json.load(template_file_fd)

    def prepare_nic_template(self,
                             resource_group,
                             network_interface_name='test_nice_' + str(random.randint(1, 10) * 5),
                             location="uksouth",
                             subnet="Office1",
                             ip_assignment_type="Dynamic",
                             ip_address=""):
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
                            "privateIPAllocationMethod": "{0}".format(ip_assignment_type),
                            "privateIPAddress": "{0}".format(ip_address),
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
                        "id": "/subscriptions/8da87477-14ec-488c-a181-1dbdcc25525e/resourceGroups/{0}/providers/Microsoft.Network/networkInterfaces/{1}".format(
                            resource_group, nic_name),
                        "properties": {
                            "primary": "true"
                        }
                    }
                ]
            }
        }
