# Tools to control the cluster

## check_swarm.sh

Checks all nodes and removes/rejoins any node that might be failing.  

### Installation
Copy .env.dist to .env and adapt the values of the variables.  
Add the following to your crontab:  
```*/10 * * * * <INSTALLDIR>/orchestrator/system/check_swarm.sh > <INSTALLDIR>/orchestrator/system/lastrun.log 2>&1```  
  
, where INSTALLDIR is the full path to where you installed the homelab repo.
