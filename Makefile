PYTHON_VERSION ?= 3.10
OS := $(shell uname -s)

help:
	@echo "Available commands:"
	@echo ""
	@echo "    help:              Show this page"
	@echo "    setup:             Setup the environment"
	@echo "    test:              Run fast tests"
	@echo "    test-all:          Run all tests"
	@echo "    unit-test:         Run unit tests"
	@echo "    integration-test:  Run integration tests"
	@echo "    property-test:     Run property tests"
	@echo "    functional-test:   Run functional tests"
	@echo "    security-test:     Run security tests"
	@echo "    smoke-test:        Run smoke tests"
	@echo "    acceptance-test:   Run acceptance tests"
	@echo "    performance-test:  Run performance tests"
	@echo "    fmt:               Format the codebase"
	@echo "    package:           Package"
	@echo "    publish:           Publish"
	@echo "    install:           Install"
	@echo "    clean:             Cleanup"
	@echo ""
	@echo "Project-specific commands:"
	@echo ""
	@echo "    test-all-versions: Run all tests on all supported versions"


setup:
	@if [ ! -d ".venv/${OS}/${PYTHON_VERSION}" ]; then\
		python${PYTHON_VERSION} -m venv ".venv/${OS}/${PYTHON_VERSION}" &&\
		. ".venv/${OS}/${PYTHON_VERSION}/bin/activate" &&\
		python -m pip install --upgrade pip setuptools wheel &&\
		python -m pip install --editable .[dev,test,hashing,secrets] ;\
	fi

test: unit-test integration-test functional-test acceptance-test

test-all: unit-test integration-test property-test functional-test security-test smoke-test acceptance-test performance-test

test-all-versions:
	make all-test PYTHON_VERSION=3.8
	make all-test PYTHON_VERSION=3.9
	make all-test PYTHON_VERSION=3.10

unit-test: setup
	. .venv/${OS}/${PYTHON_VERSION}/bin/activate && \
	pytest -vv tests/unit

integration-test: setup
	docker-compose up -d
	. .venv/${OS}/${PYTHON_VERSION}/bin/activate && \
	pytest -vv tests/integration

property-test: setup
	. .venv/${OS}/${PYTHON_VERSION}/bin/activate && \
	pytest -vv tests/property

functional-test: setup
	@echo "Nothing to do"

security-test: setup
	@echo "Nothing to do"

smoke-test: setup
	@echo "Nothing to do"

acceptance-test: setup
	@echo "Nothing to do"

performance-test: setup
	@echo "Nothing to do"

fmt: setup
	. .venv/${OS}/${PYTHON_VERSION}/bin/activate && \
	python-sdk fmt --files .

package: setup
	@echo "Not implemented"

publish: setup
	@echo "Not implemented"

install: setup
	@echo "Not implemented"

clean:
	rm -rf .venv
	rm -rf .hypothesis .mypy_cache .pytest_cache testresults.xml .coverage .cache htmlcov *.egg-info build .test_artifacts
	find . -name "__pycache__" -type d -not -path "*/.venv/*" -not -path "*/.git/*" | xargs rm -rf
	find . -type f -name "*.pyc" -delete
	docker-compose down || true
