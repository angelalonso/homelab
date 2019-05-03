# Home Lab Monitoring

This folder includes anything needed to monitor our Cluster.

## Installing node_exporter
curl -SL https://github.com/prometheus/node_exporter/releases/download/v0.17.0/node_exporter-0.17.0.linux-armv6.tar.gz > node_exporter.tar.gz

sudo tar -xvf node_exporter.tar.gz -C /usr/local/bin/ --strip-components=1

sudo vim /etc/systemd/system/nodeexporter.service
```
[Unit]
Description=NodeExporter

[Service]
TimeoutStartSec=0
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
```

sudo systemctl daemon-reload  && sudo systemctl enable nodeexporter  && sudo systemctl start nodeexporter

## Installing Influxdb

curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -

echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

sudo apt-get update
sudo apt-get install influxdb
sudo systemctl start influxdb

sudo ufw allow 8086

influx
```
CREATE DATABASE telegraf
CREATE USER telegraf WITH PASSWORD 'superpa$$word'
GRANT ALL ON telegraf TO telegraf
CREATE RETENTION POLICY thirty_days ON telegraf DURATION 30d REPLICATION 1 DEFAULT
```

## Installing Telegraf

(done for InfluxDB)
#curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
#echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
#sudo apt-get update

sudo apt-get install telegraf

sudo systemctl start telegraf

sudo mv /etc/telegraf/telegraf.conf /etc/telegraf/telegraf.conf.orig

sudo vim /etc/telegraf/telegraf.conf
```
[agent]
  hostname = "this_one"
  flush_interval = "15s"
  interval = "15s"

[[inputs.cpu]]

[[inputs.mem]]

[[inputs.system]]

[[inputs.disk]]
  mount_points = ["/"]

[[inputs.processes]]

[[inputs.net]]
  fieldpass = [ "bytes_*" ]

[[outputs.influxdb]]
  database = "telegraf"
  urls = [ "http://127.0.0.1:8086" ]
  username = "telegraf"
  password = "superpa$$word"
```
 
sudo ufw allow 8086

sudo systemctl restart telegraf

## Installing Grafana

wget https://dl.grafana.com/oss/release/grafana_6.1.6_armhf.deb

sudo dpkg -i grafana_6.1.6_armhf.deb

sudo apt-get install libfontconfig

sudo apt --fix-broken install # yeah, I know

sudo dpkg -i grafana_6.1.6_armhf.deb # yeah, again, I know…


sudo vim /etc/grafana/grafana.ini
```
http_addr = 127.0.0.1
domain = dev.grafana.test
enable_gzip = true
root_url = https://dev.grafana.test
```

sudo systemctl restart grafana-server
sudo systemctl enable grafana-server

openssl genrsa -des3 -out myCA.key 4096
openssl req -x509 -new -nodes -key myCA.key -sha256 -days 1825 -out myCA.pem
openssl genrsa -out dev.grafana.test.key 4096
openssl req -new -key dev.grafana.test.key -out dev.grafana.test.csr
vim dev.grafana.test.ext
```
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = dev.grafana.test
DNS.2 = grafana.test
```


openssl x509 -req -in dev.grafana.test.csr -CA myCA.pem -CAkey myCA.key -CAcreateserial -out dev.grafana.test.crt -days 1825 -sha256 -extfile dev.grafana.test.ext


sudo apt-get install nginx

sudo vim /etc/nginx/sites-available/default
```
server {
        listen 80;
        listen [::]:80;
        server_name dev.grafana.test;
        return 301 https://dev.grafana.test$request_uri;

        access_log  /dev/null;
        error_log /dev/null;
}
server {
        listen 443 ssl http2;
        listen [::]:443 ssl http2;
        server_name dev.grafana.test;

        access_log /var/log/nginx/grafana-access.log;
        error_log  /var/log/nginx/grafana-error.log;
        ssl_certificate /home/user/ssl/dev.grafana.test.crt;
        ssl_certificate_key /home/user/ssl/dev.grafana.test.key;

        location / {
                proxy_set_header Host $http_host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_pass http://127.0.0.1:3000;
        }
}
```

sudo ufw allow 443


