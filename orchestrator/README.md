# Home Lab Orchestrator

This folder includes anything required to install the Orchestration layer on the cluster nodes.

## Docker Swarm

- curl -sSL https://get.docker.com | sh
- sudo vi /etc/apt/preferences.d/docker-ce
Package: docker-ce
Pin: version 18.06.*
Pin-Priority: 1000
- sudo apt-get update
- sudo apt-get install docker-ce
- sudo init 6

### Docker Swarm MANAGER
- docker swarm init --advertise-addr <manager-IP>

### Docker Swarm WORKER
- Paste the output command from the manager (previous step)

### Deploy or update your stacks
docker stack deploy --compose-file stacks/frontend_poll-compose.yml frontend

## HOWTOs

### Install Docker compose
sudo apt-get install python-pip
pip install -U docker-compose

### Install Docker machine
- get to https://github.com/docker/machine/releases to check latest release (here v0.16.1)
wget https://github.com/docker/machine/releases/download/v0.16.1/docker-machine-Linux-armhf
sudo install docker-machine-Linux-armhf /usr/local/bin/docker-machine

### create a services network
docker network create \
--driver overlay \
--subnet 10.10.1.0/24 \
--opt encrypted \
services

### deploy a stack
on docker-compose.yml:

services:
  frontend:
    image: angelalonso/frontend:v0.04
    ports:
      - "80:80"
networks:
  default:
    external:
      name: services


docker stack deploy --compose-file docker-compose.yml stackdemo
- NOTE: on a raspi1 it might take up to 10 minutes to have the container up and running (gets stuck on Preparing)

### Troubleshooting docker swarm
$ docker service ls
$ docker service ps <service>
$ docker service inspect <service>
$ docker inspect <task>
$ docker inspect <container>
$ docker logs <container>

https://success.docker.com/article/swarm-troubleshooting-methodology
