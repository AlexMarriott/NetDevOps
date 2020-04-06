# int fast 0/0 ip address: 192.168.0.2/24

in fastEthernet 0/0.10
encapsulation dot1Q 10
ip address 10.16.17.2 255.255.255.0
no shut
hostname R2
service password-encryption
line vty 0 4
login local
password secret cisco

aaa new-model
aaa authentication login default local enable
username user1 password cisco
enable password cisco
