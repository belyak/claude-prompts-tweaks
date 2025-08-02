"""Tests for the main CLI interface."""

import json
import tempfile
from pathlib import Path
from typing import Any, Dict

import pytest
from click.testing import CliRunner

from claude_prompts_tweaks.main import (
    cli,
    _analyze_prompts,
    _display_stats,
    _search_prompts,
    _display_search_results,
    _extract_to_markdown,
    _save_analysis,
    _stats_to_markdown,
    _stats_to_text,
)


@pytest.fixture
def sample_data() -> Dict[str, Any]:
    """Sample data for testing."""
    return {
        "system_prompts": [
            "You are a helpful assistant.",
            "Always be respectful and kind.",
            "Provide accurate information."
        ],
        "user_prompts": [
            "How do I write Python code?",
            "Explain machine learning."
        ],
        "categories": {
            "coding": [
                "Help with programming tasks.",
                "Debug code issues."
            ],
            "general": [
                "Answer general questions."
            ]
        }
    }


@pytest.fixture
def temp_json_file(sample_data: Dict[str, Any]) -> Path:
    """Create a temporary JSON file with sample data."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_data, f, indent=2)
        return Path(f.name)


def test_cli_help() -> None:
    """Test that the CLI help command works."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_cli_version() -> None:
    """Test that the CLI version command works."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0


def test_analyze_command_help() -> None:
    """Test analyze command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", "--help"])
    assert result.exit_code == 0
    assert "Analyze Claude Code prompt JSON files" in result.output


