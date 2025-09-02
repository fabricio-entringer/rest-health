# Contributing to rest-health

Thank you for your interest in contributing to `rest-health`! This document provides comprehensive information about the project structure, development workflow, and technical requirements.

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Project Overview](#-project-overview)
- [Development Setup](#-development-setup)
- [Project Structure](#-project-structure)
- [Development Workflow](#-development-workflow)
- [Code Quality Standards](#-code-quality-standards)
- [Testing](#-testing)
- [Build System](#-build-system)
- [CI/CD Pipelines](#-cicd-pipelines)
- [Makefile Commands](#-makefile-commands)
- [Release Process](#-release-process)
- [Contribution Guidelines](#-contribution-guidelines)

## 🚀 Quick Start

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/rest-health.git
cd rest-health

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install development dependencies
make install-dev

# 4. Run all checks to ensure everything works
make ci

# 5. Create a new branch for your feature
git checkout -b feature/your-feature-name
```

## 🎯 Project Overview

`rest-health` is a framework-agnostic Python library that provides standardized REST healthcheck endpoints for web applications. The project focuses on:

- **Framework Independence**: Core logic works with any Python web framework
- **Simplicity**: Clean, minimal API with no unnecessary complexity
- **Production Readiness**: Proper error handling and standard HTTP responses
- **Type Safety**: Full type annotations with mypy validation
- **High Quality**: Comprehensive testing and code quality checks

### Core Design Principles

1. **Framework Agnostic**: Core functionality independent of web frameworks
2. **Adapter Pattern**: Framework-specific integrations via adapters
3. **Fail-Safe**: Graceful error handling with informative responses
4. **Zero Dependencies**: Core library has no external dependencies
5. **Type Safe**: Full type annotations and mypy compliance

## 🛠️ Development Setup

### Prerequisites

- **Python**: 3.8 or higher (3.9+ recommended for development due to mypy)
- **pip**: Latest version
- **git**: For version control

### Environment Setup

```bash
# Clone the repository
git clone https://github.com/fabricio-entringer/rest-health.git
cd rest-health

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install development dependencies
make install-dev

# Verify installation
make info
```

### IDE Configuration

#### VS Code (Recommended)

The project includes workspace settings. Install these extensions:
- Python
- Black Formatter
- Pylance
- Flake8

#### PyCharm

Configure:
- Interpreter: Point to your virtual environment
- Code style: Black (line length: 88)
- Type checker: mypy

## 📁 Project Structure

```
rest-health/
├── .github/
│   └── workflows/          # GitHub Actions CI/CD pipelines
│       ├── pr-validation.yml      # PR validation workflow
│       ├── publish-to-pypi.yml    # PyPI publishing workflow
│       └── create-release.yml     # GitHub release workflow
├── assets/
│   └── rest-health-logo.png       # Project logo
├── src/
│   └── rest_health/               # Main package
│       ├── __init__.py           # Package exports
│       ├── core/                 # Core functionality
│       │   ├── __init__.py
│       │   └── checker.py        # HealthCheck class
│       └── adapters/             # Framework adapters
│           ├── __init__.py
│           ├── fastapi.py        # FastAPI integration
│           └── flask.py          # Flask integration
├── tests/
│   ├── __init__.py
│   └── test_checker.py           # Unit tests
├── pyproject.toml                # Project configuration
├── Makefile                      # Development automation
├── README.md                     # Project documentation
├── LICENSE                       # MIT License
└── CONTRIBUTING.md               # This file
```

### Key Files Explained

- **`src/rest_health/core/checker.py`**: Main `HealthCheck` class implementation
- **`src/rest_health/adapters/`**: Framework-specific integrations
- **`pyproject.toml`**: Project metadata, dependencies, and tool configurations
- **`Makefile`**: Development automation commands
- **`.github/workflows/`**: CI/CD pipeline definitions

## 🔄 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### 2. Development Cycle

```bash
# Make your changes
# ...

# Run quick checks during development
make quick-check

# Run full validation before committing
make all

# Auto-fix formatting issues
make fix
```

### 3. Commit and Push

```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

### 4. Create Pull Request

- Target the `develop` branch
- Follow the PR template
- Ensure all CI checks pass

## ✅ Code Quality Standards

### Code Formatting

- **Tool**: Black
- **Line Length**: 88 characters
- **Target**: Python 3.8+

```bash
# Check formatting
make format-check

# Auto-format code
make format
```

### Linting

- **Tool**: Flake8
- **Configuration**: Defined in `pyproject.toml`
- **Key Rules**: E9, F63, F7, F82 errors, max complexity 10

```bash
# Run linting
make lint
```

### Type Checking

- **Tool**: mypy
- **Configuration**: Strict mode with `disallow_untyped_defs`
- **Python Version**: 3.9+ (for mypy compatibility)

```bash
# Run type checking
make type-check
```

### Import Standards

```python
# Standard library imports first
import os
import sys

# Third-party imports second
import requests
import flask

# Local imports last
from rest_health import HealthCheck
from rest_health.core.checker import SomeClass
```

### Type Annotation Standards

```python
from typing import Dict, Any, Optional, Union

def health_check() -> bool:
    """All functions must have return type annotations."""
    return True

def add_check(self, name: str, check_func: Callable[[], bool]) -> None:
    """Include parameter types for all functions."""
    self.checks[name] = check_func
```

## 🧪 Testing

### Test Framework

- **Framework**: pytest
- **Coverage**: pytest-cov
- **Target**: >90% code coverage

### Running Tests

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run specific test file
pytest tests/test_checker.py

# Run specific test
pytest tests/test_checker.py::TestHealthCheck::test_empty_healthcheck
```

### Writing Tests

```python
"""
Test file naming: test_*.py
Test class naming: TestClassName
Test method naming: test_method_description
"""

import pytest
from rest_health import HealthCheck

class TestHealthCheck:
    """Test cases for the HealthCheck class."""
    
    def test_feature_name(self):
        """Test description with expected behavior."""
        # Arrange
        health = HealthCheck()
        
        # Act
        result = health.run()
        
        # Assert
        assert result["status"] == "ok"
```

### Test Coverage Requirements

- **Minimum**: 80% overall coverage
- **New Code**: Must have 90% coverage
- **Critical Paths**: Error handling must be tested
- **Integration**: Framework adapters must have integration tests

## 🏗️ Build System

### Configuration

The project uses **setuptools** with `pyproject.toml` configuration:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"
```

### Building

```bash
# Clean previous builds
make clean

# Build package
make build

# Check build artifacts
ls dist/
```

### Package Structure

```
dist/
├── rest_health-0.1.0.tar.gz         # Source distribution
└── rest_health-0.1.0-py3-none-any.whl  # Wheel distribution
```

## 🔧 CI/CD Pipelines

### 1. PR Validation Workflow

**File**: `.github/workflows/pr-validation.yml`
**Trigger**: Pull requests to `develop` branch

**Jobs**:
- **validate**: Multi-Python version testing (3.8-3.13)
  - Code formatting check
  - Linting with flake8
  - Type checking with mypy
  - Package building
  - Test execution with coverage
- **security-check**: Security vulnerability scanning
- **dependency-check**: Dependency audit

### 2. PyPI Publishing Workflow

**File**: `.github/workflows/publish-to-pypi.yml`
**Trigger**: Push to `master` branch

**Jobs**:
- **build**: Quality checks and package building
- **publish-to-pypi**: Automatic PyPI publication
- **publish-to-testpypi**: Manual TestPyPI publication

### 3. Release Creation Workflow

**File**: `.github/workflows/create-release.yml`
**Trigger**: Successful PyPI publication

**Features**:
- Automatic GitHub release creation
- Generated release notes from commit history
- Git tag creation
- Categorized changelog (features, fixes, improvements)

### Environment Variables

```bash
# Required GitHub Secrets
PYPI_USER_NAME    # PyPI username
PYPI_TOKEN        # PyPI API token
GITHUB_TOKEN      # Automatic (GitHub Actions)
```

## 🔨 Makefile Commands

### Essential Commands

```bash
make help              # Show all available commands
make install-dev       # Install development dependencies
make ci               # Complete CI pipeline simulation
```

### Development Commands

```bash
make format-check     # Check code formatting (CI equivalent)
make lint            # Run linting (CI equivalent)
make type-check      # Run type checking (CI equivalent)
make test-cov        # Run tests with coverage (CI equivalent)
make build           # Build package (CI equivalent)
```

### Utility Commands

```bash
make clean           # Remove build artifacts
make format          # Auto-format code
make fix            # Auto-fix common issues
make info           # Show project information
```

### Workflow Shortcuts

```bash
make all            # format-check + lint + type-check + test-cov + build
make dev-check      # format-check + lint + type-check + test
make quick-check    # format-check + lint + test
```

### Security Commands

```bash
make security-check     # Run safety and bandit scans
make dependency-check   # Run pip-audit dependency check
```

## 📦 Release Process

### Versioning Strategy

- **Semantic Versioning**: MAJOR.MINOR.PATCH
- **Version Location**: `pyproject.toml` → `[project].version`
- **Release Branches**: `master` (production), `develop` (integration)

### Release Steps

1. **Prepare Release**:
   ```bash
   # Update version in pyproject.toml
   vim pyproject.toml  # Change version = "0.1.1"
   
   # Run full validation
   make ci
   
   # Commit version bump
   git add pyproject.toml
   git commit -m "bump: version 0.1.1"
   ```

2. **Merge to Master**:
   ```bash
   git checkout master
   git merge develop
   git push origin master
   ```

3. **Automatic Process**:
   - PyPI publication workflow triggers
   - Package builds and publishes to PyPI
   - Release creation workflow triggers
   - GitHub release created with generated notes

### Version Bumping Guidelines

- **PATCH** (0.1.0 → 0.1.1): Bug fixes, documentation updates
- **MINOR** (0.1.0 → 0.2.0): New features, backward-compatible changes
- **MAJOR** (0.1.0 → 1.0.0): Breaking changes, API redesign

## 🤝 Contribution Guidelines

### Code Style

1. **Follow PEP 8** with Black formatting
2. **Use type hints** for all function signatures
3. **Write docstrings** for public APIs
4. **Keep functions focused** and single-purpose
5. **Use meaningful variable names**

### Commit Message Format

```
<type>: <description>

<optional body>

<optional footer>
```

**Types**:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/modifications
- `chore`: Maintenance tasks

**Examples**:
```
feat: add support for custom health check timeouts
fix: handle connection errors in database health checks
docs: update FastAPI integration examples
```

### Pull Request Guidelines

1. **Target Branch**: Always target `develop` branch
2. **Description**: Clearly describe changes and motivation
3. **Tests**: Include tests for new functionality
4. **Documentation**: Update docs for user-facing changes
5. **CI Checks**: Ensure all automated checks pass

### Issue Reporting

When reporting issues:

1. **Use Issue Templates**: Follow the provided templates
2. **Provide Context**: Include Python version, framework, OS
3. **Minimal Example**: Provide reproducible code sample
4. **Expected vs Actual**: Clearly describe the problem

### Feature Requests

For new features:

1. **Check Existing Issues**: Avoid duplicates
2. **Describe Use Case**: Explain the problem you're solving
3. **Propose Solution**: Suggest implementation approach
4. **Consider Alternatives**: Discuss other possible solutions

## 🔍 Debugging and Troubleshooting

### Common Issues

1. **mypy Errors**: 
   - Ensure Python 3.9+ for development
   - Check type annotations are complete
   - Verify import error configurations

2. **Test Failures**:
   - Run tests in clean environment
   - Check test isolation
   - Verify mock configurations

3. **Import Errors**:
   - Check optional dependencies are installed
   - Verify package is installed in development mode

### Development Tips

1. **Use Virtual Environments**: Always isolate dependencies
2. **Run Checks Frequently**: Use `make quick-check` during development
3. **Test Edge Cases**: Consider error conditions and boundary cases
4. **Profile Performance**: Monitor for performance regressions

## 📚 Additional Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Type Hints Documentation](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🙋 Getting Help

- **Issues**: [GitHub Issues](https://github.com/fabricio-entringer/rest-health/issues)
- **Discussions**: [GitHub Discussions](https://github.com/fabricio-entringer/rest-health/discussions)
- **Email**: [fabricio.entringer@example.com](mailto:fabricio.entringer@example.com)

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

---

Thank you for contributing to `rest-health`! Your efforts help make health monitoring simpler and more reliable for Python web applications. 🎉