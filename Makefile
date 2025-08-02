.PHONY: help install install-dev format lint type-check test test-fast coverage clean build publish

help:
	@echo "Available commands:"
	@echo "  make install       Install project dependencies"
	@echo "  make install-dev   Install project with dev dependencies"
	@echo "  make format        Format code with black and isort"
	@echo "  make lint          Run linting checks"
	@echo "  make type-check    Run mypy type checking"
	@echo "  make test          Run all tests with coverage"
	@echo "  make test-fast     Run tests without coverage"
	@echo "  make coverage      Generate HTML coverage report"
	@echo "  make clean         Clean build artifacts"
	@echo "  make build         Build distribution packages"
	@echo "  make publish       Publish to PyPI (requires auth)"

install:
	uv sync

install-dev:
	uv sync --all-extras
	uv run pre-commit install

format:
	uv run black .
	uv run isort .

lint:
	uv run black --check .
	uv run isort --check-only .

type-check:
	uv run mypy claude_prompts_tweaks

test:
	uv run pytest

test-fast:
	uv run pytest --no-cov

coverage:
	uv run pytest --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	uv build

publish: build
	uv run twine upload dist/*