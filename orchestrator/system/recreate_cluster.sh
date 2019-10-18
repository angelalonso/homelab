#!/usr/bin/env bash
#set -x

function get_recreate_vars {
  MASTER=$(/bin/hostname)
  NEWMASTERIP=$(/sbin/ifconfig eth0 | grep "inet " | awk '{print $2}'"

}

function test_recreate_vars {
  echo "- Testing vars for cluster are correct..."
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

function get_etchosts {
  echo "- Getting current IPs for master and all nodes"
  echo "master name is $MASTER and IP is $NEWMASTERIP"

}

function recreate_cluster {
  get_recreate_vars
  test_recreate_vars
  get_etchosts
}

