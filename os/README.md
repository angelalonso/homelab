# Home Lab OS

This folder includes anything required to install the base OS on the cluster nodes.

## Steps to recreate the base image

- Download the image  
- Burn it to the MicroSD
- touch $BOOTDIR/ssh
- sudo apt-get update && sudo apt-get upgrade && sudo apt-get install vim
- echo $HOSTNAME | sudo tee /etc/hostname

## Installing python3.7
### https://gist.github.com/SeppPenner/6a5a30ebc8f79936fa136c524417761d
sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz
tar xf Python-3.7.0.tar.xz
cd Python-3.7.0
./configure
make -j 4
sudo make altinstall
cd ..
sudo rm -r Python-3.7.0
rm Python-3.7.0.tar.xz
sudo apt-get --purge remove build-essential tk-dev -y
sudo apt-get --purge remove libncurses5-dev libncursesw5-dev libreadline6-dev -y
sudo apt-get --purge remove libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev -y
sudo apt-get --purge remove libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y
sudo apt-get autoremove -y
sudo apt-get clean

## Making sure we can control the LEDs from scripts/d8s
sudo chmod 666 /sys/class/leds/led0/trigger
sudo chmod 666 /sys/class/leds/led0/brightness
