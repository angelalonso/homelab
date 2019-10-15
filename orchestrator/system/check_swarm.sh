#!/usr/bin/env bash
#set -x
USER=$1
SSHKEY=$2
MASTERIP="192.168.0.15"
NODES="lisboa praha dublin"
#NODES="lisboa"
DB_NODE="dublin"

function check_master_ip {
  IP_OK=$(/sbin/ifconfig | grep $MASTERIP)
  if [[ $"IP_OK" == "" ]]; then
    echo "wrong IP"
  fi
}

function check_nodes {
  JOINCMD=$(docker swarm join-token worker | grep join)
  for node in $NODES; do 
    #echo $node
    STATUS=$(docker node ls | grep $node | awk '{print $3 $4}')
    if [[ $"STATUS" != "ReadyActive" ]]; then
      echo "Leaving the swarm..."

      ssh -i $SSHKEY -o "StrictHostKeyChecking no" $USER@$node -p 21012 "hostname"
      echo "ssh exit: "$?
      ssh -i $SSHKEY -o "StrictHostKeyChecking no" $USER@$node -p 21012 "docker swarm leave"
      echo "ssh exit: "$?
      sleep 5
      docker node rm $node
      sleep 5
      ssh -i $SSHKEY -o "StrictHostKeyChecking no" $USER@$node -p 21012 "$JOINCMD"
    fi
    echo $STATUS
  done
}
#date "+%Y%m%d-%T"
check_master_ip
check_nodes
