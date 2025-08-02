# Contributing to Claude Prompts Tweaks

We welcome contributions to Claude Prompts Tweaks! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/claude-prompts-tweaks.git
   cd claude-prompts-tweaks
   ```

3. Install uv (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

4. Install development dependencies:
   ```bash
   make install-dev
   ```

## Development Workflow

### Before Starting Work

1. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Ensure pre-commit hooks are installed:
   ```bash
   uv run pre-commit install
   ```

### During Development

1. Write tests first (TDD approach)
2. Implement your changes
3. Run tests frequently:
   ```bash
   make test-fast
   ```

4. Format your code:
   ```bash
   make format
   ```

5. Check types:
   ```bash
   make type-check
   ```

### Before Submitting

1. Run the full test suite:
   ```bash
   make test
   ```

2. Ensure all checks pass:
   ```bash
   make lint
   make type-check
   ```

3. Update documentation if needed

## Code Standards

- **Black** for code formatting (88 character line length)
- **isort** for import sorting (Black profile)
- **mypy** for static type checking (strict mode)
- **pytest** for testing with minimum 90% coverage
- All code must have type annotations
- All public functions must have docstrings

## Pull Request Process

1. Ensure your branch is up to date with master
2. Push your changes and create a pull request
3. Ensure all CI checks pass
4. Request review from maintainers
5. Address any feedback

## Testing Guidelines

- Write tests using pytest
- Follow TDD principles
- Aim for 90%+ test coverage
- Include both unit and integration tests
- Use descriptive test names

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in present tense
- Keep the first line under 72 characters
- Reference issues when applicable

Example:
```
Add search functionality for prompt patterns

- Implement pattern matching with regex support
- Add category filtering option
- Include comprehensive tests

Fixes #123
```