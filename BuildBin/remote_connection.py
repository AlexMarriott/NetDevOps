from paramiko import SSHClient, WarningPolicy
from paramiko import BadHostKeyException, AuthenticationException, SSHException


class RemoteSSH:

    """
    This Class is the uses the paramiko library to connect to devices during the build process
    and run commands on the remote system.
    """

    def __init__(self, hostname, username, password, port=22):
        """
        The init function takes the necessary parameters to instantiate an instance of SSHclient
        :param hostname:
        :param username: String, username used for remote authentication
        :param password: String, used for authenticating with the remote device
        :param port: int, port number for the remote ssh port
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(WarningPolicy)

    def connect(self):
        """
        This function is used to connect to the remote device

        :param self:
        :return: True if the connection is successful or False is an expectation is thrown, or connection to the remote device fails
        """
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
        """
        This function is used run commands on the remote system.
        :param self:
        :param command: String, the command to run on the remote device
        :param bufsize: Interpreted the same way as by the built-in file() function in Python
        :param timeout: int, if no response is returned, the command will timeout.
        :return: Returns the standard output from the command ran or the error returned from the remote system.
        """
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
