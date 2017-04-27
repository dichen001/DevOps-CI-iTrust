#!/bin/sh
# name: Di Chen, UnityId: dchen20
# automatically configure a server running jenkins.
#  automatically setup a job to build this repo

sudo npm install
export ANSIBLE_HOST_KEY_CHECKING=False
node AWS.js
echo "\nWait for 15 seconds..."
sleep 15s
ansible-playbook ansible-playbook.yml -i Inventory
