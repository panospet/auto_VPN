import pycurl
import certifi
import getpass
import pwd
import grp

try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode

c = pycurl.Curl()
c.setopt(pycurl.CAINFO, certifi.where())
c.setopt(pycurl.URL, 'https://83.212.116.170/login')
c.setopt(pycurl.SSL_VERIFYPEER, 0)
c.setopt(pycurl.COOKIEFILE, 'cookie.txt')
post_data = {'username': 'admin', 'password': 'admin'}
postfields = urlencode(post_data)
c.setopt(pycurl.POSTFIELDS, postfields)
c.setopt(c.FOLLOWLOCATION, True)
c.setopt(pycurl.WRITEFUNCTION, lambda x: None)
c.perform()

# Save cacert file
c.setopt(pycurl.URL, 'https://83.212.116.170/cacert')
with open('ca.crt', 'w') as f:
    c.setopt(c.WRITEFUNCTION, f.write)
    c.perform()

# Save client cert file
c.setopt(pycurl.URL, 'https://83.212.116.170/clientcert')
with open('client.crt', 'w') as f:
    c.setopt(c.WRITEFUNCTION, f.write)
    c.perform()

# Save client key file
c.setopt(pycurl.URL, 'https://83.212.116.170/clientkey')
with open('client.key', 'w') as f:
    c.setopt(c.WRITEFUNCTION, f.write)
    c.perform()

# Logout
c.setopt(pycurl.URL, 'https://83.212.116.170/logout')
c.setopt(pycurl.WRITEFUNCTION, lambda x: None)
c.perform()
c.close()


def get_group_from_username(username):
    for p in pwd.getpwall():
        if (p[0] == username):
            return grp.getgrgid(p[3])[0]

# create client.conf file
client_conf_file = open('client.conf', 'w+')
f = open('client.conf', 'a+')

f.write('# OpenVPN client configuration file example' + '\n')
f.write('client' + '\n')
f.write('dev tun' + '\n')
f.write('remote 83.212.116.170' + '\n')
f.write('ca ca.crt' + '\n')
f.write('cert client.crt' + '\n')
f.write('key client.key' + '\n')
f.write('comp-lzo' + '\n')
f.write('keepalive 10 60' + '\n')
f.write('ping-timer-rem' + '\n')
f.write('persist-tun' + '\n')
f.write('persist-key' + '\n')
f.write('user ' + getpass.getuser() + '\n')
f.write('group ' + get_group_from_username(getpass.getuser()) + '\n')
