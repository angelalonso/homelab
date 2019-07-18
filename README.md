# Welcome to my Home Lab

This is a repository meant to keep track of all the bits needed to make it work.

## Goal

Learn how a cluster would work with the law of minimum investment.  
  
So far ~120€ :/

## Rough instructions

- Buy all the parts, or get them for free.
- Connect the pieces together.
- Burn the images, modify them accordingly to run a configuration script at boot time.
- plug them in the machines, and feed the machines with power!
...To be continued

## What's with all the directories in this repo?

Ehm, these are "tools" I test. As of June 2019, they contain:  
### application

Several applications that might or might not be related to one another

### cicd

A set of scripts that automate the process between making changes on Github and getting the corresponding dockerhub image.

### logs

Instructions on how to get centralized logging working

### monitoring

So far it contains nothing, but it's meant to store things like Grafana Dashboards

### orchestrator

Orchestrating-related definitions. So far it contains only docker-compose-related files

### os

So far empty, but one day this should help automate the installation of a new node on the cluster

### scripts

Scripts that don't belong in any of the other folders

### security

So far I just keep here some notes on how I secure my nodes
