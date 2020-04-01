#!/usr/bin/env bash

function check_status_code(){
    if [ $? -ne $1 ]
    then
        echo $?
    fi
}



apt update && apt upgrade -y && apt install ansible sshpass python3 python3-pip -y && ssh-keygen -b 2048 -t rsa -q -N '' -f ~/.ssh/sshkey 2>/dev/null <<< y >/dev/null

touch password.txt && echo "Movingonup2016" > password.txt

rm -rf /root/.ssh/known_hosts

sshpass -f password.txt ssh-copy-id -i ~/.ssh/sshkey.pub amarriott@192.168.11.10
sshpass -f password.txt ssh-copy-id -i ~/.ssh/sshkey.pub amarriott@192.168.13.10
