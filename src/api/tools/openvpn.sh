#!/bin/bash
cd /etc/openvpn/openvpn-ca
source ./vars
openssl req -nodes -newkey rsa:2048 -keyout $1.key -out $1.csr \
  -subj "/C=US/ST=BuenosAires/L=BuenosAires/O=SimpleVPN/OU=IT/CN=simplevpn.com"
openssl ca -days 3650 -out $1.crt -in $1.cst \
  -subj "/C=US/ST=BuenosAires/L=BuenosAires/O=SimpleVPN/OU=IT/CN=simplevpn.com"
mv $1.* keys/

