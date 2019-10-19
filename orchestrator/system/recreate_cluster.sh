#!/usr/bin/env bash
#set -x

# ---- TODO 
#  several masters
#  basis etc/hosts, or maybe sed out the wrong ones

tmp_etchosts=/tmp/etc_hosts

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
  # Remove our boxes from the temporary etchosts
  GREPS=$(echo cluster "$CLUSTER_BOXES" | sed 's/ /\\|/g')
  grep -v $GREPS /etc/hosts > $tmp_etchosts

  echo "- Getting current IPs for all boxes in the cluster..."
  echo "# cluster" >> $tmp_etchosts
  for ip in $(seq -f "192.168.0.%g" 1 20); do
    IPOK=$(ping -c 1 $ip &> /dev/null 2>&1; echo $?)
    if [[ IPOK -eq 0 ]]; then
      NEWNODE=$(ssh -i $SSHKEY -o "StrictHostKeyChecking no" $USER@$ip -p $PORT "hostname" 2>&1)
      if [[ $CLUSTER_BOXES == *$NEWNODE* ]]; then
        echo $ip $NEWNODE >> $tmp_etchosts
      fi
    fi
    printf '.'
  done
  echo
  echo "-------------------"
  cat $tmp_etchosts
  echo "-------------------"
}

function set_etchosts {
  # compare both files without the cluster
  #  if same, backup original
  #  then move over
  echo "- Checking the new etchosts will be fine..."
  CLEAN_ORIGINAL=$(grep -v $GREPS /etc/hosts)
  CLEAN_NEW=$(grep -v $GREPS $tmp_etchosts)
  if [[ $CLEAN_ORIGINAL == $CLEAN_NEW ]]; then
    echo "...they are fine."
    echo "- Backing up the original one..."
    cp /etc/hosts /etc/hosts.bak
    if [ -s /etc/hosts.bak ]; then
      echo "...backup seems ready"
      echo "- Overwriting /etc/hosts..."
      cp $tmp_etchosts /etc/hosts
      echo "...done."
    else
      echo "...backup seems wrong, aborting!"
    fi
  else
    echo "...there is something wrong:"
    echo $CLEAN_ORIGINAL
    echo $CLEAN_NEW
  fi
}

function distribute_etchosts {
  CLUSTER_IPS=$(cat $tmp_etchosts | awk '{print $1}')
  for ip in $CLUSTER_IPS; do
    scp -P $PORT -i $SSHKEY -o "StrictHostKeyChecking no" /etc/hosts $USER@$ip:/tmp/etchosts
  done
}

function recreate_cluster {
  get_recreate_vars
  test_recreate_vars
  get_etchosts
  set_etchosts
}

