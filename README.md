# Claude Prompts Tweaks

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

Built with:
- Python 3.12+
- Click for CLI interface
- Rich for beautiful terminal output
- Pydantic for data validation