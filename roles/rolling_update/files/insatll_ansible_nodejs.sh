#!/bin/bash
#deploy the environment
# install ansible
sudo apt-get install -y software-properties-common
sudo apt-add-repository -y ppa:ansible/ansible
sudo apt-get update
sudo apt-get install -y ansible

# install node js
sudo apt-get install -y python-software-properties
curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo apt-get install -y build-essential
node npm install

# install haproxy
sudo add-apt-repository -y ppa:vbernat/haproxy-1.6
sudo apt-get install -y haproxy
sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.original
sudo mv -f ~/haproxy.cfg /etc/haproxy/
sudo service haproxy restart

# # creat slave nodes
# export secretKey=Mx4YWF5tXqXIdbmuBO1PzT+s+miUDvJH6xAA4zF1
# node AWS-6.js
#
# ansible-playbook -i inventory ./jenkins/main.yml
# ansible-playbook -i inventory ./iTrust/main.yml

# ansible-playbook -i inventory ./checkbox.io/main.yml
#deploy jenkins in local host
