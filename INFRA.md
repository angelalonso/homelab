# Infrastructure as Code

Here we try to get as close to "hands-off" as possible on all of the following phases:  
- Securing the machines  
- Installing and configuring everything needed for stack to run  
- Making applications run (e.g.: docker swarm join) and keeping them up (e.g.: live checks and restarts)  

## Problems I am trying to solve
- Templates can be on version control, but passwords and some other stuff cannot. 
  - SOLUTION: templating  
- When Ansible must do changes to SSH config (also credentials), connection will stop working.  
  - SOLUTION: run in two phases, automatic creation of phase2 definitions from phase1's variables.  

## TL;DR
``` make create``` 
- Edit secrets.yaml
``` make init```
``` make plan```
``` make apply```

### Alright, I do want to read about the two phases...

This part of the documentation is meant for people wanting to modify the default config provided.

Use case: you just burnt Raspbian into an SSD, added the /boot/ssh file and want to make your Raspi secure before applying your ansible configs. 
From now on we assume the following example variables:
- your new machine will be called raspihost1  
- the playbook for that machine, where you define what you want to do, will be called raspisetup  
  
- Create your secrets from the template:  
``` make create ```
- Edit secrets.yaml according to these rules:
  - Under ```groups:```, add your playbook's name (raspisetup) and variables WITHOUT ```hosts:```
  - Under ```groups:```, ALSO add another one named 'phase1_raspisetup' with the following variables:  
  ```
    hosts:
    - phase1_raspihost1
    phase2_ansible_user:
      name: <future username you want to use>
      password: <future password for that username>
      ssh_key: </path/to/local/file/with/the/public.key>
      ssh_path: </path/to/.ssh/on/the/raspberry/server>
      ssh_port: <future ssh port you want to use on the raspberry server>
  ```
  - Under ```hosts:```, add the current raspberry definition, and name it 'phase1_raspihost1', such as:
  ```
hosts:
  phase1_raspihost1:
    ansible_ssh_port: 22
    ansible_user:
      name: pi
      password: raspberry
    ip: 192.168.0.4
  ```
- Under the templates folder:  
  - rename playbook_phase1_raspbian.yaml to playbook_phase1_raspisetup.yaml, and edit the file to have '- hosts: phase1_raspisetup'
  - rename playbook_raspbian.yaml to playbook_raspisetup.yaml, and edit the file to have '- hosts: raspisetup'
  - make sure any group you defined has its own playbook_ file

``` make init```
``` make plan```
``` make apply```

### What will happen in the background?
- asd.py is where the (not-so-)magic happens.
- asd.py create copies secrets_test.yaml to secrets.yaml, as a means to create an "empty" secrets file to modify 
- asd.py init creates the hosts needed for phase1, then separately those for phase2
- asd.py init creates the manifests based on templates and your secrets.yaml file  
- asd.py init creates any config files that are tailored to a specific group
- asd.py plan 



## Caveats
- Since we are using a wrapper on top of ansible, any group we define on our secrets.yaml will need a templates/playbook_<group>.yaml file for it to work.
- If there is a "new_<group>" group present, we cannot plan for the <group> itself, because dependencies defined on new_<group> will make the plan fail anyway.



## Requirements
You'll need ansible and some other stuff. Just run:
'''$ make init '''
- Install it 
$ sudo apt-get update && sudo apt-get install ansible  
- Create your SSH key to access hosts  
$ ssh-keygen -t rsa -b 4096 -N '' -f ~/.ssh/ansible
- Copy it over to the admin's .ssh/authorized_keys

### Plan
- [x] Create python wrapper that generates hosts and playbooks from file that is not on git
  - [x] init:
    - [ok] read secrets.yaml
    - [ok] create hosts, manifests
  - [ok] plan:
    - [ok] run dry 
  - [ok] apply:
    - [ok]ansible-playbook
- [ok] Create and document standard configuration/playbooks
- [x] Use and document dedicated ssh keys for ansible

## Other systems that failed
- Ansible + Makefile for the secrets -> escaping strings on the makefile is a bit complex
- Saltstack 
  - too heavy to run master and minions
  - official installation does not work out of the box on raspbian
