# NetDevOps Testing Pipeline Instructions
To run the testing pipeline, three components need to be set up and running. 
 1. Jenkins build server VM
 2. GNS3 server VM
 3. Local area network configured as a 192.168.1.0/24 (can be done in VMware)

The two VMs can be found in the NetDevOps zip file and are under NetDevOps/VM/(Jenkins or GNS3). 

The network is already setup to have the first VMware adaptor as NAT with the second as bridged with a 192.168.1.* address.

The password for both of these VM's, the Jenkins webpage and GNS3 server is:
* Username: amarriott
* Password: Movingonup2020

##### GNS3
To access the GNS3, you need the GNS3 client; this can be downloaded from https://www.gns3.com/software/download.

Once installed, you need to set the remote central server as:
	Host: 192.168.1.129
	Port: 3080 TCP
	Auth: (username above)
This connects you to the GNS3 server and allows you to interface with the simulated physical network.

##### Jenkins
To access the Jenkins, you can access it's the webpage at 192.168.1.130:8080, this requires the same login as above. 

Once accessed, you can navigate to either the CloudBaseTest or LanBaseTest jobs which runs the build script to test the chosen network. 

Everything has been configured on the Jenkins server, so additional configuration should not be necessary. 

If a new job needs to be created, ensure that the GitHub project is linked, the address is https://github.com/AlexMarriott/NetDevOps/.

The source code management tab is configured to git, with the repository URL configured as well: https://github.com/AlexMarriott/NetDevOps/ with the necessary credentials.

The final step is to populate the execute shell command with the following:

```
#!/bin/bash
python3 -m venv venv 
source venv/bin/actative
pip3 install -r requirements.txt
python3 build.py *Network type parameter, example: lan*
```

##### How To Run The Physical Network Pipeline:
To run the physical network test pipeline, you need to ensure both the Jenkins server and the GNS3 are online and running. The Jenkins serve already has the necessary routes configured to connect into the GNS3 simulated network. 

By selecting the LanBaseTest and clicking build, it executes running the job, select view console to see the output from the build job. 

##### How To Run The Cloud Network Pipeline:
To run the physical network test pipeline, you need to ensure the Jenkins server is online and running. The Jenkins serve already has the necessary routes configured to connect into the GNS3 simulated network. 

By selecting the LanBaseTest and clicking build, it executes running the job, select view console to see the output from the build job.

 ##### Passwords
 GNS3/Jenkins: amarriott:Movingonup2020
 Github Repo: https://github.com/AlexMarriott/NetDevOps
 Github Login (Throw away account): pinkconsole362@gmail.com:cJ*q=8=Ke@H=DT32p&Nd8=N8
 