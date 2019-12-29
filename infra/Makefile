#!make

help:
	@echo   SYNTAX:
	@echo make init   - install dependencies, prepare manifests
	@echo make create - Create secrets.yaml from a template
	@echo make plan   - Dry run of the manifests
	@echo make apply  - Apply manifests
	@echo make help   - this help

test:
	bash ./dependencies.sh
	pipenv install
	pipenv run pytest -vvv
create:
	pipenv install
	pipenv run python3 asd.py create
init:
	bash ./dependencies.sh
	pipenv install
	pipenv run python3 asd.py init
plan: init
	pipenv run python3 asd.py plan
#  $(shell ansible-playbook -i ./manifests/hosts ./manifests/playbooks.yaml --check)
apply: plan
	pipenv run python3 asd.py apply

.PHONY : init plan apply help
.DEFAULT_GOAL := plan
