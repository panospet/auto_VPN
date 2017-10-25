# auto_VPN
### Implementation for a VPN server-client set up using OpenVPN

#### Server side
Put this repo inside your /var/www/ folder.

To serve the Flask application so that the clients can download their script:
1. Apache2, easy-rsa and OpenVPN packages need to be installed in your system.
2. Read here (http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/) how you can setup apache server
to handle wsgi. This is needed to be able to run Flask framework.
3. Run OpenVPN in server mode by running the command:
    `sudo openvpn --config /path/to/server.conf`
It is better to enter absolute path to file `server.conf`. You can use the `--daemon` option to run it as a
daemon as well.
4. Copy the contents of `apache_conf` folder to your apache configuration. `/etc/apache2/sites-enabled` is the default place.
5. Copy the contents of `easy_rsa_scripts` folder to your `easy-rsa` folder. `/usr/share/easy-rsa` is the default place.
6. `pbkdf2` package is borrowed from here. https://github.com/dlitz/python-pbkdf2 Please clone and run 
setup.py, then rename 'python-pbkdf2' folder to 'pbkdf2'.
7. To manage users, a database needs to be created by running `create_db.py`.
8. The application is ready to run. Note: Of course the internal services of the application are not included in this repository. Every website installed in `/var/www/html` folder is served only for clients connected to the VPN network.

#### Client side
Enter to the address of the server you deployed above and login with your credentials. Depending on the OS that you are running, fill the correct form with the number of minutes you want to connect. Download the bundle and run the script.

Demonstration here: https://83.212.116.170/login
