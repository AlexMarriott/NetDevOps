import unittest
from BuildBin.azure.azure_api import AzureApi


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
        test_nodes = [{"node": "T1AinTest", "nic": 'T1AinTest01'},
                      {"node": "T2AinTest", "nic": 'T2AinTest02'},
                      {"node": "T3AinTest", "nic": 'T3AinTest03'}]

        for test_node in test_nodes:
            resp = azure_api.create_node(vmname=test_node['node'])
            print(resp)
        #self.assertEqual(resp['status_code'], 202)
        #self.clean_up()