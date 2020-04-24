#!/usr/bin/env bash

# A bash script for configuring and setting up the remote ansible node in auzre
# Alex Marriott - 24/4/2020

apt update && apt upgrade -y && apt install ansible sshpass python3 python3-pip -y

rm -rf /home/amarriott/.ssh/known_hosts

sudo -u amarriott ssh-keygen -b 2048 -t rsa -q -N '' -f /home/amarriott/.ssh/sshkey 2>/dev/null <<< y >/dev/null

sudo -u amarriott  sshpass -p "Movingonup2016" ssh-copy-id -i /home/amarriott/.ssh/sshkey.pub amarriott@192.168.11.10
sudo -u amarriott  sshpass -p "Movingonup2016" ssh-copy-id -i /home/amarriott/.ssh/sshkey.pub amarriott@192.168.13.10

sudo -u amarriott  chmod 744 /home/amarriott/.ssh/sshkey*  && sudo -u amarriott  chown amarriott.amarriott /home/amarriott/.ssh/sshkey*

sudo -u amarriott  ssh-agent bash
sudo -u amarriott  ssh-add ~/.ssh/sshkey