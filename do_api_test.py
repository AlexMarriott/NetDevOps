import unittest
from BuildBin.do_api import DoApi


class Do_Api_Test(unittest.TestCase):

    def clean_up(self):
        do_api = DoApi()
        nodes = do_api.list_droplets()
        for i in nodes:
            print("Deleting nodes:{0}".format(i['name']))
            print("Respones: {0}".format(do_api.delete_droplet(i)))

    def test_create_droplet(self):
        do_api = DoApi()
        names = ['T1.ain.test", "T2.ain.test", "T3.ain.test']
        self.assertEqual(do_api.create_droplets(names=names)['status_code'], 201)
        self.clean_up()
