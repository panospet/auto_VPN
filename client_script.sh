#!/bin/bash

python client_script.py

#clear
echo "Starting VPN connection in 5 seconds, press CTRL-C anytime to stop"
sleep 1
#clear
echo "Starting VPN connection in 4 seconds, press CTRL-C anytime to stop"
sleep 1
#clear
echo "Starting VPN connection in 3 seconds, press CTRL-C anytime to stop"
sleep 1
#clear
echo "Starting VPN connection in 2 seconds, press CTRL-C anytime to stop"
sleep 1
#clear
echo "Starting VPN connection in 1 seconds, press CTRL-C anytime to stop"
sleep 1
#clear

echo "Starting OpenVPN..."
sleep 2

sudo openvpn --config client.conf

rm -rf $CLIENTCRT $CLIENTKEY $CLIENTCONF $CACERTFILE

echo "Thank you for using our VPN service! :-)"

