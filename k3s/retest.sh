#!/usr/bin/env bash

k3 delete -f ./apps/cns_fe/01_deployment.yaml
k3 delete -f ./apps/cns_be/01_deployment.yaml
k3 delete -f ./system/nfs-client.yaml
k3 delete -f ./system/nfs-server.yaml

sleep 10

k3 apply -f ./system/nfs-server.yaml
k3 apply -f ./system/nfs-client.yaml
k3 apply -f ./apps/cns_fe/01_deployment.yaml
k3 apply -f ./apps/cns_be/01_deployment.yaml
