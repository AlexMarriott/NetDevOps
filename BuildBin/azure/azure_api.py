import json

from .azure_credentials import get_credentials, get_subscription
from azure.mgmt.resource.resources.models import DeploymentMode
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from.azure.mgmt.resource import ResourceGroupsOperations

import requests
import random
import os


class AzureApi:

    def __init__(self):
        self.credentials = get_credentials()
        self.subscription = get_subscription()
        self.resource_group = "TestNetwork"
        self.compute_client = ComputeManagementClient(self.credentials, self.subscription)
        self.network_client = NetworkManagementClient(self.credentials, self.subscription)
        self.template_path = os.path.abspath("BuildBin/azure/templates/fuckazure.json")
        with open(self.template_path, 'r') as template_file_fd:
            self.template = json.load(template_file_fd)

    def create_node(self, vmname="R1TestNode", subnet="Office1"):

        # Create a resource group for node

        # Create network interfacecard for the node
        self.network_client()
        parameters = {'networkInterfaceName': 'sick'}
        parameters = {k: {'value': v} for k, v in parameters.items()}
        deployment_properties = {
            'mode': DeploymentMode.incremental,
            'template': self.template,
            'parameters': parameters
        }
        deployment_async_operation = self.client.virtual_machines.create_or_update(self.resource_group, vmname, self.template
)
        deployment_async_operation.wait()

        print(deployment_async_operation)
