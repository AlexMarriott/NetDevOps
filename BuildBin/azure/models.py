

class AzureNode(object):

    def __init__(self, name, resource_group, nic_name, nic_ip, disk_name):
        self.name = name
        self.resource_group = resource_group
        self.nic_name = nic_name
        self.nic_ip = nic_ip
        self.disk_name = disk_name

    def get_resourcegroup(self):
        return self.resource_group

    def get_name(self):
        return self.name

    def get_nic_name(self):
        return self.nic_name

    def get_ip(self):
        return self.nic_ip
