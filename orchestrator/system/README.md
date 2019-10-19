# Tools to control the cluster

## Prerrequisites
- So far there is only a master
- The tools are run FROM the master
- There is a number of nodes, but also some extra boxes in the cluster (e.g.: for monitoring or proxying)
- All of the boxes have the same content on /etc/hosts

## check_swarm.sh

Checks all nodes and removes/rejoins any node that might be failing.  

### Installation
Copy .env.dist to .env and adapt the values of the variables.  
Add the following to root's crontab:  
```*/10 * * * * <INSTALLDIR>/orchestrator/system/check_swarm.sh > <INSTALLDIR>/orchestrator/system/lastrun.log 2>&1```  
  
, where INSTALLDIR is the full path to where you installed the homelab repo.
