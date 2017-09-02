#!/bin/bash

source ./vars
openssl ca -gencrl -out "keys/crl.pem" -config "$KEY_CONFIG"
