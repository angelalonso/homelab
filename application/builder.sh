#!/usr/bin/env bash

APPS="frontend backend"

uptodate() {
  echo up to date
  exit 0
}

build() {
  echo new build needed
  for APP in ${APPS}; do
    echo ${APP}
    git fetch origin master
    DIFF=$(git diff origin/master -- ${APP}/VERSION)
    if [ "$DIFF" != "" ]; then
      PWD=$(pwd)
      cd ${APP}
      git pull
      VERSION=$(cat VERSION)
      echo $VERSION
      cd $PWD
    fi

  done
}

[ $(git rev-parse HEAD) = $(git ls-remote $(git rev-parse --abbrev-ref @{u} | \
sed 's/\// /g') | cut -f1) ] \
&& uptodate \
|| build

