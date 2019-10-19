#!/usr/bin/env bash
#set -x

tmp_etchosts=/tmp/etchosts

function update_etchosts {
  if [ -s $tmp_etchosts ];then
    cp /etc/hosts /etc/hosts.bak
    cp $tmp_etchosts /etc/hosts
    rm $tmp_etchosts
  fi
}

update_etchosts
