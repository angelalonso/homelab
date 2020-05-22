#!make

RUN_TEST=pipenv run pytest --cov . --flake8 -vv --cov-report html && firefox htmlcov/index.html

RUN_SEC=pipenv run bandit ./*.py -n 3 -ll

help:
	@echo   SYNTAX:
	@echo make init    - install dependencies
	@echo make run     - Run server
	@echo make help    - this help

init:
	/home/aafmin/.local/bin/pipenv install

sec:
	@$(RUN_SEC)

test:
	@$(RUN_TEST)


.PHONY : init sec test help
.DEFAULT_GOAL := run
