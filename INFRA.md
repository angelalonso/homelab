# Infrastructure as Code

## SaltStack
NOTE: this is not yet working! These are just temporary notes...

### Install on master
- make sure you are running on python3  
$ python --version # If not, check OS.md again  
- Install and run the salt master as a daemon  
$ curl -L https://bootstrap.saltstack.com -o install_salt.sh  
$ sudo sh install_salt.sh -P -M  
$ sudo salt-master -d  

### Install on each minion
#### Debian 9-based minions:
- make sure you are running on python3  
$ python --version # If not, check OS.md again  
- Install and run the salt master as a daemon  
$ wget -O - https://repo.saltstack.com/apt/debian/9/armhf/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -  
$ sudo vim /etc/apt/sources.list.d/saltstack.list  
```deb https://repo.saltstack.com/apt/debian/9/armhf/latest stretch main```
$ sudo apt-get update  
$ sudo apt-get install salt-minion python3-pip
$ sudo pip install futures salt
  
```
NOTE: this didn't work:
$ curl -L https://bootstrap.saltstack.com -o install_salt.sh  
$ sudo sh install_salt.sh -P  
```
