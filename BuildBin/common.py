import os
"""
    This file is used to store all the common functions.
"""
def build_path(*argv):
    """
    The build_path function is used to contruct a path for files on a file system.
    example: /home/alex/blah/blah1/1.txt -> build_path("blah", "blah1")
    :param argv: sections of the path way to build the file path
    :return: file path.
    """
    full_path = os.getcwd()
    given_path = ""
    for i in argv:
        print(i)
        given_path = os.path.join(given_path, i)
    return os.path.join(full_path, given_path)
