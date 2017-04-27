#!/bin/bash
echo '################################ Provisioning Servers on AWS ################################'
bash aws.sh
echo '################################ Update Inventory and Haproxy Configuration ################################'
python ip_function.py
echo '################################ Configure Jenkins for CI iTrust ################################'
sudo ansible-playbook -i Inventory m4.yml -s
eecho '################################ Great! Done~ Thanks! ################################'

