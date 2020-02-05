from BulidBin.do_api import DoApi


class NetworkNode:

    __init__(self, id, name, public_ip, private_ip):
        self.id = id
        self.name = name
        self.public_ip = public_ip
        self.private_ip = private_ip

    get_public_ip(self):
        return self.public_ip

    get_private_ip(self):
        return self.private_ip

    get_id(self):
        return self.id

    check_status(self):
        return DoApi.get_last_action(self.id)
