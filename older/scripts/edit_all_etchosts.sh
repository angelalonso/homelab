#!/usr/bin/env bash

HOSTS="tokyo seoul lisboa praha riga sidney beirut"
for i in $HOSTS 
do 
  echo "Editing /etc/hosts on "$i
  ssh -t -A -p 21012 aafmin@$i "sudo vim /etc/hosts" 
done
