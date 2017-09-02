#!/bin/bash

username=$1

client_key_file="/usr/share/easy-rsa/keys/"$username".key"
client_crt_file="/usr/share/easy-rsa/keys/"$username".crt"

echo $client_key_file
echo $client_crt_file

if [ -f $client_key_file -a -f $client_crt_file ];
then
    echo "Key and certificate files already exist for this user."
else
    cd /usr/share/easy-rsa; . ./vars; ./build-key --batch $username
fi



