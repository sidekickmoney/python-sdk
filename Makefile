PYTHON_VERSION ?= 3.10

help:
	@echo "Available commands:"
	@echo ""
	@echo "    help:              Show this page"
	@echo "    setup:             Setup the environment"
	@echo "    test:              Run fast tests"
	@echo "    test-all:          Run all tests"
	@echo "    test-all-versions: Run all tests on all versions"
	@echo "    acceptance-test:   Run acceptance tests"
	@echo "    integration-test:  Run integration tests"
	@echo "    load-test:         Run load tests"
	@echo "    performance-test:  Run performance tests"
	@echo "    property-test:     Run property tests"
	@echo "    system-test:       Run system tests"
	@echo "    unit-test:         Run unit tests"
	@echo "    lint:              Run the linters"
	@echo "    format:            Format the codebase"
	@echo "    package:           Package"
	@echo "    publish:           Publish"
	@echo "    install:           Install"
	@echo "    clean:             Cleanup"

.venv/${PYTHON_VERSION} setup:
	rm -rf .venv/${PYTHON_VERSION}
	python${PYTHON_VERSION} -m venv .venv/${PYTHON_VERSION}
	. .venv/${PYTHON_VERSION}/bin/activate && \
	python -m pip install --upgrade pip setuptools wheel && \
	python -m pip install --editable .[dev,test,hashing,secrets] --config-settings editable-mode=strict

test: lint unit-test integration-test acceptance-test

test-all: lint unit-test integration-test acceptance-test property-test load-test performance-test system-test

test-all-versions:
	make all-test PYTHON_VERSION=3.8
	make all-test PYTHON_VERSION=3.9
	make all-test PYTHON_VERSION=3.10

acceptance-test: .venv/${PYTHON_VERSION}
#	. .venv/${PYTHON_VERSION}/bin/activate && \
#	pytest -vv tests/acceptance

integration-test: .venv/${PYTHON_VERSION}
	docker-compose up -d
	. .venv/${PYTHON_VERSION}/bin/activate && \
	pytest -vv tests/integration

load-test: .venv/${PYTHON_VERSION}
#	. .venv/${PYTHON_VERSION}/bin/activate && \
#	pytest -vv tests/load

performance-test: .venv/${PYTHON_VERSION}
#	. .venv/${PYTHON_VERSION}/bin/activate && \
#	pytest -vv tests/performance

property-test: .venv/${PYTHON_VERSION}
	. .venv/${PYTHON_VERSION}/bin/activate && \
	pytest -vv tests/property

system-test: .venv/${PYTHON_VERSION}
#	. .venv/${PYTHON_VERSION}/bin/activate && \
#	pytest -vv tests/system

unit-test: .venv/${PYTHON_VERSION}
	. .venv/${PYTHON_VERSION}/bin/activate && \
	pytest -vv tests/unit

lint: .venv/${PYTHON_VERSION}
	. .venv/${PYTHON_VERSION}/bin/activate && \
	black --check . && \
	isort --check-only .

format: .venv/${PYTHON_VERSION}
	. .venv/${PYTHON_VERSION}/bin/activate && \
	black . && \
	isort .

package: .venv/${PYTHON_VERSION}
	@echo "TODO"

publish: .venv/${PYTHON_VERSION}
	@echo "TODO"

install: .venv/${PYTHON_VERSION}
	@echo "TODO"

clean:
	rm -rf .hypothesis .mypy_cache .pytest_cache testresults.xml .coverage .cache htmlcov *.egg-info build .test_artifacts
	find . -name "__pycache__" -type d -not -path "*/.venv/*" -not -path "*/.git/*" | xargs rm -rf
	find . -type f -name "*.pyc" -delete
	docker-compose down
