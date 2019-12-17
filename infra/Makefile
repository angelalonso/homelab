#!make

init:
	@echo "Initializing..."
	pipenv install
	pipenv run python3 asd.py init
plan: init
	@echo "Planning..."
apply: init plan
	@echo "Applying..."

.PHONY : init plan apply
.DEFAULT_GOAL := plan
