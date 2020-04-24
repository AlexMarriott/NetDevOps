class AzureNode(object):
    """
    The init function takes the necessary parameters to instantiate an instance of SSHclient
            :param hostname:
            :param username: String, username used for remote authentication
            :param password: String, used for authenticating with the remote device
            :param port: int, port number for the remote ssh port
    """
    def __init__(self, name, resource_group, nic_name, nic_ip, disk_name, public_ip=''):
        self.name = name
        self.resource_group = resource_group
        self.nic_name = nic_name
        self.nic_ip = nic_ip
        self.disk_name = disk_name
        self.public_ip = public_ip

    def get_resourcegroup(self):
        return self.resource_group

    def get_name(self):
        return self.name

    def get_nic_name(self):
        return self.nic_name

    def get_ip(self):
        return self.nic_ip
