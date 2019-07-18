# Centralized logs
## At the centralized logging server
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
sudo apt-get update && sudo apt-get install rsyslog

sudo vim /etc/rsyslog.conf # comment everything below #### RULES #### and add the following:
```
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