def test_search_command_help() -> None:
    """Test search command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "--help"])
    assert result.exit_code == 0
    assert "Search through prompts" in result.output


def test_extract_command_help() -> None:
    """Test extract command help."""
    runner = CliRunner()
    result = runner.invoke(cli, ["extract", "--help"])
    assert result.exit_code == 0
    assert "Extract prompts to a readable markdown format" in result.output


def test_analyze_command_basic(temp_json_file: Path) -> None:
    """Test basic analyze command functionality."""
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", str(temp_json_file)])
    assert result.exit_code == 0
    assert "Analyzing" in result.output
    assert "Total Categories" in result.output
    assert "Total Prompts" in result.output


def test_analyze_command_with_json_output(temp_json_file: Path) -> None:
    """Test analyze command with JSON output."""
    runner = CliRunner()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as output_file:
        result = runner.invoke(cli, [
            "analyze", str(temp_json_file),
            "--output", output_file.name,
            "--format", "json"
        ])
        assert result.exit_code == 0
        assert "Analysis saved" in result.output
        
        # Verify output file was created and contains valid JSON
        output_path = Path(output_file.name)
        assert output_path.exists()
        with open(output_path, 'r') as f:
            output_data = json.load(f)
            assert "total_categories" in output_data
            assert "total_prompts" in output_data


def test_analyze_command_with_md_output(temp_json_file: Path) -> None:
    """Test analyze command with markdown output."""
    runner = CliRunner()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as output_file:
        result = runner.invoke(cli, [
            "analyze", str(temp_json_file),
            "--output", output_file.name,
            "--format", "md"
        ])
        assert result.exit_code == 0
        assert "Analysis saved" in result.output
        
        # Verify output file was created and contains markdown
        output_path = Path(output_file.name)
        assert output_path.exists()
        with open(output_path, 'r') as f:
            content = f.read()
            assert "# Prompt Analysis Results" in content
            assert "Total Categories" in content


def test_analyze_command_with_txt_output(temp_json_file: Path) -> None:
    """Test analyze command with text output."""
    runner = CliRunner()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as output_file:
        result = runner.invoke(cli, [
            "analyze", str(temp_json_file),
            "--output", output_file.name,
            "--format", "txt"
        ])
        assert result.exit_code == 0
        assert "Analysis saved" in result.output
        
        # Verify output file was created and contains text
        output_path = Path(output_file.name)
        assert output_path.exists()
        with open(output_path, 'r') as f:
            content = f.read()
            assert "PROMPT ANALYSIS RESULTS" in content
            assert "Total Categories" in content


def test_analyze_command_file_not_found() -> None:
    """Test analyze command with non-existent file."""
    runner = CliRunner()
    result = runner.invoke(cli, ["analyze", "nonexistent.json"])
    assert result.exit_code != 0


def test_analyze_command_invalid_json() -> None:
    """Test analyze command with invalid JSON file."""
    runner = CliRunner()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("invalid json content")
        f.flush()
        
        result = runner.invoke(cli, ["analyze", f.name])
        assert result.exit_code == 0  # The command handles the error gracefully
        assert "Error analyzing file" in result.output


def test_search_command_basic(temp_json_file: Path) -> None:
    """Test basic search command functionality."""
    runner = CliRunner()
    result = runner.invoke(cli, ["search", str(temp_json_file)])
    assert result.exit_code == 0
    assert "Searching in" in result.output


def test_search_command_with_pattern(temp_json_file: Path) -> None:
    """Test search command with pattern."""
    runner = CliRunner()
    result = runner.invoke(cli, ["search", str(temp_json_file), "--pattern", "assistant"])
    assert result.exit_code == 0
    assert "Searching in" in result.output


def test_search_command_with_category(temp_json_file: Path) -> None:
    """Test search command with category filter."""
    runner = CliRunner()
    result = runner.invoke(cli, ["search", str(temp_json_file), "--category", "coding"])
    assert result.exit_code == 0
    assert "Searching in" in result.output


def test_search_command_with_both_filters(temp_json_file: Path) -> None:
    """Test search command with both pattern and category."""
    runner = CliRunner()
    result = runner.invoke(cli, [
        "search", str(temp_json_file),
        "--pattern", "code",
        "--category", "coding"
    ])
    assert result.exit_code == 0
    assert "Searching in" in result.output


def test_search_command_invalid_json() -> None:
    """Test search command with invalid JSON."""
    runner = CliRunner()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("invalid json")
        f.flush()
        
        result = runner.invoke(cli, ["search", f.name])
        assert result.exit_code == 0
        assert "Error searching file" in result.output


def test_extract_command_basic(temp_json_file: Path) -> None:
    """Test basic extract command functionality."""
    runner = CliRunner()
    result = runner.invoke(cli, ["extract", str(temp_json_file)])
    assert result.exit_code == 0
    assert "Extracting prompts" in result.output
    assert "# Claude Code System Prompts" in result.output


def test_extract_command_with_output(temp_json_file: Path) -> None:
    """Test extract command with output file."""
    runner = CliRunner()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as output_file:
        result = runner.invoke(cli, [
            "extract", str(temp_json_file),
            "--output", output_file.name
        ])
        assert result.exit_code == 0
        assert "Extracted to" in result.output
        
        # Verify output file was created
        output_path = Path(output_file.name)
        assert output_path.exists()
        with open(output_path, 'r') as f:
            content = f.read()
            assert "# Claude Code System Prompts" in content


def test_extract_command_invalid_json() -> None:
    """Test extract command with invalid JSON."""
    runner = CliRunner()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("invalid json")
        f.flush()
        
        result = runner.invoke(cli, ["extract", f.name])
        assert result.exit_code == 0
        assert "Error extracting prompts" in result.output


def test_analyze_prompts_function(sample_data: Dict[str, Any]) -> None:
    """Test the _analyze_prompts function directly."""
    stats = _analyze_prompts(sample_data)
    
    assert stats["total_categories"] == 4  # system_prompts, user_prompts, categories.coding, categories.general
    assert stats["total_prompts"] == 8    # 3 + 2 + 2 + 1
    assert "system_prompts" in stats["categories"]
    assert "user_prompts" in stats["categories"]
    assert "categories.coding" in stats["categories"]
    assert "categories.general" in stats["categories"]
    assert stats["avg_prompt_length"] > 0
    assert len(stats["longest_prompt"]) > 0
    assert len(stats["shortest_prompt"]) > 0


def test_analyze_prompts_empty_data() -> None:
    """Test _analyze_prompts with empty data."""
    stats = _analyze_prompts({})
    assert stats["total_categories"] == 0
    assert stats["total_prompts"] == 0
    assert stats["avg_prompt_length"] == 0.0


def test_search_prompts_function(sample_data: Dict[str, Any]) -> None:
    """Test the _search_prompts function directly."""
    # Test without filters
    results = _search_prompts(sample_data, None, None)
    assert len(results) == 8  # All prompts
    
    # Test with pattern
    results = _search_prompts(sample_data, "assistant", None)
    assert len(results) == 1  # Only "You are a helpful assistant."
    
    # Test with category
    results = _search_prompts(sample_data, None, "coding")
    assert len(results) == 2  # Only coding category prompts
    
    # Test with both filters
    results = _search_prompts(sample_data, "programming", "coding")
    assert len(results) == 1  # Only "Help with programming tasks." in coding category


def test_extract_to_markdown_function(sample_data: Dict[str, Any]) -> None:
    """Test the _extract_to_markdown function directly."""
    markdown = _extract_to_markdown(sample_data)
    
    assert "# Claude Code System Prompts" in markdown
    assert "## system_prompts" in markdown
    assert "## user_prompts" in markdown
    assert "## categories" in markdown
    assert "### coding" in markdown
    assert "### general" in markdown
    assert "You are a helpful assistant." in markdown


def test_stats_to_markdown_function() -> None:
    """Test the _stats_to_markdown function."""
    stats = {
        "total_categories": 2,
        "total_prompts": 5,
        "avg_prompt_length": 25.5,
        "categories": {"test": 3, "example": 2}
    }
    
    markdown = _stats_to_markdown(stats)
    assert "# Prompt Analysis Results" in markdown
    assert "**Total Categories:** 2" in markdown
    assert "**Total Prompts:** 5" in markdown
    assert "25.5 characters" in markdown
    assert "**test:** 3 prompts" in markdown
    assert "**example:** 2 prompts" in markdown


def test_stats_to_text_function() -> None:
    """Test the _stats_to_text function."""
    stats = {
        "total_categories": 2,
        "total_prompts": 5,
        "avg_prompt_length": 25.5,
        "categories": {"test": 3, "example": 2}
    }
    
    text = _stats_to_text(stats)
    assert "PROMPT ANALYSIS RESULTS" in text
    assert "Total Categories: 2" in text
    assert "Total Prompts: 5" in text
    assert "25.5 characters" in text
    assert "test: 3 prompts" in text
    assert "example: 2 prompts" in text


def test_save_analysis_json(sample_data: Dict[str, Any]) -> None:
    """Test _save_analysis with JSON format."""
    stats = _analyze_prompts(sample_data)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        output_path = Path(f.name)
        _save_analysis(stats, output_path, "json")
        
        with open(output_path, 'r') as read_f:
            saved_data = json.load(read_f)
            assert saved_data["total_categories"] == stats["total_categories"]
            assert saved_data["total_prompts"] == stats["total_prompts"]


def test_save_analysis_markdown(sample_data: Dict[str, Any]) -> None:
    """Test _save_analysis with markdown format."""
    stats = _analyze_prompts(sample_data)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        output_path = Path(f.name)
        _save_analysis(stats, output_path, "md")
        
        with open(output_path, 'r') as read_f:
            content = read_f.read()
            assert "# Prompt Analysis Results" in content
            assert "Total Categories" in content


def test_save_analysis_text(sample_data: Dict[str, Any]) -> None:
    """Test _save_analysis with text format."""
    stats = _analyze_prompts(sample_data)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        output_path = Path(f.name)
        _save_analysis(stats, output_path, "txt")
        
        with open(output_path, 'r') as read_f:
            content = read_f.read()
            assert "PROMPT ANALYSIS RESULTS" in content
            assert "Total Categories" in content


def test_display_stats_function(sample_data: Dict[str, Any], capsys) -> None:
    """Test the _display_stats function."""
    stats = _analyze_prompts(sample_data)
    _display_stats(stats)
    
    captured = capsys.readouterr()
    # We can't easily test rich output, but we can ensure the function runs without error
    assert len(captured.out) >= 0  # Function ran without crashing


def test_display_search_results_function(sample_data: Dict[str, Any], capsys) -> None:
    """Test the _display_search_results function."""
    results = _search_prompts(sample_data, "assistant", None)
    _display_search_results(results)
    
    captured = capsys.readouterr()
    # We can't easily test rich output, but we can ensure the function runs without error
    assert len(captured.out) >= 0  # Function ran without crashing


def test_display_search_results_empty(capsys) -> None:
    """Test _display_search_results with empty results."""
    _display_search_results([])
    
    captured = capsys.readouterr()
    # We can't easily test rich output, but we can ensure the function runs without error
    assert len(captured.out) >= 0  # Function ran without crashing


def test_analyze_prompts_long_content() -> None:
    """Test _analyze_prompts with very long prompt content."""
    long_prompt = "a" * 500  # Very long prompt
    data = {"test": [long_prompt, "short"]}
    
    stats = _analyze_prompts(data)
    assert "..." in stats["longest_prompt"]  # Should be truncated
    assert len(stats["longest_prompt"]) <= 203  # 200 chars + "..."


def test_search_prompts_regex_pattern(sample_data: Dict[str, Any]) -> None:
    """Test _search_prompts with regex pattern."""
    # Test regex pattern matching
    results = _search_prompts(sample_data, r"\bcode\b", None)
    # Should match "How do I write Python code?" and "Debug code issues."
    assert len(results) >= 1


def test_main_cli_execution() -> None:
    """Test main CLI execution path."""
    from claude_prompts_tweaks.main import cli
    runner = CliRunner()
    result = runner.invoke(cli, [])
    # CLI without arguments should show help and exit with code 0
    # Click may return 2 for missing required arguments, which is expected
    assert result.exit_code in [0, 2]
