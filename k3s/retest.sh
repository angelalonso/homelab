#!/usr/bin/env bash

sudo k3s kubectl delete -f ./apps/cns_fe/01_deployment.yaml
sudo k3s kubectl delete -f ./apps/cns_be/01_deployment.yaml
sudo k3s kubectl delete -f ./system/nfs-client.yaml
sudo k3s kubectl delete -f ./system/nfs-server.yaml

sleep 10

sudo k3s kubectl apply -f ./system/nfs-server.yaml
sudo k3s kubectl apply -f ./system/nfs-client.yaml
sudo k3s kubectl apply -f ./apps/cns_fe/01_deployment.yaml
sudo k3s kubectl apply -f ./apps/cns_be/01_deployment.yaml
