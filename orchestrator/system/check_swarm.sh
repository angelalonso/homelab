#!/usr/bin/env bash

MASTERIP="192.168.0.15"
NODES="lisboa praha dublin"
DB_NODE="dublin"

function check_master_ip {
  IP_OK=$(ifconfig | grep $MASTERIP)
  if [[ $IP_OK == "" ]]; then
    echo "wrong IP"
  fi
}

function check_nodes {
  JOINCMD=$(docker swarm join-token worker | grep join)
  for node in $NODES; do 
    echo $node
    STATUS=$(docker node ls | grep $node | awk '{print $3 $4}')
    if [[ $STATUS != "ReadyxActive" ]]; then
      echo "Leaving the swarm..."
      ssh aafmin@$node -p 21012 "docker swarm leave"
      sleep 5
      echo "Removing node $node"
      docker node rm $node
      echo "Node $node is now joining the swarm"
      ssh aafmin@$node -p 21012 "$JOINCMD"
    fi
    echo $STATUS
  done
}

check_master_ip
check_nodes
