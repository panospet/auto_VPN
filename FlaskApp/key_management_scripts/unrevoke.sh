#!/bin/bash

keys_index_file=/usr/share/easy-rsa/keys/index.txt

linenumber="$(grep -n "/CN=$1/" $keys_index_file | cut -f1 -d:)"
echo $linenumber

fileline="$(grep -n "/CN=$1/" $keys_index_file)"
echo $fileline

column2="$(echo $fileline | awk '{print $2}')"
echo $column2

column4="$(echo $fileline | awk '{print $4}')"
echo $column4

column5="$(echo $fileline | awk '{print $5}')"
echo $column5

column6="$(echo $fileline | awk '{print $6}')"
echo $column6

echo -e "V\t$column2\t\t$column4\t$column5\t$column6" >> $keys_index_file

sed -i "${linenumber}d" $keys_index_file

# source /usr/share/easy-rsa/vars
# openssl ca -gencrl -out "/usr/share/easy-rsa/keys/crl.pem" -config "$KEY_CONFIG"
cd /usr/share/easy-rsa; source ./vars ; ./generate_crl_file.sh
