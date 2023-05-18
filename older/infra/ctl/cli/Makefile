#!make

RUN_TEST=pipenv run pytest --cov . --flake8 -vv --cov-report html && firefox htmlcov/index.html

RUN_SEC=pipenv run bandit ./*.py -n 3 -ll

help:
	@echo   SYNTAX:
	@echo make init    - install dependencies
	@echo make run     - Run server
	@echo make help    - this help


sec:
	@$(RUN_SEC)

test:
	@$(RUN_TEST)


.PHONY : sec test help
.DEFAULT_GOAL := run
