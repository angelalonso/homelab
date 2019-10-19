# Tools to control the cluster

## Prerrequisites
- So far there is only a master
- The tools are run FROM the master
- There is a number of nodes, but also some extra boxes in the cluster (e.g.: for monitoring or proxying)
- All of the boxes have the same content on /etc/hosts
- All of the boxes have to have this repo checked out under $HOME
- All of the boxes need the following cronjob:
```*/1 * * * * cd $HOME/homelab && /usr/bin/git pull -q origin master > /tmp/homelab.gitpull.log  2>&1```
  

## check_swarm.sh

Checks all nodes and removes/rejoins any node that might be failing.  

### Installation
Copy .env.dist to .env and adapt the values of the variables.  
Add the following to root's crontab:  
```*/10 * * * * <INSTALLDIR>/orchestrator/system/check_swarm.sh > /tmp/homelab.check_swarm.log 2>&1```  
  
, where INSTALLDIR is the full path to where you installed the homelab repo.


## box_update.sh

Updates files on a regular basis. Those files are usually written from the scripts running at the master

### Installation

Making sure this repo is installed under <HOME>, add the following to root's crontab:

```*/1 * * * * /home/aafmin/homelab/orchestrator/system/box_update.sh > /home/aafmin/homelab/orchestrator/system/lastupdate.log 2>&1```
