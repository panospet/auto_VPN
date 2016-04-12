#!/bin/bash

USERNAME=test
PASSWORD=test

CACERTFILE="ca.crt"
CLIENTCRT="client.crt"
CLIENTKEY="client.key"
CLIENTCONF="client.conf"

openssl s_client -showcerts -connect 83.212.116.170:443/login </dev/null 2>/dev/null|openssl x509 -outform PEM > mycertfile.pem

curl --cacert mycertfile.pem --cookie-jar cookies_temp 'https://83.212.116.170/login' --data 'username=test&password=test&submit=Login'

curl --cacert mycertfile.pem --cookie cookies_temp 'https://83.212.116.170/cacert' > $CACERTFILE

curl --cacert mycertfile.pem --cookie cookies_temp 'https://83.212.116.170/clientcert' > $CLIENTCRT

curl --cacert mycertfile.pem --cookie cookies_temp 'https://83.212.116.170/clientkey' > $CLIENTKEY

curl --cacert mycertfile.pem --cookie cookies_temp 'https://83.212.116.170/logout'

rm -rf cookies_temp mycertfile.pem



echo "# OpenVPN client configuration file example" > $CLIENTCONF

echo "client" >> $CLIENTCONF

echo "dev tun" >> $CLIENTCONF

echo "remote 83.212.116.170" >> $CLIENTCONF

echo "ca $CACERTFILE" >> $CLIENTCONF

echo "cert $CLIENTCRT" >> $CLIENTCONF

echo "key $CLIENTKEY" >> $CLIENTCONF

echo "comp-lzo" >> $CLIENTCONF

echo "keepalive 10 60" >> $CLIENTCONF

echo "ping-timer-rem" >> $CLIENTCONF

echo "persist-tun" >> $CLIENTCONF

echo "persist-key" >> $CLIENTCONF

echo "user $USER" >> $CLIENTCONF

echo "group $USER" >> $CLIENTCONF

clear
echo "Starting VPN connection in 5 seconds, press CTRL-C anytime to stop"
sleep 1
clear
echo "Starting VPN connection in 4 seconds, press CTRL-C anytime to stop"
sleep 1
clear
echo "Starting VPN connection in 3 seconds, press CTRL-C anytime to stop"
sleep 1
clear
echo "Starting VPN connection in 2 seconds, press CTRL-C anytime to stop"
sleep 1
clear
echo "Starting VPN connection in 1 seconds, press CTRL-C anytime to stop"
sleep 1
clear

echo "Starting OpenVPN..."
sleep 2

sudo openvpn --config client.conf

rm -rf $CLIENTCRT $CLIENTKEY $CLIENTCONF $CACERTFILE

clear
echo "Thank you for using our VPN service! :-)"

