# Welcome to my [Home Lab](https://angelalonso.github.io/homelab/)
In this repository you will find all the bits (that I can put online) needed to put my home cluster(s) together and keep them alive.
[test](https://angelalonso.github.io/homelab/Test)
# TL;DR
## Steps (roughly)
### Get the components
Nothing to add, this changes from day to day, maybe check [this](https://blog.alexellis.io/test-drive-k3s-on-raspberry-pi/) out...

### Install the OS, make it safe
TBD, check [/os/README.md](https://github.com/angelalonso/homelab/blob/master/os/README.md) while I update it.

### Install the tools
- Clone this repo  
```git clone https://github.com/angelalonso/homelab```

### ... (TBD)

## Phase 2
- Desired Architecture:

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


### Tools 
#### Must have
- Logging
- IP/resolv management (recovery from all systems rebooted and assigned new IPs)
#### Wish list
- Monitoring
- Load testing
- CICD


### Proxy/Bastion/Bouncer
#### Must have
- Proxy for the Web cluster
#### Wish list
- Authentication/Authorisation for the Web cluster


### IOT cluster
#### Must have
- Protected from the outside
- Single endpoint for the IoT stuff to connect to
- All applications running there must be stored on different, external repositories
- Scripts to build images, helm charts... should either be template-generators, or included on the application repos themselves.
#### Wish list
- Fork and further develop Docker Swarm (rename to HomeSwarm? IoTernetes?)
- Authentication/Authorisation for itself


### Web cluster
#### Must have
- K3s or some lightweight K8s installation
- All applications running there must be stored on different, external repositories
- Scripts to build images, helm charts... should either be template-generators, or included on the application repos themselves.
#### Wish list
TBD






## Phase 1, May-Dec 2019 - completed (good enough)
### Goal(s)
Learn how a cluster would work with the law of minimum investment.  
  
So far ~120€ :/

