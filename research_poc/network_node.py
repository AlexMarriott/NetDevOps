from BulidBin.do_api import DoApi


class NetworkNode:

    def __init__(self, id, name, public_ip, private_ip):
        self.id = id
        self.name = name
        self.public_ip = public_ip
        self.private_ip = private_ip

    def get_public_ip(self):
        return self.public_ip

    def get_private_ip(self):
        return self.private_ip

    def get_id(self):
        return self.id

    def check_status(self):
        return DoApi.get_last_action(self.id)
