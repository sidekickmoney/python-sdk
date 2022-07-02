PYTHON_VERSION := 3.10

help:
	@echo "Available commands:"
	@echo ""
	@echo "    help:             Show this page"
	@echo "    setup:            Setup the project"
	@echo "    test:             Run fast tests"
	@echo "    all-test:         Run all tests"
	@echo "    acceptance-test:  Run acceptance tests"
	@echo "    integration-test: Run integration tests"
	@echo "    load-test:        Run load tests"
	@echo "    performance-test: Run performance tests"
	@echo "    property-test:    Run property tests"
	@echo "    system-test:      Run system tests"
	@echo "    unit-test:        Run unit tests"
	@echo "    lint:             Run the linters"
	@echo "    format:           Format the codebase"
	@echo "    package:          Package"
	@echo "    publish:          Publish"
	@echo "    build:            Build"
	@echo "    upload:           Upload"
	@echo "    install:          Install"
	@echo "    clean:            Cleanup"

.venv setup:
	rm -rf .venv
	python${PYTHON_VERSION} -m venv .venv
	. .venv/bin/activate && \
	python -m pip install .[test package]

test: acceptance-test integration-test unit-test

all-test: acceptance-test integration-test load-test performance-test property-test system-test unit-test

acceptance-test: .venv
	. .venv/bin/activate && \
	pytest -vv tests/acceptance

integration-test: .venv
	. .venv/bin/activate && \
	pytest -vv tests/integration

load-test: .venv
	. .venv/bin/activate && \
	pytest -vv tests/load

performance-test: .venv
	. .venv/bin/activate && \
	pytest -vv tests/performance

property-test: .venv
	. .venv/bin/activate && \
	pytest -vv tests/property

system-test: .venv
	. .venv/bin/activate && \
	pytest -vv tests/system

unit-test: .venv
	. .venv/bin/activate && \
	pytest -vv tests/unit

lint: .venv
	. .venv/bin/activate && \
	black --check . && \
	isort --check-only .

format: .venv
	. .venv/bin/activate && \
	black . && \
	isort .

package: .venv
	@echo "TODO"

publish: .venv
	@echo "TODO"

build: .venv
	@echo "TODO"

upload: .venv
	@echo "TODO"

install: .venv
	@echo "TODO"

clean:
	@rm -rf .hypothesis .mypy_cache .pytest_cache testresults.xml .coverage .cache htmlcov *.egg-info
	@find . -name "__pycache__" -type d \
		-not -path "*/.venv/*" \
		-not -path "*/.git/*" | xargs rm -rf
	@find . -type f -name "*.pyc" -delete
