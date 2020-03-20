import os


def build_path(*argv):
    full_path = os.getcwd()
    given_path = ""
    for i in argv:
        print(i)
        given_path = os.path.join(given_path, i)
    return os.path.join(full_path, given_path)
