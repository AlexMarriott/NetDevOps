vlan 10
int vlan 10
ip address 10.16.17.3 255.255.255.0
no shut
hostname SW1
service password-encryption
line vty 0 4
login local
password secret cisco

aaa new-model
aaa authentication login default local enable
username user1 password cisco
enable password cisco
