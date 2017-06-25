#!/bin/bash
python get-pip.py
python -m pip install pycurl
python -m pip install certifi
python client_script.py

echo "Starting VPN connection in 5 seconds, press CTRL-C anytime to stop"
sleep 5
echo "Starting OpenVPN..."
sleep 2

sudo openvpn --config client.conf

rm -rf $CLIENTCRT $CLIENTKEY $CLIENTCONF $CACERTFILE

echo "Thank you for using our VPN service! :-)"

