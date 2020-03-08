import json

from requests import session

r = session()

username = 'admin'
password = 'eve'
url = 'http://192.168.59.129'
def login():

    return r.post('{0}/api/auth/login'.format(url), json={'username': username, 'password':password})

def get_users():
    return r.get('{0}/api/users/'.format(url))
def get_lab(lab_name):
    host = '{0}/api/labs/apiuser/network_1583580511021.unl'.format(url)
    print(host)
    return r.get(host)

#def get_all_labs():
#    return r.get('{0}/api/labs/{1}/legacy/dev-network.unl'.format(host,blah='yes'))

print(login().text)
print(json.loads(get_users().text))
#print(get_all_labs().text)
print(get_lab('legacy/dev-network.unl/topology').text)