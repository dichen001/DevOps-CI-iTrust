#!/bin/bash
echo $"--- Creating master node ---"
node AWS.js
for i in 1 2 3 4 5
do
	echo ""
   	echo $"--- Creating $i slave node ---"
   	node aws_slave.js
done
