#!/bin/bash

keys_index_file=/usr/share/easy-rsa/keys/index.txt
linenumber="$(grep -n "/CN=$1/" $keys_index_file | cut -f1 -d:)"
fileline="$(grep -n "/CN=$1/" $keys_index_file)"
line="$(grep "/CN=$1/" $keys_index_file)"

columns_number="$(echo $line | awk -F' ' '{print NF;}')"
echo $columns_number



if [[ $columns_number -eq 6 ]] && [[ $line == R* ]]; then

    column2="$(echo $fileline | awk '{print $2}')"
    column4="$(echo $fileline | awk '{print $4}')"
    column5="$(echo $fileline | awk '{print $5}')"
    column6="$(echo $fileline | awk '{print $6}')"
    echo -e "V\t$column2\t\t$column4\t$column5\t$column6" >> $keys_index_file
    sed -i "${linenumber}d" $keys_index_file
    cd /usr/share/easy-rsa; source ./vars; ./generate_crl_file.sh

    echo "Certificate unrevoked successfully."
    exit 0;

elif [[ $columns_number -eq 5 ]] && [[ $fileline == V* ]]; then

    echo "Certificate is already unrevoked and active"
    exit 0;

else

    echo "Error; Key index file may be corrupted."
    exit 1;

fi
