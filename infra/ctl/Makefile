#!make

help:
	@echo   SYNTAX:
	@echo make init    - install dependencies
	@echo make run     - Run server
	@echo make help    - this help

init:
	/home/aafmin/.local/bin/pipenv install

run:
	$(HOME)/.local/bin/pipenv run python3 api.py

.PHONY : init run help
.DEFAULT_GOAL := run
