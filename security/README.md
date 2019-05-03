# Home Lab Security

This folder includes anything needed to secure our Cluster.

## Installing and configuring Firewall

### UFW

sudo apt-get update && sudo apt-get install ufw

sudo vim /etc/default/ufw
```
IPV6=yes
```

sudo ufw default deny incoming

sudo ufw default allow outgoing

sudo ufw allow ${SSH_PORT}

