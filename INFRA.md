# Infrastructure as Code

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
