#!/usr/bin/env bash

APPS="frontend backend"

uptodate() {
  echo up to date
  exit 0
}

build() {
  echo "-_- Checking if new build needed"
  for APP in ${APPS}; do
    echo "-_- Checking ${APP}..."
    git fetch origin master > /dev/null 2>&1
    DIFF=$(git diff origin/master -- ${APP}/VERSION)
    if [ "$DIFF" != "" ]; then
      echo "-_- There was a version change on ${APP}"
      PWD=$(pwd)
      cd ./${APP}
      git pull > /dev/null 2>&1
      VERSION=$(cat VERSION)
      echo "-_- New version for ${APP} is $VERSION"
      #docker build . -t <account>/<repo>:<version>
      #docker push <account>/<repo>:<version>
      cd $PWD
    else
      echo "-_- There was NO version change on ${APP}"
    fi

  done
}

[ $(git rev-parse HEAD) = $(git ls-remote $(git rev-parse --abbrev-ref @{u} | \
sed 's/\// /g') | cut -f1) ] \
&& uptodate \
|| build

