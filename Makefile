.PHONY: help install install-dev clean test test-fast test-cov test-watch lint format security type-check build docs serve-docs pre-commit setup-pre-commit update-deps audit fix-audit benchmark profile clean-all

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3.12
UV := uv
PROJECT := claude_prompts_tweaks
MIN_COVERAGE := 90

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install production dependencies
	$(UV) sync --frozen

install-dev: ## Install all dependencies including dev
	$(UV) sync --frozen --all-extras
	$(UV) run pre-commit install --install-hooks
	$(UV) run pre-commit install --hook-type commit-msg

clean: ## Clean build artifacts
	rm -rf build dist *.egg-info
	rm -rf .coverage coverage.xml htmlcov .pytest_cache
	rm -rf .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test: ## Run all tests with coverage
	$(UV) run pytest -v --cov=$(PROJECT) --cov-report=term-missing --cov-report=html --cov-fail-under=$(MIN_COVERAGE)

test-fast: ## Run tests without coverage (faster)
	$(UV) run pytest -v --no-cov -n auto

test-cov: ## Run tests and open coverage report
	$(UV) run pytest --cov=$(PROJECT) --cov-report=html --cov-fail-under=$(MIN_COVERAGE)
	open htmlcov/index.html

test-watch: ## Run tests in watch mode
	$(UV) run ptw -- -v --no-cov

lint: ## Run all linters
	$(UV) run black --check .
	$(UV) run isort --check-only .
	$(UV) run ruff check .
	$(UV) run pylint $(PROJECT) --fail-under=9.0
	$(UV) run mypy $(PROJECT) --strict

format: ## Format code with black and isort
	$(UV) run black .
	$(UV) run isort .
	$(UV) run ruff check --fix .

security: ## Run security checks
	$(UV) run bandit -r $(PROJECT) -f json -o bandit-report.json
	$(UV) run safety check --json
	$(UV) run pip-audit

type-check: ## Run type checking with mypy
	$(UV) run mypy $(PROJECT) --strict

build: ## Build distribution packages
	$(UV) build
	$(UV) run twine check dist/*
	$(UV) run check-wheel-contents dist/*.whl

docs: ## Build documentation
	$(UV) run sphinx-build -b html docs docs/_build/html -W --keep-going

serve-docs: docs ## Build and serve documentation
	cd docs/_build/html && python -m http.server

pre-commit: ## Run pre-commit on all files
	$(UV) run pre-commit run --all-files

setup-pre-commit: ## Set up pre-commit hooks
	$(UV) run pre-commit install --install-hooks
	$(UV) run pre-commit install --hook-type commit-msg
	$(UV) run pre-commit install --hook-type pre-push

update-deps: ## Update all dependencies
	$(UV) lock --upgrade
	$(UV) sync --all-extras

audit: ## Run comprehensive audit
	@echo "Running security audit..."
	$(UV) run pip-audit
	@echo "\nRunning dependency check..."
	$(UV) run safety check
	@echo "\nRunning code security scan..."
	$(UV) run bandit -r $(PROJECT) -ll
	@echo "\nChecking for outdated dependencies..."
	$(UV) pip list --outdated
	@echo "\nRunning license check..."
	$(UV) run pip-licenses --summary

fix-audit: ## Fix known security issues
	$(UV) run pip-audit --fix --dry-run
	@echo "Run 'uv run pip-audit --fix' to apply fixes"

benchmark: ## Run performance benchmarks
	$(UV) run pytest tests/benchmarks/ --benchmark-only --benchmark-json=benchmark.json
	@echo "Benchmark results saved to benchmark.json"

profile: ## Profile the code
	$(UV) run python -m cProfile -o profile.stats demo.py
	$(UV) run python -m pstats profile.stats

clean-all: clean ## Deep clean including caches and virtual environments
	rm -rf .venv
	rm -rf node_modules
	rm -rf .uv
	rm -rf .cache
	rm -rf pip-audit-report.json safety-report.json bandit-report.json
	rm -rf profile.stats benchmark.json

# Quality gate - run before committing
quality: format lint type-check test security ## Run all quality checks

# CI simulation - run what CI would run
ci: lint type-check test security build ## Simulate CI pipeline locally

# Release preparation
release-prep: quality build ## Prepare for release
	@echo "Ready for release!"
	@echo "Don't forget to:"
	@echo "  1. Update CHANGELOG.md"
	@echo "  2. Bump version in pyproject.toml"
	@echo "  3. Create git tag"
	@echo "  4. Push to main branch"