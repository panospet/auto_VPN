#!/bin/bash

source /usr/share/easy-rsa/vars 
/usr/share/easy-rsa/revoke-full $1

{
    sleep 3
    echo kill $1
    sleep 3
    echo exit
} | telnet localhost 7505

