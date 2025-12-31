.PHONY: help install test test-verbose coverage clean

help:
	@echo "Available commands:"
	@echo "  make install        - Set up virtual environment and install dependencies"
	@echo "  make test           - Run tests"
	@echo "  make test-verbose   - Run tests with verbose output"
	@echo "  make coverage       - Run tests with coverage report"
	@echo "  make clean          - Remove virtual environment and cache files"

install:
	python3 -m venv venv
	./venv/bin/pip install -e ".[dev]"

test:
	./venv/bin/pytest

test-verbose:
	./venv/bin/pytest -v

coverage:
	./venv/bin/pytest --cov=mdx_better_lists --cov-report=term-missing --cov-report=html

clean:
	rm -rf venv
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
