"extract IPs from inventory. add to haproxy.cfg for rolling update"
# command
# python function.py "IPs"


import sys
import os
import requests
import json
cwd = os.getcwd()


# read ip list from command line
if len(sys.argv) != 2:
	filename = os.path.join(cwd, 'Inventory')
	print "default inventory name: \'Inventory\'"
else:
	filename = sys.argv[1]

print 'extracting IPs from file: ' + filename



# store ip to file
ip_list = []
write_flag = False

with open(filename, 'r') as f1:
    # Read non-empty lines from input file
	master_IP = ''
	IPs = []
	lines = [line for line in f1]
	for line in lines:
		if line.startswith('aws_slave_server'):
			IPs += [line.split()[1].split('=')[-1]]
		if line.startswith('aws_master_server'):
			master_IP = line.split()[1].split('=')[-1]




# inventory for master
with open(filename, 'w') as output:
	count = 0
	for i, line in enumerate(lines):
		if line.startswith('aws_slave_server'):
			x = len('aws_slave_server')
			lines[i] = line[:x] + '-' + str(count) + line[x:]
			count += 1
		output.write(lines[i])

# inventory for slaves (rolling updates)
with open('/'.join(filename.split('/')[:-1]) + '/roles/rolling_update/files/Inventory', 'w') as output:
	for i, line in enumerate(lines):
		if line.startswith('aws_'):
			x = len('./DevOps-AWS.pem')
			line = line[:-x-1] + '/home/ubuntu/DevOps-AWS.pem\n'
		output.write(line)


print '\n'.join(IPs)

with open("haproxy_origin.cfg", 'r') as input:
    # Read non-empty lines from input file
    # lines = [line for line in input if line.strip()]
    lines = [line for line in input]

with open("haproxy.cfg", "w") as output:
    for i in range(len(lines)):
    	output.write(lines[i])
    	if lines[i].startswith("        redirect location"):
    		k = i
    		break

    output.write("\n")
    for i in range(len(IPs)):
    	output.write("        server Server0" + str(i + 1) + " " + str(IPs[i]) + ":8080 check\n")

    for j in range(k + 1, len(lines)):
    	output.write(lines[j])

print 'slaves IP got added to haproxy.cfg'







print 'add IP of Master Node to GitHub Webhook'


auth_id = 'dchen20'
auth_token = 'a18a4d8aec6feee61064c5d5575d9a8625542876'
data={
      "name": "web",
      "active": True,
      "events": [
        "push",
        "pull_request"
      ],
      "config": {
        "url": "http://" + master_IP + ":6060/github-webhook/",
        "content_type": "json"
      }
    }
data = json.dumps(data)

# LIST hooks to get the ID for each hook. ID could be used to delete the hook afterwards.    Successful return should be Response 200 OK.
# r0 = requests.get("https://github.ncsu.edu/api/v3/repos/dchen20/iTrust-v23/hooks", auth=(auth_id, auth_token))

# CREATE a hook. Successful return should be Response 201 Created.
r1 = requests.post("https://github.ncsu.edu/api/v3/repos/dchen20/iTrust-v23/hooks", data=data, auth=(auth_id, auth_token))

# DELETE a hook by ID. Successful return should be Response 204 No Content.
# r1 = requests.delete("https://github.ncsu.edu/api/v3/repos/dchen20/iTrust-v23/hooks/1021", data=data, auth=(auth_id, auth_token))

# print r1.headers
# print '\n---\n'
# print r1.content




# url = 'https://github.ncsu.edu/api/v3/repos/dchen20/iTrust-v23/stats/contributors'
# r2 = requests.get(url, auth=(auth_id, auth_token))
# print r1

print 'webhook added!'
