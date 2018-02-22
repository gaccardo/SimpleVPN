#!/bin/bash
cd /etc/openvpn/openvpn-ca
source ./vars
req -nodes -newkey rsa:2048 -keyout $1.key -out $1.csr \
  -subj "/C=US/ST=BuenosAires/L=BuenosAires/O=SimpleVPN/OU=IT/CN=simplevpn.com"
mv $1.* keys/
