import unittest
from BuildBin.do_api import DoApi


class Do_Api_Test(unittest.TestCase):

    @staticmethod
    def setup():
        do_api = DoApi()
        names = ["T1.ain.test", "T2.ain.test", "T3.ain.test"]
        do_api.create_droplets(names=names)
        nodes = do_api.list_droplets()
        return nodes

    @staticmethod
    def clean_up():
        do_api = DoApi()
        nodes = do_api.list_droplets()
        for i in nodes:
            print("Deleting nodes:{0}".format(i['name']))
            print("Respones: {0}".format(do_api.delete_droplet(i['id'])))

    def test_create_droplet(self):
        print("Running create droplet test")
        do_api = DoApi()
        names = ["T1.ain.test", "T2.ain.test", "T3.ain.test"]
        resp = do_api.create_droplets(names=names)
        self.assertEqual(resp['status_code'], 202)
        self.clean_up()
        
    def test_list_droplets(self):
        print("Running list droplet test")
        nodes = self.setup()
        self.assertTrue(nodes)
        self.clean_up()

    def test_delete_droplets(self):
        print("Running delete droplet test")
        do_api = DoApi()
        nodes = self.setup()
        for node in nodes:
            resp = do_api.delete_droplet(node['id'])
            self.assertEqual(resp['status_code'], 204)
        self.clean_up()

