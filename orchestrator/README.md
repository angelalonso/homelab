# Home Lab Orchestrator

This folder includes anything required to install the Orchestration layer on the cluster nodes.

## Docker Swarm

### Up and running
- curl -sSL https://get.docker.com | sh
- sudo vi /etc/apt/preferences.d/docker-ce
Package: docker-ce
Pin: version 18.06.*
Pin-Priority: 1000
- sudo apt-get update
- sudo apt-get install docker-ce
- sudo init 6

#### Docker Swarm MANAGER
- docker swarm init --advertise-addr <manager-IP>

#### Docker Swarm WORKER
- Paste the output command from the manager (previous step)
- otherwise, run the following on the MANAGER to retrieve the token again:
  - docker swarm join-token worker

#### Make one of the workers get the DBs
docker node ls # to get the node's ID
docker node update --label-add type=db <NODE_ID>

#### Deploy or update your stacks
bash create_secrets.sh
docker network create --driver overlay --subnet 10.10.9.0/24 --attachable grid
docker stack deploy --compose-file stacks/frontend_poll-compose.yml frontend
docker stack deploy --compose-file stacks/backend-compose.yml backend
docker stack deploy --compose-file stacks/db-compose.yml db
docker stack deploy --compose-file stacks/frontend_data-compose.yml fe-data



### HOWTOs

#### Install Docker compose
sudo apt-get install python-pip
pip install -U docker-compose

#### Install Docker machine
- get to https://github.com/docker/machine/releases to check latest release (here v0.16.1)
wget https://github.com/docker/machine/releases/download/v0.16.1/docker-machine-Linux-armhf
sudo install docker-machine-Linux-armhf /usr/local/bin/docker-machine

#### create a services network
docker network create \
--driver overlay \
--subnet 10.10.1.0/24 \
--opt encrypted \
services

#### deploy a stack
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

#### Troubleshooting docker swarm
$ docker service ls
$ docker service ps <service>
$ docker service inspect <service>
$ docker inspect <task>
$ docker inspect <container>
$ docker logs <container>

https://success.docker.com/article/swarm-troubleshooting-methodology

#### remove a service completely
- look for the proper service name:  
docker service ls  
- delete it:  
docker service rm <name_you_found>
