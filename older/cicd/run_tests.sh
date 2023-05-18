#!/usr/bin/env bash
PWD=$(pwd)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
python3 -m pytest -s -v
RESULT=$?
cd $PWD
exit $RESULT

