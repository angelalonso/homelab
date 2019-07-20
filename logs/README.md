# Centralized logs
## At the centralized logging server
echo 'deb http://download.opensuse.org/repositories/home:/rgerhards/Raspbian_9.0/ /' | sudo tee /etc/apt/sources.list.d/home:rgerhards.list
wget -nv https://download.opensuse.org/repositories/home:rgerhards/Raspbian_9.0/Release.key -O Release.key
apt-key add - < Release.key
sudo apt-get update && sudo apt-get install rsyslog

sudo vim /etc/rsyslog.conf # and add/uncomment the following:
```
# provides TCP syslog reception
module(load="imtcp")
input(type="imtcp" port="514")

$template Incoming-logs,"/var/log/rsyslog/%HOSTNAME%.log" 
*.*  ?Incoming-logs
& ~
```

sudo systemctl restart rsyslog

sudo ufw allow 514

# At the client we want to get the logs from
echo 'deb http://download.opensuse.org/repositories/home:/rgerhards/Raspbian_9.0/ /' | sudo tee /etc/apt/sources.list.d/home:rgerhards.list
wget -nv https://download.opensuse.org/repositories/home:rgerhards/Raspbian_9.0/Release.key -O Release.key
sudo apt-key add - < Release.key
sudo apt-get update && sudo apt-get install rsyslog

sudo vim /etc/rsyslog.conf # comment everything below #### RULES #### and add the following:
```
$ModLoad imfile
$InputFileName /var/lib/docker/containers/*/*.log
$InputFileTag docker-logs
$InputFileStateFile stat-docker-logs
$InputFileFacility local3
$InputRunFileMonitor
#local3.* @@rsyslog_server_IP:514 # this produces duplicated logs, leaving it here for future reference

*.* @@rsyslog_server_IP:514

```
sudo systemctl restart rsyslog

sudo -i
crontab -e 
```
0 * * * * /bin/systemctl restart rsyslog # restart every hour. Useful to recover from connectivity loss
```

## How to read all logs simultaneously
./all_logs # or sudo find /var/log/rsyslog/ -type f \( -name "*.log" \) -exec sudo tail -f "$file" {} +

