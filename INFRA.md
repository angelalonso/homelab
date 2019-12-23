# Infrastructure as Code

With this tool we try to get as close to "hands-off" as possible on all of the following phases:  
- Securing the machines  
- Installing and configuring everything needed for stuckk to run  
- Making applications run (e.g.: docker swarm join) and keeping them up (e.g.: live checks and restarts)  

## Why do we need this tool?

Ansible (almost) can manage all three topics for us, but the first phase (securing machines) involves changing ssh access. From that moment on, ansible cannot connect to that host anymore.  

The solution was to run ansible in two sequential phases:  
- new_<group> phase: includes all changes that will invalidate our origin ssh access.
- <group> phase: includes all other changes needed.  
, where <group> is the group definition for the playbook we will run, e.g.: raspbian for all the tasks we run on a raspbian system to have it configured as we want, or dockernode for all the tasks we need to turn a machine into a docker swarm node.  

## Caveats
- Since we are using a wrapper on top of ansible, any group we define on our secrets.yaml will need a templates/playbook_<group>.yaml file for it to work.
- If there is a "new_<group>" group present, we cannot plan for the <group> itself, because dependencies defined on new_<group> will make the plan fail anyway.



## Ansible
- Install it on your tools host  
$ sudo apt-get update && sudo apt-get install ansible  
- Create your SSH key to access hosts  
$ ssh-keygen -t rsa -b 4096 -N '' -f ~/.ssh/ansible
- Copy it over to the admin's .ssh/authorized_keys

### TBD
- [x] Create python wrapper that generates hosts and playbooks from file that is not on git
  - [x] init:
    - [x] read secrets.yaml
    - [x] create hosts, manifests
  - [x] plan:
    - [x] run dry 
  - [x] apply:
    - [x]ansible-playbook
- [x] Create and document standard configuration/playbooks
 - Create sshkey, add to admin
 - Create ansible user, add sshkey
 - Remove sshkey from admin user
- [x] Use and document dedicated ssh keys for ansible

## Other systems that failed
- Ansible + Makefile for the secrets -> escaping strings on the makefile is a bit complex
- Saltstack 
  - too heavy to run master and minions
  - official installation does not work out of the box on raspbian
