#!/usr/bin/env bash
PWD=$(pwd)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
go get -u github.com/gorilla/mux
go get -u github.com/lib/pq
go get -u github.com/romana/rlog
go get -u github.com/prometheus/client_golang/prometheus/promhttp
go test -v -cover
RESULT=$?
cd $PWD
exit $RESULT

