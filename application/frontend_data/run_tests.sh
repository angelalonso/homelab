#!/usr/bin/env bash
PWD=$(pwd)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
go test -v -cover
RESULT=$?
cd $PWD
exit $RESULT

