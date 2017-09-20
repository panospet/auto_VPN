import pycurl
import certifi
import getpass

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
username = ''
password = getpass.getpass()
post_data = {'username': username, 'password': password}
postfields = urlencode(post_data)
c.setopt(pycurl.POSTFIELDS, postfields)
c.setopt(c.FOLLOWLOCATION, True)
c.setopt(pycurl.WRITEFUNCTION, lambda x: None)
c.perform()

c.setopt(pycurl.URL, 'https://83.212.116.170/cacert')
with open('ca.crt', 'w') as f:
    c.setopt(c.WRITEFUNCTION, f.write)
    c.perform()

c.setopt(pycurl.URL, 'https://83.212.116.170/clientcert')
with open('client.crt', 'w') as f:
    c.setopt(c.WRITEFUNCTION, f.write)
    c.perform()

c.setopt(pycurl.URL, 'https://83.212.116.170/clientkey')
with open('client.key', 'w') as f:
    c.setopt(c.WRITEFUNCTION, f.write)
    c.perform()

c.setopt(pycurl.URL, 'https://83.212.116.170/logout')
c.setopt(pycurl.WRITEFUNCTION, lambda x: None)
c.perform()
c.close()
