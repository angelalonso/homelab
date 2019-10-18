#!/usr/bin/env bash
#set -x

function get_vars {
  echo "- Loading vars..."
  SELFPATH="$( cd "$(dirname "$0")" ; pwd -P )"
  source $SELFPATH/.env
  echo "...loaded."
  echo "- Loading external functions..."
  source $SELFPATH/recreate_cluster
  echo "...loaded."
}

function test_vars {
  echo "- Testing vars are correct..."
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
  echo "... vars are correct."
}

function check_master_ip {
  echo "- Checking the Master IP didn't change..."
  IP_OK=$(/sbin/ifconfig | grep $MASTERIP)
  if [[ $IP_OK == "" ]]; then
    echo "...it changed!"
    recreate_cluster
  else
    echo "...it didn't change."
  fi
}

function correct_nodes {
  echo "- Checking that all nodes are OK..."
  JOINCMD=$(docker swarm join-token worker | grep join)
  for node in $NODES; do 
    echo checking $node
    STATUS=$(docker node ls | grep $node | awk '{print $3 $4}')
    if [[ $STATUS != "ReadyActive" ]]; then
      echo "...node $node is not OK!\n, forcing it to leave the swarm..."
      ssh -i $SSHKEY -o "StrictHostKeyChecking no" $USER@$node -p $PORT "docker swarm leave"
      sleep 5
      echo ", removing node $node from the swarm..."
      docker node rm $node
      sleep 5
      echo ", rejoining node $node to the swarm..."
      ssh -i $SSHKEY -o "StrictHostKeyChecking no" $USER@$node -p $PORT "$JOINCMD"
    else
      echo "...node $node is $STATUS."
    fi
  done
}

function correct_nodes_db {
  echo "- Checking that all DB nodes are labelled correctly..."
  for node in $NODES_DB; do
    TESTLABEL=$(docker node inspect $node | grep type)
    if [[ "$TESTLABEL" != '                "type": "db"' ]]; then
      echo "...node $node is not!\n, adding the db label to node $node"
      docker node update --label-add type=db $node
    else
      echo "...node $node is already labelled a db one."
    fi
  done
}
date "+%Y%m%d-%T"
get_vars
test_vars
check_master_ip
correct_nodes
correct_nodes_db
