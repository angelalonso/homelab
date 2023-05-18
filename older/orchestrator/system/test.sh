#!/usr/bin/env bash
#set -x

## THIS FILE IS USED TO TEST NEW FUNCTIONS

lockfile=/tmp/test.lock

function get_vars {
  echo "- Loading vars..."
  SELFPATH="$( cd "$(dirname "$0")" ; pwd -P )"
  source $SELFPATH/.env
  echo "...loaded."
  echo "- Loading external functions..."
  source $SELFPATH/recreate_cluster.sh
  echo "...loaded."
}

function test_grep {
  GREPS=$(echo cluster "$CLUSTER_BOXES" | sed 's/ /\\|/g')
  echo $GREPS
  grep $GREPS /etc/hosts

}

if ( set -o noclobber; echo "$$" > "$lockfile") 2> /dev/null;
then
  trap 'rm -f "$lockfile"; exit $?' INT TERM EXIT KILL
  get_vars
  recreate_cluster
  rm -f "$lockfile"
  trap - INT TERM EXIT
else
  echo "Failed to acquire lockfile: $lockfile."
  echo "Held by $(cat $lockfile)"
fi

