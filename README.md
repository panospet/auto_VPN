# auto_VPN
### Implementation for a VPN server-client set up using OpenVPN

#### Server side
Just put this repo inside your /var/www/ folder.

To serve the Flask application so that the clients can download their script:
1. Apache2, easy-rsa and OpenVPN packages need to be installed in your system.
2. Read here (http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/) how you can setup apache server
to handle wsgi. This is needed to be able to run Flask framework.
3. Make it work by running
    sudo openvpn --config /path/to/server.conf
It is better to enter absolute path to file server.conf. You can use the --daemon option to run it as a
daemon as well.
4. pbkdf2 package is borrowed from here. https://github.com/dlitz/python-pbkdf2 Please clone and run 
setup.py, then rename 'python-pbkdf2' folder to 'pbkdf2'.

#### Client side
Just download the script that the server gives to you, and run it.
Demonstration here: https://83.212.116.170/login
