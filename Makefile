.DEFAULT_GOAL := help
.PHONY: help

define color-yellow
"\033[0;33m$1\033[0m"
endef

define color-red
"\033[0;31m$1\033[0m"
endef

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sed -n 's/^\(.*\): \(.*\)\(##.*\)/\1\3/p' \
	| column -t  -s '##'

clean: ## Remove all .pyc files from repo.
	@echo $(call color-yellow, "→ Clean working directory")
	@# Remove old pyc files
	find . -name "*.pyc" -exec rm -rf {} \;
	@echo $(call color-yellow, "✔︎ Cleaned")

test: clean .state-requirements test-ci ## Run test suite.

test-ci:
	python manage.py test

test-deprecations: clean .state-requirements ## Run test suite with deprecation checks
	python -Wall manage.py test

.state-requirements: requirements.txt
	@echo $(call color-yellow,"→ Detected change in requirements.txt")
	pip install -r requirements.txt
	@touch .state-requirements

autoformat: .state-requirements ## Auto format all code
	black . --exclude="venv/*"

lint: .state-requirements lint-ci ## Lint project

lint-ci:
	./manage.py makemigrations --check
	black . --check --exclude="(venv|src)"
	flake8 .
