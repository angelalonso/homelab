# Home Lab CI/CD

This folder includes anything required to automatically get code deployed unto the cluster

## Installing Docker to build Images

- curl -sSL https://get.docker.com | sh
- sudo vi /etc/apt/preferences.d/docker-ce
Package: docker-ce
Pin: version 18.06.*
Pin-Priority: 1000
- sudo apt-get update
- sudo apt-get install docker-ce

## Getting the git2image program to work
sudo apt-get remove python-pip python3-pip
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
/usr/local/bin/pip3 install pytest -U



### Installing docker-compose

sudo apt-get install build-essential libssl-dev libffi-dev python-dev python-pip
pip install -U docker-compose

