import os

class BuildAnsible():
    """
    The BuildAnsible class is used to control the ansible runs and better formalise the dependencies needed to run the playbooks
    """
    def __init__(self, host_file):
        """
        The init function takes the necessary parameters to instantiate an instance of BuildAnsible
        :param name: String, The location of the host file for the ansible runs.
        """
        self.host_file = host_file

    def run_script(self, script_name, script_path, parameters=None):
        """
        The run_script function takes the script name, path and additional parameters for the ansible playbook runs.
        :param script_name: String, The ansible playbook to run.
        :param script_path: String, The location of the ansible playbook
        :param parameters: String, Additional parameters to be passed to the playbook
        :return: True if the playbook ran correctly, False if the playbook could not be ran or exceptions were thrown during the execution.
        """
        if parameters is not None:
            new_parameters = os.path.abspath("{0}/{1}.yaml --extra-vars {2}".format(script_path, script_name, parameters))
        else:
            new_parameters = os.path.abspath("{0}/{1}.yaml".format(script_path, script_name))

        print("Running ansible script: {0}".format(script_name))
        try:
            print("ansible-playbook -i {0} {1} -vvvv".format(self.host_file, new_parameters))
            os.system("ansible-playbook -i {0} {1} -vvvv".format(self.host_file, new_parameters))
            return True
        except Exception as e:
            print(e)
            return False