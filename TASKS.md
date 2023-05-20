# First setup

- used RaspiOS bullseye ARMHF
- configured SSH and user/passwd
- SSHed into the machine
sudo apt update && sudo apt upgrade -y
- change SSH config
- raspi-config to change hostname

# Ansible config

- copy over variables.enc.template to variables.enc
- choose values
make encrypt
make run



