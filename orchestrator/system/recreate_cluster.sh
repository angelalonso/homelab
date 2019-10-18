#!/usr/bin/env bash
#set -x

# ---- TODO 
#  several masters
#  lockfile
#  basis etc/hosts, or maybe sed out the wrong ones

function get_recreate_vars {
  MASTER=$(/bin/hostname)
  # TODO check MASTER_INTERFACE BEFORE RUNNING THIS
  NEWMASTERIP=$(/sbin/ifconfig $MASTER_INTERFACE | grep "inet " | awk '{print $2}')

}

function test_recreate_vars {
  echo "- Testing vars for cluster are correct..."
  if [[ -z $USER || \
    -z $PORT || \
    -z $SSHKEY || \
    -z $MASTERIP || \
    -z $MASTER_INTERFACE || \
    -z $CLUSTER_BOXES || \
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
  echo " - /etc/hosts:"
  echo "$NEWMASTERIP $MASTER"
  for ip in $(seq -f "192.168.0.%g" 1 20); do
    IPOK=$(ping -c 1 $ip &> /dev/null 2>&1; echo $?)
    if [[ IPOK -eq 0 ]]; then
      NEWNODE=$(ssh -i $SSHKEY -o "StrictHostKeyChecking no" $USER@$ip -p $PORT "hostname" 2>&1)
      if [[ $CLUSTER_BOXES == *$NEWNODE* ]]; then
        echo $ip $NEWNODE
      fi
    fi
  done
}

function recreate_cluster {
  get_recreate_vars
  test_recreate_vars
  get_etchosts
}

