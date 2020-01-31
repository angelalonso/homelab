#!/usr/bin/env bash

k3s kubectl delete -f ./apps/cns_fe/01_deployment.yaml
k3s kubectl delete -f ./apps/cns_be/01_deployment.yaml
k3s kubectl delete -f ./system/nfs-client.yaml
k3s kubectl delete -f ./system/nfs-server.yaml

sleep 10

k3s kubectl apply -f ./system/nfs-server.yaml
k3s kubectl apply -f ./system/nfs-client.yaml
k3s kubectl apply -f ./apps/cns_fe/01_deployment.yaml
k3s kubectl apply -f ./apps/cns_be/01_deployment.yaml
