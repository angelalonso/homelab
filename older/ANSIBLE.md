# Ansible workflow

## Installation
You will need to run Ansible from the "tools" machine in your cluster.  
- Install it and some dependencies  
$ sudo apt-get update && sudo apt-get install ansible sshpass

# Configuration
- Hosts file:
$HOMELAB_DIR/infra/hosts
- Playbooks directory:
$HOMELAB_DIR/infra/manifests

## Project goals
- Avoid manual work when installing or modifying machines in the cluster
  - Define infrastructure as code
  - Have an init-> plan-> apply workflow, similar to terraform's

## Tasks
- [x] define new machine
  - [x] Burn new image from scratch and mount it
  - [x] Get it ready from the tools host, document steps out of OS.md and into here (leave it documented somewhere else as reference)
    - [x] Create aafmin user, with a given password
    - [x] Add Ansible key
    - [x] Add aafmin to same groups as pi
    - [x] Remove pi user
    - [x] update, upgrade, install vim, git, fail2ban, ufw
    - [x] Strengthen ssh
    - [x] configure fail2ban
    - [x] configure ufw
    - [x] check python3 is default
- [x] define new docker-swarm machine
  - [x] follow installation procedure

