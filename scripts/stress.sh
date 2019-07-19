#!/usr/bin/env bash

URL="https://homelab.fonseca.de.com/"

MS=1000
function timer
{
while [[ 0 -ne $MS ]]; do
    curl $URL
    sleep 0.01
    MS=$[$MS-10]
done
}
timer
