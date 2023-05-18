# REMEMBER:
THIS PROGRAM IS NOWHERE NEAR PRODUCTION READY. 
THERE ARE MANY RISKS INVOLVED.
DO NOT SAY I DID NOT WARN YOU

# secrets.yaml
```
hosts:
  test01:

groups:
  phase1:
    hosts:
    - test01
```

## Logic
- If phase1 has something on the "hosts:" definition, a first phase is run.
- phase1 run means:
  - make init generates ONLY manifests for phase1
  - make plan runs only on manifests for phase1
  - make apply runs only on manifests for phase1
    - secrets.yaml is modified AFTER make apply has run successfully.
      - The user needs to be informed of this.
    - once this has happened, the user will be asked if a run of the other regular playbooks is desired.
      - This second run includes a make init of the rest, as well as a make plan that requires confirmation before appliying

##Known Issues
- If you recreate hosts under the same IP, you'll need to deal with "REMOTE HOST IDENTIFICATION HAS CHANGED" manually (change ansible configs)
