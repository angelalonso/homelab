# K3s
 based on https://blog.alexellis.io/test-drive-k3s-on-raspberry-pi/

raspi-config
> advanced options > Memory Split
Set the GPU memory split to 16mb 
exit and reboot

We need to enable container features in the kernel
vim /boot/cmdline.txt # and add the following to the end of the line:
``` cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory```
reboot
sudo init 6

## Master
bootstrap cluster
curl -sfL https://get.k3s.io | sh -
sudo systemctl status k3s

Grab the join key from this node with:
$ sudo cat /var/lib/rancher/k3s/server/node-token

open access to port 6443
sudo ufw allow from 192.168.0.1/24 to any port 6443

## Node
export K3S_URL="https://<hostname of master>:6443"
export K3S_TOKEN="The Join Key you got from master"
curl -sfL https://get.k3s.io | sh -
sudo k3s agent --server ${K3S_URL} --token ${K3S_TOKEN}


