#!make

init:
	@echo "Initializing..."
#$(shell brew install https://raw.githubusercontent.com/kadwanev/bigboybrew/master/Library/Formula/sshpass.rb >/dev/null 2>&1)
	pipenv install
	pipenv run python3 asd.py init
plan: init
	@echo "Planning..."
	pipenv run python3 asd.py plan
#  $(shell ansible-playbook -i ./manifests/hosts ./manifests/playbooks.yaml --check)
apply: init plan
	@echo "Applying..."

.PHONY : init plan apply
.DEFAULT_GOAL := plan
