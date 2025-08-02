"""Tests for the main CLI interface."""

from click.testing import CliRunner

from claude_prompts_tweaks.main import cli


def test_cli_help() -> None:
    """Test that the CLI help command works."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
