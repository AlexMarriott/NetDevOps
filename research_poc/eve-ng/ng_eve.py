from requests import session
#https://www.eve-ng.net/index.php/documentation/howtos/how-to-eve-ng-api/

r = session()

username = 'apiuser'
password = ''

def login():

    return r.post('http://192.168.1.183/api/auth/login', json={'username': username, 'password':password})


def get_lab(lab_name):
    url = 'http://192.168.1.183/api/labs/{0}/dev-network.unl'.format(username)
    print(url)
    return r.get(url)

def get_all_labs():
    return r.get('http://192.168.1.183/api/labs/{0}/legacy/dev-network.unl')

print(login().text)

print(get_all_labs().text)
print(get_lab('legacy/dev-network.unl/topology').text)