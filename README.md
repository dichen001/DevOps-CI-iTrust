#DevOps Milestone 3 Rolling Update for iTrust
Auto following Steps:
  1. Provision AWS servers  (e.g. 1 master with 5 slave nodes) 
  2. Config Inventory and Haproxy  
  3. Create Github WebHook with Jenkins 
  4. Env Setup for iTrust (tomcat, mysql)  
  5. Jenkins Setup(auto build, test coverage analysis, build results analysis. rolling update for slave nodes)

## How To Run?

change access key in `AWS.js` with yours
then set your `secretKey`
```
npm install
export secretKey=[your sercret key]
echo $secretKey
```
### Provision 1 Master Node and 5 Slave Node on AWS
```
bash aws.sh 
```

### Update Invetory and Haproxy.cfg & Create GitHub WebHook for Master Node

(I'm using my own fork of iTrust in NCSU GitHub [https://github.ncsu.edu/dchen20/iTrust-v23](https://github.ncsu.edu/dchen20/iTrust-v23))
```
python ip_function.py 
```

### Config Master and Slave Nodes with Ansible PlayBook
```
sudo ansible-playbook -i inventory iTrust.yml -s
```

## Master Node
- ip: redirect to slave nodes on [slave_ip:8080/iTrust] in a round roubin way.
- ip:1111 `Haproxy Console`
- ip:6060 `Jenkins`
    - iTurst: `triggered by GitHub pull requests, build iTrust. If build success, triger rolling update to build slave nodes`
    - Auto_Rolling_Updates: `triggered by succesful build of iTrust. round robin update slave node`
- ip:8080  `Tomcat`
- ip:8080/iTrust `iTrust`

## Slave Nodes
- ip:8080  `Tomcat`
- ip:8080/iTrust `iTrust`
