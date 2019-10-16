#!/usr/bin/env bash
#set -x

function get_vars {
  SELFPATH="$( cd "$(dirname "$0")" ; pwd -P )"
  source $SELFPATH/.env
}

function test_vars {
  if [[ -z $USER || \
    -z $PORT || \
    -z $SSHKEY || \
    -z $MASTERIP || \
    -z $NODES || \
    -z $NODES_DB ]] 
  then
    echo 'ERROR: one or more variables are undefined, Check/Create your .env file'
    exit 1
  fi
}

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
get_vars
test_vars
check_master_ip
check_nodes
