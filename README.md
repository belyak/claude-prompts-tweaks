# Claude Prompts Tweaks

[![CI](https://github.com/belyak/claude-prompts-tweaks/actions/workflows/ci.yml/badge.svg)](https://github.com/belyak/claude-prompts-tweaks/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

A CLI utility for analyzing and processing Claude Code system prompts and instructions.

## Features

- **Analyze**: Get comprehensive statistics about prompt JSON files
- **Search**: Find specific patterns or categories within prompts  
- **Extract**: Convert prompt data to readable markdown format

## Installation

This tool uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install dependencies
uv sync

# Run the CLI
uv run claude-prompts-tweaks --help
```

## Usage

### Analyze prompts
```bash
uv run claude-prompts-tweaks analyze claude_prompts_tweaks/data/claude_system_prompts.json
```

### Search for specific patterns
```bash
# Search for "todo" patterns
uv run claude-prompts-tweaks search claude_prompts_tweaks/data/claude_system_prompts.json --pattern "todo"

# Search within specific categories
uv run claude-prompts-tweaks search claude_prompts_tweaks/data/claude_system_prompts.json --category "tool_instructions"
```

### Extract to markdown
```bash
uv run claude-prompts-tweaks extract claude_prompts_tweaks/data/claude_system_prompts.json -o prompts.md
```

## Data Files

The utility comes with pre-loaded Claude Code prompt research files:

- `claude_system_prompts.json` - Categorized system prompts extracted from Claude Code binary
- `claude_prompts.json` - Raw prompt collection 
- `claude_prompts_summary.md` - Human-readable summary of all prompts

## Development

### Quick Start

```bash
# Clone the repository
git clone https://github.com/belyak/claude-prompts-tweaks.git
cd claude-prompts-tweaks

# Install development dependencies
make install-dev

# Run tests
make test

# Format code
make format

# Run all quality checks
make lint type-check test
```

### Tools and Standards

- **Python 3.12+** with full type annotations
- **uv** for dependency management
- **Black** for code formatting (88 char line length)
- **isort** for import sorting
- **mypy** for static type checking (strict mode)
- **pytest** for testing with 90%+ coverage requirement
- **pre-commit** hooks for automated quality checks

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

This project is open source. Please check the repository for license details.