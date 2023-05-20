
.PHONY: encrypt
encrypt: # encrypt the secrets file
	@ansible-vault encrypt variables.enc 

.PHONY: secrets
secrets: # decrypt to edit the secrets file
	@ansible-vault edit variables.enc 

.PHONY: runtest
runtest: # just run the TEST tasks
	@ansible-playbook ./playbooks/*.yml -e @variables.enc --ask-vault-pass --user labmin -i ./hosts --tags "test"

.PHONY: runfast
runfast: # just run the tasks that are not one-timers
	@ansible-playbook ./playbooks/*.yml -e @variables.enc --ask-vault-pass --user labmin -i ./hosts --tags "do_always"

.PHONY: run
run: # run the PROD tasks
	@ansible-playbook ./playbooks/*.yml -e @variables.enc --ask-vault-pass --user labmin -i ./hosts --tags "prod"
