#!make

test:
	@echo "    Testing...    "
	@echo "#######################"
	bash ./dependencies.sh
	pipenv install
	pipenv run pytest -vvv
create:
	@echo "    Creating a new Secrets File...    "
	@echo "#######################"
	pipenv install
	pipenv run python3 asd.py create
init:
	@echo "    Initializing...    "
	@echo "#######################"
	bash ./dependencies.sh
	pipenv install
	pipenv run python3 asd.py init
plan: init
	@echo "    Planning...        "
	@echo "#######################"
	pipenv run python3 asd.py plan
#  $(shell ansible-playbook -i ./manifests/hosts ./manifests/playbooks.yaml --check)
apply: plan
	@echo "    Applying...        "
	@echo "#######################"
	pipenv run python3 asd.py apply

.PHONY : init plan apply
.DEFAULT_GOAL := plan
