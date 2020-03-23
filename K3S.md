# K3s
 based on https://blog.alexellis.io/test-drive-k3s-on-raspberry-pi/

## Raspberry preparations
### Memory Split -> Done by ansible
raspi-config
> advanced options > Memory Split
Set the GPU memory split to 16mb 

### Cgroup Configs -> Done by ansible
We also need to enable container features in the kernel
vim /boot/cmdline.txt # and add the following to the end of the line:
``` cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory```
reboot  
sudo init 6  
  
## Master
bootstrap cluster
export INSTALL_K3S_SKIP_START=true && export INSTALL_K3S_VERSION='v1.0.1' && curl -sfL https://get.k3s.io | sh -s -
sudo systemctl status k3s
sudo systemctl start k3s

Grab the join key from this node with:
$ sudo cat /var/lib/rancher/k3s/server/node-token

open access to any port within the cluster
sudo ufw allow from 192.168.0.1/24

## Node
export K3S_URL="https://<hostname of master>:6443"
export K3S_TOKEN="The Join Key you got from master"
export INSTALL_K3S_VERSION='v1.0.1' && curl -sfL https://get.k3s.io | sh -
sudo k3s agent --server ${K3S_URL} --token ${K3S_TOKEN}

### Tag nodes
- Node where you mount the USB for your NFS server
k3 label nodes <your-node-name> nfs_usb=true

## Reverse Proxy
If you are using some kind of nginx proxy before your cluster, remembe you need to pass headers:
```
upstream frontend {
  server master_1;
#  server master_2;
}
server {
  listen       80;
  listen       [::]:80;

  proxy_set_header Host            $host;
  proxy_set_header X-Forwarded-For $remote_addr;

  location / {
    proxy_pass  http://frontend;
  }
}
```

## Q&A
- Remove k3s completely
``` /usr/local/bin/k3s-uninstall.sh```
- Check installation
``` k3s check-config ```

## KNOWN ISSUES
- After running k3s my machine collapses and I have to reboot
 - Check you modified cmdline.txt as described above
 - There seems to be trouble when running with 
 ``` INSTALL_K3S_EXEC='server --no-deploy traefik --cluster-cidr=192.168.0.0/17 --service-cidr=192.168.128.0/17' sh -s - ```
- After first install I had to recreate local-path-provisioner and metrics-server because coredns was not alive yet
 - Check you opened ports
 - Had also to use legacy-iptables
``` sudo update-alternatives --set iptables /usr/sbin/iptables-legacy > /dev/null
sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy > /dev/null ```
- msg="failed to get CA certs at https://127.0.0.1:39051/cacerts ... at the agent
 - edit /etc/systemd/system/k3s-agent.service.env
 - Use Ip on K3S_URL instead of hostname



## To be documented
### NFS
https://medium.com/@aallan/adding-an-external-disk-to-a-raspberry-pi-and-sharing-it-over-the-network-5b321efce86a

format a USB drive as FAT32
plug it
mount it
check it's there
 lsblk
format it
 sudo mkfs.vfat /dev/sda1 -n USB
mount it
 sudo mkdir /mnt/usb
 sudo chown -R user:user /mnt/usb
 sudo mount /dev/sda1 /mnt/usb -o uid=user,gid=user
do it permanent
 sudo vim /etc/fstab
   /dev/sda1 /mnt/usb auto defaults,user 0 1

apply -f nfs*

### Dashboard
k3 apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta8/aio/deploy/recommended.yaml
k3 proxy

how to access from outside?

## test https://github.com/rancher/k3s/issues/1442
/usr/local/bin/k3s-killall.sh
/usr/local/bin/k3s-uninstall.sh
sudo find / -name "k3s"
curl -sfL https://get.k3s.io | K3S_TOKEN=SECRET INSTALL_K3S_exec="server --cluster-init --docker --tls-san seoul -v 5 --log /tmp/k3s.log " sh -s -
curl -sfL https://get.k3s.io | K3S_TOKEN=SECRET INSTALL_K3S_exec="server --cluster-init --docker --tls-san raspi4 -v 5 --log /tmp/k3s.log --bind-address 192.168.1.242" sh -s -
