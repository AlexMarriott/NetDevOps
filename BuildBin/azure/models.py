class AzureNode(object):
    """
    The Azure Node class is used to retain information of the running azure vms for the CI/CD pipeline.
    """
    def __init__(self, name, resource_group, nic_name, nic_ip, disk_name, public_ip=''):
        """
        The init function takes the necessary parameters to instantiate an instance of AzureNode
        :param name: String,  Name of the VM
        :param resource_group: String,  resource group which the VM belongs to
        :param nic_name: String, The name of the network card
        :param nic_ip: String, The Ip address for the network card
        :param disk_name: String, The name of the VM's disk
        :param public_ip: String, The public IP address for the network card, if it has one.

        """
        self.name = name
        self.resource_group = resource_group
        self.nic_name = nic_name
        self.nic_ip = nic_ip
        self.disk_name = disk_name
        self.public_ip = public_ip

    def get_resourcegroup(self):
        """
        The get_resourcegroup function returns which resource_group the azurenode objects belongs to
        :param self:
        :return: Returns the resource_group of the object.
        """
        return self.resource_group

    def get_name(self):
        """
        The get_name function returns the name of the azurenode.
        :param self:
        :return: Returns the name of the vm.
        """
        return self.name

    def get_nic_name(self):
        """
        The get_nic_name function returns the Network card name of the VM
        :return: Returns the network card name of the object.
        """
        return self.nic_name

    def get_ip(self):
        """
        The get_ip function returns the IP address of the network card
        :param self:
        :return: Returns the IP address of the object.
        """
        return self.nic_ip
