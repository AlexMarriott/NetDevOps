vlan 10
int vlan 10
ip address 10.16.17.3 255.255.255.0
no shut
hostname SW1
no ip domain-lookup
aaa new-model
username  password 
ip domain-name ain.test
enable secret 
ip ssh rsa keypair-name sshkey
crypto key generate rsa usage-keys label sshkey modulus 768
line vty 0 4
transport input ssh
exit
username user priv 15 secret 

int gigabitEthernet 0/1
switchport mode trunk
switchport trunk allowed vlan all
exit

int gigabitEthernet 0/2
switchport mode trunk
switchport trunk allowed vlan all
exit

int fastEthernet 0/1
switchport mode access
switchport access vlan 10
