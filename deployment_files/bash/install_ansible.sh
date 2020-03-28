#!/usr/bin/env bash
#exec 3>&1 4>&2
#trap 'exec 2>&4 1>&3' 0 1 2 3
#exec 1>log.out 2>&1

#echo "$(date) : part 1 - start" >&3

apt update && apt upgrade -y && apt install ansible sshpass python3 python3-pip -y && ssh-keygen -b 2048 -t rsa -q -N '' -f ~/.ssh/sshkey 2>/dev/null <<< y >/dev/null

touch password.txt && echo "Movingonup2016" > password.txt

#sshpass -p "Movingonup2016" ssh-copy-id -i ~/.ssh/sshkey.pub amarriott@192.168.11.10
sshpass -f password.txt ssh-copy-id -i ~/.ssh/sshkey.pub amarriott@192.168.13.10

