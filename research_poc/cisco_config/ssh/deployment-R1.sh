# int fast 0/0 ip address: 192.168.0.1/24
int GigabitEthernet0/0
no shut
int GigabitEthernet0/0.10
encapsulation dot1Q 10
ip address 10.16.17.2 255.255.255.0
no shut
no ip domain-lookup
hostname R1
aaa new-model
username  password 
ip domain-name ain.test
enable secret Cisco
ip ssh rsa keypair-name sshkey
crypto key generate rsa usage-keys label sshkey modulus 2048
line vty 0 4
transport input ssh
exit
username user priv 15 secret cisco
