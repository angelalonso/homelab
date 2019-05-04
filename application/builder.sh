#!/usr/bin/env bash

APPS="frontend"

uptodate() {
  echo up to date
  exit 0
}

build() {
  echo new build needed
  for i in ${APPS}; do
    echo $i
  done
}

[ $(git rev-parse HEAD) = $(git ls-remote $(git rev-parse --abbrev-ref @{u} | \
sed 's/\// /g') | cut -f1) ] \
&& uptodate \
|| build

