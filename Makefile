define color-yellow
"\033[0;33m$1\033[0m"
endef

define color-red
"\033[0;31m$1\033[0m"
endef

help:
	@echo "    clean"
	@echo "        Remove all .pyc files from repo."
	@echo "    test"
	@echo "        Run test suite."
	@echo "    test-with-coverage"
	@echo "        Run tests and generate a coverage report."
	@echo "    lint"
	@echo "        Run flake8."
	@echo "    release"
	@echo "        Release to PyPi."

clean:
	@echo $(call color-yellow, "→ Clean working directory")
	@# Remove old pyc files
	find . -name "*.pyc" -exec rm -rf {} \;
	@echo $(call color-yellow, "✔︎ Cleaned")

test: clean
	python setup.py test

test-with-coverage: clean
	coverage run setup.py test

lint:
	flake8 .

release:
	mkdir -p dist
	python setup.py publish

.PHONY: help clean test test-with-coverage lint release
