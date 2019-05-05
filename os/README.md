# Home Lab OS

This folder includes anything required to install the base OS on the cluster nodes.

## Steps to recreate the base image

- Download the image  
- Burn it to the MicroSD
- touch $BOOTDIR/ssh
- sudo apt-get update && sudo apt-get upgrade && sudo apt-get install vim
- echo $HOSTNAME | sudo tee /etc/hostname


## Known Issues

### Locales
#### Error:
apt-listchanges: Can't set locale; make sure $LC_* and $LANG are correct!
perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
	LANGUAGE = (unset),
	LC_ALL = (unset),
	LC_TIME = "de_DE.UTF-8",
	LC_MONETARY = "de_DE.UTF-8",
	LC_CTYPE = "en_US.UTF-8",
	LC_ADDRESS = "de_DE.UTF-8",
	LC_TELEPHONE = "de_DE.UTF-8",
	LC_NAME = "de_DE.UTF-8",
	LC_MEASUREMENT = "de_DE.UTF-8",
	LC_IDENTIFICATION = "de_DE.UTF-8",
	LC_NUMERIC = "de_DE.UTF-8",
	LC_PAPER = "de_DE.UTF-8",
	LANG = "en_US.UTF-8"
    are supported and installed on your system.


