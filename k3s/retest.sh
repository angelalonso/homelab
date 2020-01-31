#!/usr/bin/env bash

for i in ./apps/cns_fe/01_deployment.yaml ./apps/cns_be/01_deployment.yaml ./system/nfs-client.yaml ./system/nfs-server.yaml
do
  echo "### deleting $i"
  sudo k3s kubectl delete -f $i
done

sleep 10

sudo k3s kubectl apply -f ./system/nfs-server.yaml
sudo k3s kubectl apply -f ./system/nfs-client.yaml
sudo k3s kubectl apply -f ./apps/cns_fe/01_deployment.yaml
sudo k3s kubectl apply -f ./apps/cns_be/01_deployment.yaml
