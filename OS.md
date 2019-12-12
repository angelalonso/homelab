# Installing and configuring a base OS for the machines

## Before we start...
Anything $VARIABLE expects you to substitute that for the value you want.  
You can easily run ```export VARIABLE=value``` before running it literally.  
  
## Get the image
- Download the latest version, lite, zipped from https://www.raspberrypi.org/downloads/raspbian/
- Unzip it to get the .img file:
$ unzip 20XX-yy-zz-raspbian-****-lite.zip

## Burn the image to the microSD
For this I use https://www.balena.io/etcher/

## Enable SSH to the bootloader and boot it
- Mount the partition called "boot"
- In ubuntu:  
$ touch /media/$USER/boot/ssh
- Unmount the MicroSD card
- Insert it to the raspberry pi
- Connect it to power and the network (use a cable, mate!)
- Find the IP  
$ nmap -sP 192.168.0.0/24

## SSH into it, give it a name
$ ssh pi@<IP> # password is raspberry, accept authenticity
- once in, change hostname to your liking  
$ echo $HOSTNAME | sudo tee /etc/hostname

## Add your own admin user, remove user pi
$ sudo useradd -s /bin/bash -m -d /home/$NEWUSER $NEWUSER
- Give that user a strong password  
$ sudo passwd $NEWUSER
- Add your SSH key to log in  
$ sudo mkdir -p /home/$NEWUSER/.ssh  
$ sudo vi /home/$NEWUSER/.ssh/authorized_keys # Here you should paste your public SSH key and save
- Add your user to the same groups as pi is in  
$ vigr
```
:%s/:pi/:pi,$NEWUSER/g
```
- Make your NEW USER owner of its own environment  
$ sudo chmod 600 /home/$NEWUSER/.ssh/authorized_keys  
$ sudo chown -R $NEWUSER:$NEWUSER /home/$NEWUSER 
- Log out, log in again
$ logout  
$ ssh -i <PATH TO YOUR SSH KEY> $NEWUSER@<IP>  
- Get rid of pi  
$ sudo deluser -remove-home pi  
  
## Update, upgrade, install the basics
$ sudo apt-get update  
$ sudo apt-get upgrade  
$ sudo apt-get install git vim  
  
## Strengthen SSH
$ sudo vi /etc/ssh/sshd_config   
```ChallengeResponseAuthentication no
PasswordAuthentication no  
UsePAM no  
PermitRootLogin no  
Port $NEWPORT  
```
$ sudo systemctl reload ssh  
- Install fail2ban  
[x]

## Installing and configuring Firewall
- Install and configure UFW  
$ sudo apt-get update && sudo apt-get install ufw  
- Add support for IPv6  
$ sudo vim /etc/default/ufw    
```
IPV6=yes  
```  
- Configure default config  
$ sudo ufw default deny incoming  
$ sudo ufw default allow outgoing  
$ sudo ufw allow ${SSH_PORT}  
$ sudo ufw enable  


