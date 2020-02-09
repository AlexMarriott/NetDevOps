import json

from .azure_credentials import get_credentials, get_subscription
from azure.mgmt.resource.resources.models import DeploymentMode
from azure.mgmt.compute import ComputeManagementClient
import requests
import random
import os


class AzureApi:

    def __init__(self):
        self.credentials = get_credentials()
        self.subscription = get_subscription()
        self.resource_group = "TestNetwork"
        self.client = ComputeManagementClient(self.credentials, self.subscription)
        self.template_path = os.path.abspath("BuildBin/azure/templates/fuckazure.json")
        with open(self.template_path, 'r') as template_file_fd:
            self.template = json.load(template_file_fd)

    def create_node(self, vmname="R1TestNode", subnet="Office1"):

            # 'mode': DeploymentMode.incremental,
            # 'template': self.template,
            # 'parameters': parameters,
            # "location": "uksouth"
        print(self.template)
        deployment_async_operation = self.client.virtual_machines.create_or_update(self.resource_group, vmname, parameters={
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
      },
      "osDisk": {
        "caching": "ReadWrite",
        "managedDisk": {
          "storageAccountType": "Standard_LRS"
        },
        "name": "myVMosdisk",
        "createOption": "FromImage"
      },
    },

    "osProfile": {
      "adminUsername": "amarriott",
      "computerName": "myVM",
      "adminPassword": "Movingonup2016"
    },
    "networkProfile": {
      "networkInterfaces": [
        {
          "id": "/subscriptions/8da87477-14ec-488c-a181-1dbdcc25525e/resourceGroups/TestNetwork/providers/Microsoft.Network/networkInterfaces/memes",
          "properties": {
            "primary": "true"
          }
        }
      ]
    }
  }
)
        deployment_async_operation.wait()

        print(deployment_async_operation)
