import os
from .common import build_path

class BuildAnsible():
    def __init__(self, host_file):
        self.host_file = host_file

    def run_script(self, script_name, script_path, parameters=None):
        if parameters is not None:
            new_parameters = os.path.abspath("{0}/{1}.yaml --extra-vars {2}".format(script_path, script_name, parameters))
        else:
            new_parameters =  os.path.abspath("{0}/{1}.yaml".format(script_path, script_name))

        print("Running ansible script: {0}".format(script_name))
        try:
            os.system("ansible-playbook -i {0} {1} -vvvv".format(self.host_file, new_parameters))
            return True
        except Exception as e:
            print(e)
            return False