from .azure_credentials import get_credentials, get_subscription
from azure.mgmt.compute import ComputeManagementClient
import requests

class AzureApi:

    def __init__(self):
        self.credentials = get_credentials()
        self.subscription = get_subscription()
        self.resource_group = "TestNetwork"
        self.client = ComputeManagementClient(self.credentials, self.subscription)


    def create_node(self, names=None):
        create
        client.virtual_machines.create_or_update(resource_group, )
