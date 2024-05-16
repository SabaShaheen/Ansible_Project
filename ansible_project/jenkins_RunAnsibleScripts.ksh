#!/bin/ksh
export PLAYBOOK=$1
export inventory=$2
export PLAYBOOK_ARGS=$3
export PIP_CONFIG_FILE=/lch/jenkins/venv3/bin/pip.conf
source /lch/jenkins/venv3/bin/activate
source_root='git rev-parse --show-toplevel'
git config --global http.sslVerify "false"

ansible-playbook -v ${source_root}${PLAYBOOK} -i ${source_root}${inventory} -e "${PLAYBOOK_ARGS}"
