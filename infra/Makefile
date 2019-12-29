#!make

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

.PHONY : init plan apply
.DEFAULT_GOAL := plan
