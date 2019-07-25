SHELL  := /bin/bash
PATH            := ${PATH}:${HOME}/.local/bin

# Variables
PENV         ?= penv
PY_ACTIVATE := $(PENV)/bin/activate

penv-init:
	rm -rf $(PENV)
	mkdir -p $(PENV)
	cp requirements.txt $(PENV)/requirements.txt
	cp requirements-dev.txt $(PENV)/requirements-dev.txt

tools:
	pip3 install pythonenv virtualenv

init: penv-init tools
	cd $(PENV) && \
	virtualenv . --always-copy --python=python3 && \
	source ./bin/activate && \
	pip3 install --no-cache-dir -r requirements.txt && \
	pip3 install --no-cache-dir -r requirements-dev.txt

start-wsgi:
	source $(PY_ACTIVATE) && \
	python3 application.py