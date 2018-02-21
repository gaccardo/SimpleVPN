#!/bin/bash

function check_status {
  if [ "$?" -ne 0 ];
  then
    echo "$1: failed"
    exit 1
  fi
}

cd /opt/simplevpn
apt install ansible -y

chown -R svpn:svpn /opt/simplevpn

ansible-playbook -i "localhost," \
                 -c local deploy/playbooks/dependencies/service_user.yml
check_status "dependencies -> service user"

ansible-playbook -i "localhost," \
                 -c local deploy/playbooks/dependencies/virtualenv.yml
check_status "dependencies -> virtualenv"
