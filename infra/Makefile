#!make

help:
	@echo   SYNTAX:
	@echo make install - install dependencies
	@echo make check   - test secrets.yaml is correct (so far only IPs)
	@echo make init    - prepare manifests
	@echo make create  - Create secrets.yaml from a template
	@echo make plan    - Dry run of the manifests
	@echo make apply   - Apply manifests
	@echo make help    - this help

install:
	bash ./dependencies.sh
	pipenv install

test:
	pipenv run pytest -vvv
create:
	pipenv run python3 asd.py create
check:
	pipenv run python3 asd.py network
init:
	pipenv run python3 asd.py init
plan: init
	pipenv run python3 asd.py plan
apply:
	pipenv run python3 asd.py apply

.PHONY : install check init plan apply help
.DEFAULT_GOAL := plan
