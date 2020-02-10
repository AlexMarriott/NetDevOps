

class azure_node(object):

    def __init__(self):
        self.name = ""
        self.resource_group = ""
        self.nic_name = ""
        self.nic_ip = ""

    def get_resourcegroup(self):
        return self.resource_group

    def get_name(self):
        return self.name

    def get_nic_name(self):
        return self.nic_name

    def get_ip(self):
        return self.nic_ip
