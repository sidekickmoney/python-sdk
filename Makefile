PYTHON_VERSION ?= 3.10

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
	@echo "    system-test:       Run system tests"
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


# TODO: Manually check if venv exists
.venv/${PYTHON_VERSION} setup:
	rm -rf .venv/${PYTHON_VERSION}
	python${PYTHON_VERSION} -m venv .venv/${PYTHON_VERSION}
	. .venv/${PYTHON_VERSION}/bin/activate && \
	python -m pip install --upgrade pip setuptools wheel && \
	python -m pip install --editable .[dev,test,hashing,secrets] #--config-settings editable-mode=strict

test: unit-test integration-test functional-test acceptance-test

test-all: unit-test integration-test property-test functional-test security-test system-test acceptance-test performance-test

test-all-versions:
	make all-test PYTHON_VERSION=3.8
	make all-test PYTHON_VERSION=3.9
	make all-test PYTHON_VERSION=3.10

unit-test: .venv/${PYTHON_VERSION}
	. .venv/${PYTHON_VERSION}/bin/activate && \
	pytest -vv tests/unit

integration-test: .venv/${PYTHON_VERSION}
	docker-compose up -d
	. .venv/${PYTHON_VERSION}/bin/activate && \
	pytest -vv tests/integration

property-test: .venv/${PYTHON_VERSION}
	. .venv/${PYTHON_VERSION}/bin/activate && \
	pytest -vv tests/property

functional-test: .venv/${PYTHON_VERSION}
	@echo "Nothing to do"

security-test: .venv/${PYTHON_VERSION}
	@echo "Nothing to do"

system-test: .venv/${PYTHON_VERSION}
	@echo "Nothing to do"

acceptance-test: .venv/${PYTHON_VERSION}
	@echo "Nothing to do"

performance-test: .venv/${PYTHON_VERSION}
	@echo "Nothing to do"

#lint: .venv/${PYTHON_VERSION}
#	. .venv/${PYTHON_VERSION}/bin/activate && \
#	python-sdk fmt --files . --check

fmt: .venv/${PYTHON_VERSION}
	. .venv/${PYTHON_VERSION}/bin/activate && \
	python-sdk fmt --files .

package: .venv/${PYTHON_VERSION}
	@echo "Not implemented"

publish: .venv/${PYTHON_VERSION}
	@echo "Not implemented"

install: .venv/${PYTHON_VERSION}
	@echo "Not implemented"

clean:
	rm -rf .hypothesis .mypy_cache .pytest_cache testresults.xml .coverage .cache htmlcov *.egg-info build .test_artifacts
	find . -name "__pycache__" -type d -not -path "*/.venv/*" -not -path "*/.git/*" | xargs rm -rf
	find . -type f -name "*.pyc" -delete
	docker-compose down
