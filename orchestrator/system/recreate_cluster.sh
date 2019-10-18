#!/usr/bin/env bash
#set -x

function get_vars {
  echo "- Loading vars..."
  SELFPATH="$( cd "$(dirname "$0")" ; pwd -P )"
  source $SELFPATH/.env
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

function get_etchosts {
  echo "- Getting current IPs for all nodes"
}

date "+%Y%m%d-%T"
get_vars
test_vars
get_etchosts

