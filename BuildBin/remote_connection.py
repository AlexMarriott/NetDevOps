from paramiko import SSHClient, WarningPolicy
from paramiko import BadHostKeyException, AuthenticationException, SSHException

class RemoteSSH:
    def __init__(self, hostname, username, password, port=22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(WarningPolicy)


    def connect(self):
        try:
            self.client.connect(hostname=self.hostname, port=self.port,
                       username=self.username, password=self.password)
            return True
        except (BadHostKeyException, AuthenticationException, SSHException) as e:
            print(e)
            return False

    def disconnect(self):
        self.client.close()

    def permission_check(self, file):
        pass
    def exec_command(self, command, bufsize=1, timeout=30):
        try:
            stdin, stdout, stderr = self.client.exec_command(command, bufsize, timeout)
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                print("Command completed!")
                return (True, stdout.read(), exit_status)
            else:
                print("Error", exit_status)
                print(stdout.read(), stderr.read())
                return (False, stderr.read(), exit_status)
        except SSHException as e:
            print("error")
            print(e)
            return stderr.read()
