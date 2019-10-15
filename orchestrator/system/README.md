# Tools to control the cluster

## check_swarm.sh

Checks all nodes and removes/rejoins any node that might be failing.  

### Installation
Add the following to your crontab: 
```*/10 * * * * <INSTALLDIR>/orchestrator/system/check_swarm.sh <SSHUSER> <SSHPORT> <PATHTOSSHKEY> > <INSTALLDIR>/orchestrator/system/lastrun.log 2>&1```

, where  
<INSTALLDIR> is the full path to where you installed the homelab repo  
<SSHUSER> is the user to SSH into the nodes  
<SSHPORT> is the port to SSH into the nodes  
<PATHTOSSHKEY> is the full path to the private key for the SSHUSER  
