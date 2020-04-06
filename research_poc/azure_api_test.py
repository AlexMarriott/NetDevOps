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
    def clean_up(nodes):
        azure_api = AzureApi()
        for node in nodes:
            if isinstance(nodes, dict):
                node = AzureNode(name=node['node'],
                                 resource_group="test",
                                 nic_name=node['nic'],
                                 nic_ip='192.168.1.1',
                                 disk_name=node['disk'])

            print("deleteing: {0}".format(node))
            azure_api.delete_node(node)

    def test_create_node(self):
        print("Running create azure node test")
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
        try:
            self.assertEqual(test_node_objects[0].name, test_nodes[0]['node'])
            self.assertEqual(test_node_objects[0].name, test_nodes[0]['nic'])
            self.assertEqual(test_node_objects[0].name, test_nodes[0]['disk'])
            self.clean_up(test_node_objects)
        except AssertionError as e:
            print(e)
            self.clean_up(test_nodes)

    def test_get_network_nodes(self):
        pass

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
            print("deleting: {0}".format(node))
            self.assertEquals(azure_api.delete_node(node), "succeeded")
