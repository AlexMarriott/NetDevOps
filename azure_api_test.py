
from BuildBin.azure.azure_api import AzureApi
from BuildBin.azure.models import AzureNode
import unittest
import json

class AzureApiTest(unittest.TestCase):

    @staticmethod
    def setup():
        azure_api = AzureApi()
        names = ["T1AinTest", "T2AinTest", "T3AinTest"]
        azure_api.create_droplets(names=names)
        nodes = azure_api.list_droplets()
        return nodes

    @staticmethod
    def clean_up():
        azure_api = AzureApi()
        nodes = azure_api.list_droplets()
        for i in nodes:
            print("Deleting nodes:{0}".format(i['name']))
            print("Respones: {0}".format(azure_api.delete_droplet(i['id'])))

    def test_create_node(self):
        print("Running create azure node test")
        azure_api = AzureApi()
        test_nodes = [{"node": "T1AinTest", "nic": 'T1AinTest01', "disk":"T1AinTest01Disk123" },
                      {"node": "T2AinTest", "nic": 'T2AinTest02', "disk":"T1AinTest01Disk123"},
                      {"node": "T3AinTest", "nic": 'T3AinTest03', "disk":"T1AinTest01Disk123"}]
        test_node_objects = []
        for node in test_nodes:
            vm = azure_api.create_node(vmname=node['node'], nic_name=node['nic'])


            test_node_objects.append(AzureNode(name=vm['vm'].name,
                                               resource_group=vm['resource_group'],
                                               nic_name=vm['nic_name'],
                                               nic_ip=vm['nic_ip'],
                                               disk_name=vm['disk_name']))
            print(test_node_objects)

        print(test_node_objects[0].__dict__)
        print(test_node_objects[0].name,test_node_objects[0].resource_group,test_node_objects[0].nic_name)
        print(test_node_objects[1].__dict__)
        print(test_node_objects[2].__dict__)

        #self.assertEqual(resp['status_code'], 202)
        #self.clean_up()

    def test_get_network_nodes(self):
        pass
        azure_api = AzureApi()
        nodes = azure_api.list_nodes()
    
    def test_delete_node(self):
        azure_api = AzureApi()

        test_nodes = [{"node": "T1AinTest", "nic": 'T1AinTest01', "disk": "T1AinTest01Disk123"},
                      {"node": "T2AinTest", "nic": 'T2AinTest02', "disk": "T1AinTest01Disk123"},
                      {"node": "T3AinTest", "nic": 'T3AinTest03', "disk": "T1AinTest01Disk123"}]
        test_node_objects = []
        for node in test_nodes:
            vm = azure_api.create_node(vmname=node['node'], nic_name=node['nic'])

            test_node_objects.append(AzureNode(name=vm['vm'].name,
                                               resource_group=vm['resource_group'],
                                               nic_name=vm['nic_name'],
                                               nic_ip=vm['nic_ip'],
                                               disk_name=vm['disk_name']))
        
        for node in test_node_objects:
            async_delete = azure_api.delete_node(node)
            async_delete.wait()
