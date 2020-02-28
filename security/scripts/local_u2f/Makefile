CWD := $(shell pwd)

U2F_TEST=pipenv run pytest --cov . -vv

U2F_SEC=pipenv run bandit ./*.py -n 3 -ll

U2F_INIT=pipenv install

U2F_ADD=pipenv run python3 local_u2f.py register

U2F_AUTH=pipenv run python3 local_u2f.py authenticate

U2F_RUN=pipenv run python3 local_u2f.py

sec:
	@$(U2F_SEC)

test:
	@$(U2F_TEST)

init:
	@$(U2F_INIT)

add:
	@$(U2F_ADD)

auth:
	@$(U2F_AUTH)

localu2f:
	@$(U2F_RUN)

help:
	@echo "Available commands:"
	@echo "init; localu2f; test; sec"
	@echo
