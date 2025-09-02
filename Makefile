# Makefile for rest-health project
# Uses the same tools and configurations as GitHub workflows

.PHONY: help install install-dev clean format format-check lint type-check test test-cov build security-check dependency-check all ci

# Default target
help:
	@echo "Available targets:"
	@echo "  install          - Install package in development mode"
	@echo "  install-dev      - Install package with development dependencies"
	@echo "  clean           - Remove build artifacts and cache files"
	@echo "  format          - Format code with black"
	@echo "  format-check    - Check code formatting with black (same as CI)"
	@echo "  lint            - Lint code with flake8 (same as CI)"
	@echo "  type-check      - Type check with mypy (same as CI)"
	@echo "  test            - Run tests with pytest"
	@echo "  test-cov        - Run tests with coverage (same as CI)"
	@echo "  build           - Build package (same as CI)"
	@echo "  security-check  - Run security checks with safety and bandit"
	@echo "  dependency-check - Check dependencies with pip-audit"
	@echo "  all             - Run all checks and build (format-check, lint, type-check, test-cov, build)"
	@echo "  ci              - Run complete CI pipeline (same as GitHub workflows)"

# Installation targets
install:
	python -m pip install --upgrade pip
	pip install -e .

install-dev:
	python -m pip install --upgrade pip
	pip install build
	pip install -e ".[dev]"

# Clean up build artifacts and cache
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Code formatting
format:
	black src/ tests/

format-check:
	@echo "🔍 Checking code format with Black (same as CI)..."
	black --check --diff src/ tests/

# Code linting
lint:
	@echo "🔍 Linting with flake8 (same as CI)..."
	flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 src/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

# Type checking
type-check:
	@echo "🔍 Type checking with mypy (same as CI)..."
	mypy src/

# Testing
test:
	@echo "🧪 Running tests with pytest..."
	pytest

test-cov:
	@echo "🧪 Running tests with coverage (same as CI)..."
	pytest --cov=rest_health --cov-report=xml --cov-report=term-missing

# Building
build:
	@echo "📦 Building package (same as CI)..."
	python -m build

# Security and dependency checks
security-check:
	@echo "🔒 Running security checks..."
	@echo "Checking for security vulnerabilities with safety..."
	safety check || true
	@echo "Running security analysis with bandit..."
	bandit -r src/ -f json -o bandit-report.json || true
	bandit -r src/

dependency-check:
	@echo "🔍 Checking dependencies with pip-audit..."
	pip install pip-audit
	pip-audit --desc --output pip-audit-report.json --format json || true
	pip-audit --desc

# Combined targets
all: format-check lint type-check test-cov build
	@echo "✅ All checks passed and package built successfully!"

ci: install-dev format-check lint type-check test-cov build security-check dependency-check
	@echo "✅ Complete CI pipeline finished successfully!"

# Development workflow shortcuts
dev-check: format-check lint type-check test
	@echo "✅ Development checks completed!"

quick-check: format-check lint test
	@echo "✅ Quick checks completed!"

# Fix common issues
fix:
	@echo "🔧 Auto-fixing code issues..."
	black src/ tests/
	@echo "✅ Code formatted with Black"

# Install pre-commit hooks (optional)
install-hooks:
	@echo "Installing pre-commit hooks..."
	pip install pre-commit
	pre-commit install
	@echo "✅ Pre-commit hooks installed"

# Show project info
info:
	@echo "Project: rest-health"
	@echo "Python version: $$(python --version)"
	@echo "Pip version: $$(pip --version)"
	@echo "Package info:"
	@python -c "import tomli; f=open('pyproject.toml','rb'); data=tomli.load(f); print(f\"  Name: {data['project']['name']}\"); print(f\"  Version: {data['project']['version']}\"); print(f\"  Description: {data['project']['description']}\"); f.close()"