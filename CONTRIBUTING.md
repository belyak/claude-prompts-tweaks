# Contributing to Claude Prompts Tweaks

Thank you for your interest in contributing! This guide will help you get started with our development workflow.

## Development Setup

### Prerequisites

- Python 3.12+
- uv (install with `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Git
- Make (optional but recommended)

### Initial Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/yourusername/claude-prompts-tweaks.git
   cd claude-prompts-tweaks
   ```

2. Install development dependencies:
   ```bash
   make install-dev
   # or manually:
   uv sync --frozen --all-extras
   uv run pre-commit install --install-hooks
   ```

3. Verify setup:
   ```bash
   make test-fast
   # or: uv run pytest -v --no-cov
   ```

## Development Workflow

### Code Quality Standards

We maintain strict code quality standards. All code must:

1. **Pass formatting checks**:
   ```bash
   make format  # Auto-format code
   make lint    # Check formatting
   ```

2. **Pass type checking**:
   ```bash
   make type-check
   ```

3. **Have 90%+ test coverage**:
   ```bash
   make test
   ```

4. **Pass security scans**:
   ```bash
   make security
   ```

### Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following TDD:
   - Write tests first
   - Implement the feature
   - Ensure all tests pass

3. Run quality checks:
   ```bash
   make quality  # Runs all checks
   ```

4. Commit using conventional commits:
   ```bash
   git commit -m "feat: add new feature"
   ```

   Commit types:
   - `feat`: New feature
   - `fix`: Bug fix
   - `docs`: Documentation changes
   - `style`: Code style changes
   - `refactor`: Code refactoring
   - `test`: Test additions/changes
   - `chore`: Maintenance tasks

### Testing

#### Running Tests

```bash
# All tests with coverage
make test

# Fast tests without coverage
make test-fast

# Watch mode
make test-watch

# Specific test file
uv run pytest tests/test_main.py

# With coverage report
make test-cov
```

#### Writing Tests

- Use pytest for all tests
- Follow AAA pattern (Arrange, Act, Assert)
- Use fixtures for common setup
- Include both positive and negative test cases
- Use hypothesis for property-based testing where appropriate

Example:
```python
def test_feature_success(fixture_name: Any) -> None:
    """Test that feature works correctly with valid input."""
    # Arrange
    input_data = {"key": "value"}
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_output
    assert result.property == expected_value
```

### Type Annotations

All code must be fully type annotated:

```python
from typing import Optional, List, Dict, Any

def process_data(
    items: List[Dict[str, Any]], 
    filter_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Process data with optional filtering."""
    if filter_key is None:
        return items
    return [item for item in items if filter_key in item]
```

### Documentation

- All public functions/classes must have docstrings
- Use Google-style docstrings
- Include type information in docstrings
- Add usage examples for complex functions

Example:
```python
def complex_function(param1: str, param2: int) -> Dict[str, Any]:
    """Perform a complex operation.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Dictionary containing results
        
    Raises:
        ValueError: If param2 is negative
        
    Example:
        >>> result = complex_function("test", 42)
        >>> print(result["status"])
        success
    """
```

## CI/CD Pipeline

Our CI pipeline automatically runs on all PRs:

1. **Quality Checks** (parallel):
   - Code formatting (black, isort)
   - Type checking (mypy)
   - Linting (ruff, pylint)
   - Security scanning (bandit, safety, pip-audit)

2. **Testing**:
   - Multi-OS testing (Ubuntu, Windows, macOS)
   - Multi-Python version (3.10-3.13)
   - Coverage reporting with 90% minimum

3. **Build Verification**:
   - Package building
   - Distribution checks

### Pre-commit Hooks

Pre-commit hooks run automatically before each commit. To run manually:

```bash
make pre-commit
# or: uv run pre-commit run --all-files
```

## Security

### Reporting Security Issues

Please report security vulnerabilities to [security email] instead of public issues.

### Security Checks

Run security scans locally:

```bash
make security
make audit
```

## Pull Request Process

1. Ensure all tests pass locally
2. Update documentation if needed
3. Add tests for new functionality
4. Ensure PR description clearly describes changes
5. Link related issues in PR description
6. Request review from maintainers

### PR Checklist

- [ ] Tests pass locally (`make test`)
- [ ] Code is formatted (`make format`)
- [ ] Type checking passes (`make type-check`)
- [ ] Security scans pass (`make security`)
- [ ] Documentation updated
- [ ] Conventional commit messages used
- [ ] PR has descriptive title

## Release Process

Releases are automated using semantic-release:

1. Merge PR to main branch
2. CI automatically:
   - Determines version from commits
   - Creates changelog
   - Tags release
   - Publishes to PyPI

## Getting Help

- Check existing issues and PRs
- Read the documentation
- Ask in discussions
- Contact maintainers

## Code of Conduct

Please follow our code of conduct in all interactions.

## License

By contributing, you agree that your contributions will be licensed under the project's license.