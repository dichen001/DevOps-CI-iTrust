// Load the AWS SDK, FileSystem from Node.js
var AWS = require('aws-sdk');
var fs = require('fs');
var sleep = require('sleep');
var secretKey = process.env.secretKey

AWS.config.update({
	accessKeyId: "AKIAJFCKXV4UZRJSYGXQ",
    secretAccessKey: secretKey,
    region: "us-west-2"
})

var ec2 = new AWS.EC2();

var params = {
  ImageId: 'ami-30e65350', // Ubuntu Server 16.04 LTS (HVM), SSD Volume Type
  InstanceType: 't2.small', //t2.micro is free tier
  KeyName: 'DevOps-AWS',   // Use existed keypair
  MinCount: 1, 
  MaxCount: 1
};

// Create the instance
ec2.runInstances(params, function(err, data) {
  if (err) { 
  	console.log("Could not create instance", err); return;
  }

  var instanceId = data.Instances[0].InstanceId;
  console.log("Created instance", instanceId);
  
  // Add tags to the instance
  params = {Resources: [instanceId], 
  			Tags: [{Key: 'Name', 
  					Value: 'M4-Master'}]
			};
  ec2.createTags(params, function(err) {
    console.log("Tagging instance", err ? "failure" : "success");
  });

  console.log("Wait 15 seconds before retrieving IP address...");
  sleep.sleep(15);

  // Wait for instance running and fetch public ip address
  var params = { InstanceIds: [instanceId] };
  ec2.waitFor('instanceExists', params, function(err, data) {
    if (err) console.log(err, err.stack);
    else {
      var ipAddress = data.Reservations[0].Instances[0].PublicIpAddress;
      //console.log("\nInstance info:");
      console.log("Public IP:", ipAddress);

      // Concatenate Inventory record
      var s1 = "[Master]\naws_master_server ansible_host=";
      var s2 = " ansible_user=ubuntu ansible_ssh_private_key_file=./DevOps-AWS.pem\n\n[Slaves]\n";
      var record = s1.concat(ipAddress, s2);
      // Create Inventory file
      fs.writeFile("Inventory", record, function(err) {
          if(err) {
              return console.log(err);
          }
          console.log("Inventory is created successfully!");
      });
    }    
  });
});
