from .common import build_path

class BuildAnsible():
    def __init__(self, host_file):
        self.host_file = host_file

    def run_script(self, script_name, parameters=None):
        #https://stackoverflow.com/questions/57763068/how-to-run-ansible-playbooks-with-subprocess
        script_path = build_path("ansible_files",script_name)
        host_file = build_path("ansible_files", "hosts")
        if parameters is not None:
            new_parameters = "{0}.yaml --extra-vars {1}".format(script_path ,parameters)
        else:
            new_parameters = "{0}.yaml".format(script_path)

        print("Running ansible script")
        print(new_parameters)
        print(host_file)
        try:
            os.system("ansible-playbook -i {0} {1} -vvvv".format(host_file, new_parameters))
            return True
        except Exception as e:
            print(e)
            return False