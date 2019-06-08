# Home Lab CI/CD

This folder includes anything required to automatically get code deployed unto the cluster

## git2image

This program looks for changes in a file named VERSION inside a list of folders.
If the version changes, it builds the related docker image and pushes it to docker hub

This is supposed to run as a cronjob, every 5 minutes.

### Getting the git2image program to work
sudo apt-get remove python-pip python3-pip
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
/usr/local/bin/pip3 install -r requirements.txt --user
sudo gpasswd -a $USER docker

### Configuring the cronjob
TBD

## Installing Docker to build Images

- curl -sSL https://get.docker.com | sh
- sudo vi /etc/apt/preferences.d/docker-ce
Package: docker-ce
Pin: version 18.06.*
Pin-Priority: 1000
- sudo apt-get update
- sudo apt-get install docker-ce



### Installing docker-compose

sudo apt-get install build-essential libssl-dev libffi-dev python-dev python-pip
pip install -U docker-compose

