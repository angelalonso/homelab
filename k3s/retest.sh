#!/usr/bin/env bash

for i in ./apps/cns_fe/01_deployment.yaml ./apps/cns_be/01_deployment.yaml .apps/cns_resources/nfs-client-db-init.yaml ./system/nfs-client.yaml ./system/nfs-server.yaml
do
  echo "### deleting $i"
  sudo k3s kubectl delete -f $i
done

sleep 10

for i in ./system/nfs-server.yaml ./system/nfs-client.yaml ./apps/cns_resources/nfs-client-db-init.yaml ./apps/cns_fe/01_deployment.yaml ./apps/cns_be/01_deployment.yaml
do
  echo "### applying $i"
  sudo k3s kubectl apply -f $i
done
