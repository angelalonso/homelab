#!/usr/bin/env bash
#set -x

USER=$1
PORT=$2
SSHKEY=$3

MASTERIP="192.168.0.15"
NODES="lisboa praha dublin"
#NODES="dublin"
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
    echo checking $node
    STATUS=$(docker node ls | grep $node | awk '{print $3 $4}')
    if [[ $STATUS != "ReadyActive" ]]; then
      echo "node $node leaving the swarm..."
      ssh -i $SSHKEY -o "StrictHostKeyChecking no" $USER@$node -p $PORT "docker swarm leave"
      sleep 5
      echo "Removing node $node from the swarm..."
      docker node rm $node
      sleep 5
      echo "Rejoining node $node to the swarm..."
      ssh -i $SSHKEY -o "StrictHostKeyChecking no" $USER@$node -p $PORT "$JOINCMD"
    else
      echo $node is $STATUS
    fi
  done
}
date "+%Y%m%d-%T"
check_master_ip
check_nodes
