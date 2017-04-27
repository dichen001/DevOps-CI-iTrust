#!/bin/sh
# name: Di Chen, UnityId: dchen20
cd ~/iTrust/iTrust/
mvn clean package -DskipTests
mv ~/iTrust/iTrust/target/iTrust-23.0.0.war /opt/apache-tomcat-9.0.0.M15/webapps/iTrust.war
chmod 777 /opt/apache-tomcat-9.0.0.M15/webapps/iTrust.war
