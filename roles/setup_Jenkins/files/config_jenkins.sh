#!/bin/sh
sudo tar -xzvf jenkins.tar.gz
sudo rm -rf /var/lib/jenkins/
sudo mv jenkins/ /var/lib/
