#!/usr/bin/env bash
sudo -s
apt update && apt upgrade -y && apt install ansible sshpass python3 python3-pip -y && ssh-keygen -b 2048 -t rsa -q -N '' -f sshkey 2>/dev/null <<< y >/dev/null

touch password.txt && echo "Movingonup2016" > password.txt

rm -rf /home/amarriott/.ssh/known_hosts
su amarriott

sshpass -p "Movingonup2016" ssh-copy-id -i /home/amarriott/.ssh/sshkey.pub amarriott@192.168.11.10
sshpass -p "Movingonup2016" ssh-copy-id -i /home/amarriott/.ssh/sshkey.pub amarriott@192.168.13.10

chmod 777 /home/amarriott/.ssh/sshkey.pub /home/amarriott/.ssh/sshkey && chown amarriott.amarriott /home/amarriott/.ssh/sshkey /home/amarriott/.ssh/sshkey.pub