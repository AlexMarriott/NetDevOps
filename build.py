"""This is the main build python file for the network deplyoment."""
from BuildBin.do_api import DoAPI


do = DoAPI

nodes = do.list_droplets()
for i in nodes:
    print(do.get_droplet(i))
