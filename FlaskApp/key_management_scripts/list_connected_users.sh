#!/bin/bash

clients="$(/var/www/FlaskApp/FlaskApp/key_management_scripts/expect.sh | grep -e ^CLIENT_LIST)"

echo $clients | awk -F ' ' '{print $2}'
