# K3s
 based on https://blog.alexellis.io/test-drive-k3s-on-raspberry-pi/

raspi-config
> advanced options > Memory Split
Set the GPU memory split to 16mb 

We also need to enable container features in the kernel
vim /boot/cmdline.txt # and add the following to the end of the line:
``` cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory```
reboot
sudo init 6

## Master
bootstrap cluster
export INSTALL_K3S_VERSION='v1.0.1' && curl -sfL https://get.k3s.io | sh -
sudo systemctl status k3s

Grab the join key from this node with:
$ sudo cat /var/lib/rancher/k3s/server/node-token

open access to port 6443
sudo ufw allow from 192.168.0.1/24 to any port 6443

## Node
export K3S_URL="https://<hostname of master>:6443"
export K3S_TOKEN="The Join Key you got from master"
export INSTALL_K3S_VERSION='v1.0.1' && curl -sfL https://get.k3s.io | sh -
sudo k3s agent --server ${K3S_URL} --token ${K3S_TOKEN}

## Q&A
- Remove k3s completely
``` /usr/local/bin/k3s-uninstall.sh```
- Check installation
``` k3s check-config ```

## KNOWN ISSUES
- After running k3s my machine collapses and I have to reboot
 - Check you modified cmdline.txt as described above
- After first install I had to recreate local-path-provisioner and metrics-server because coredns was not alive yet
 - Had to reinstall with 
 ``` export INSTALL_K3S_VERSION='v1.0.1' && curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC='server --no-deploy traefik --cluster-cidr=192.168.0.0/17 --service-cidr=192.168.128.0/17' sh -s - ```
 - Had also to use legacy-iptables
``` sudo update-alternatives --set iptables /usr/sbin/iptables-legacy > /dev/null
sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy > /dev/null ```



