#!make
include .env
export

SHELL := /bin/bash

ROOT_DIR = $(strip $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST)))))
DEV_DIR = $(ROOT_DIR)/development
DB_DIR = $(DEV_DIR)/postgres
SCRIPTS_DIR = $(DEV_DIR)/scripts
AIRFLOW_DIR = $(ROOT_DIR)/src
AIRFLOW_SCRIPTS_DIR = $(AIRFLOW_DIR)/scripts

venv-pyenv:
	cd $(SCRIPTS_DIR); . $(SCRIPTS_DIR)/setup_venv_pyenv.sh

venv-requirements-pyenv:
	cd $(AIRFLOW_SCRIPTS_DIR); . $(HOME)/.pyenv/versions/$(PYTHON_VENV)/bin/activate && . $(AIRFLOW_SCRIPTS_DIR)/install_requirements_pyenv.sh

db-up:
	cd $(DB_DIR); docker-compose -f $(DB_DIR)/docker-compose.yaml up -d

db-up-build:
	cd $(DB_DIR); docker-compose -f $(DB_DIR)/docker-compose.yaml up -d --build

db-down:
	cd $(DB_DIR); docker-compose -f $(DB_DIR)/docker-compose.yaml down

airflow-build:
	cd $(AIRFLOW_DIR); . $(AIRFLOW_DIR)/mwaa build-image

airflow-start:
	cd $(AIRFLOW_DIR); . $(AIRFLOW_DIR)/mwaa start

airflow-test-requirements:
	cd $(AIRFLOW_DIR); . $(AIRFLOW_DIR)/mwaa test-requirements

airflow-set-variables:
	cd $(AIRFLOW_DIR); . $(AIRFLOW_DIR)/mwaa set-variables

airflow-set-connections:
	cd $(AIRFLOW_DIR); . $(AIRFLOW_DIR)/mwaa set-connections

airflow-reset-db:
	cd $(AIRFLOW_DIR); . $(AIRFLOW_DIR)/mwaa reset-db

linter:
	pre-commit clean && pre-commit run --files $(AIRFLOW_DIR)

init: db-up-build airflow-build airflow-start airflow-set-variables airflow-set-connections airflow-test-requirements

up: db-up airflow-start

down: db-down

all: init linter
