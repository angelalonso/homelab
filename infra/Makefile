#!make

init:
	@echo "Initializing..."
	bash ./dependencies.sh
	pipenv install
	pipenv run python3 asd.py init
plan: init
	@echo "Planning..."
	pipenv run python3 asd.py plan
#  $(shell ansible-playbook -i ./manifests/hosts ./manifests/playbooks.yaml --check)
apply: plan
	@echo "Applying..."
	pipenv run python3 asd.py apply

.PHONY : init plan apply
.DEFAULT_GOAL := plan