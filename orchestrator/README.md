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
- sudo docker swarm init --advertise-addr <manager-IP>

### Docker Swarm WORKER
- Paste the command from the master

### Install Docker compose
sudo apt-get install python-pip
pip install -U docker-compose

### Install Docker machine
- get to https://github.com/docker/machine/releases to check latest release (here v0.16.1)
wget https://github.com/docker/machine/releases/download/v0.16.1/docker-machine-Linux-armhf
sudo install docker-machine-Linux-armhf /usr/local/bin/docker-machine


services:
  frontend:
    image: angelalonso/frontend:v0.03
    ports:
      - "8000:8000"

### deploy a stack
docker stack deploy --compose-file docker-compose.yml stackdemo

