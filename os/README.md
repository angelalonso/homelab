# Home Lab OS

This folder includes anything required to install the base OS on the cluster nodes.

## Steps to recreate the base image

- Download the image  
- Burn it to the MicroSD
- touch $BOOTDIR/ssh
- sudo apt-get update && sudo apt-get upgrade && sudo apt-get install vim
- echo $HOSTNAME | sudo tee /etc/hostname

