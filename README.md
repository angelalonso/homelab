# Welcome to my Home Lab
In this repository you will find all the bits (that I can put online) needed to put my home cluster(s) together and keep them alive.

# TL;DR
Things you might find interesting
- Python script that builds and pushes docker images when a new version is found: https://github.com/angelalonso/homelab/blob/master/cicd/git2image.py

## Phase 2
- Desired Architecture:
'''
                      +-------+
                      |Tools  |
                      |Server |
  +-----------+       +-------+       +-----------+
  |IoT cluster|          |||          |Web cluster|
  |           <----------+|+--------->+           |
  +-----------+           |           +-----------+
  |-----------|           |           |-----------|
  |-----------|           |           |-----------|
  |-----------|           |           |-----------|
  +-----------+           |           +-----------+
       ^                  |                  ^
       |                  |                  |
       |                  |                  |
       |              +---v----+             |
     Stuff            |Proxy   +-------------+
                      |Bastion |
                      |Bouncer |
   Home               +--------+
                          |
                          v
 -----------------------VPN-----------------------
                          ^
   Scary         +--------|--------+
   World         | External Server |
                 +-----------------+
'''


- Further develop the current Docker Swarm cluster into an IOT-controller cluster project
 - Docker Swarm will not be maintained anymore by docker soon, also the version of docker that works for armv6 is not the latest. Make this a LAN-only cluster installation.
- Use K3s for the Web cluster
- The Proxy/Bastion/Bouncer server (from now on PBB) will manage anything communications
 - This includes authentication/authorisation
- The Tools server will manage anything that should not run on the PBB or the clusters (CICD...).
- All applications running on both clusters should be stored on different, external repositories. This repo is from now on only for the System stuff!
 - This also means things like scripts to build images, helm charts... should either be template-generators, or included on the application repos themselves.







## Phase 1, May-Dec 2019 - completed (good enough)
### Goal(s)
Learn how a cluster would work with the law of minimum investment.  
  
So far ~120€ :/

