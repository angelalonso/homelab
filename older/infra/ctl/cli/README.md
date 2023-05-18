# Command Line Interface to APIs

## What it does
Send calls to an API of choice from command line  

## How it works
- Define your API endpoint at .env (see env.template)  
- Define your API verbs at verbs.yaml (see verbs.yaml.template)  
- Define your API objects at objects.yaml (see objects.yaml.template)  
- Run the call as:  
pipenv run python3 cli.py <verb> <object> <parameters>  
  
E.g.:  
```pipenv run python3 cli.py get host name=myhost```  
```pipenv run python3 cli.py add host host_definition.yaml```  

