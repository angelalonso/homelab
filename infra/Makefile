#!make

help:
	@echo   SYNTAX:
	@echo make install - install dependencies
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
init:
	pipenv run python3 asd.py init
plan: init
	pipenv run python3 asd.py plan
apply:
	pipenv run python3 asd.py apply

.PHONY : install init plan apply help
.DEFAULT_GOAL := plan
