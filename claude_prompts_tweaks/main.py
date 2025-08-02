"""Main CLI interface for claude-prompts-tweaks."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
@click.version_option()
def cli() -> None:
    """Claude Prompts Tweaks - Analyze and process Claude Code system prompts."""
    pass


@cli.command()
@click.argument('json_file', type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', type=click.Path(path_type=Path), help='Output file path')
@click.option('--format', 'output_format', type=click.Choice(['json', 'md', 'txt']), default='json', help='Output format')
def analyze(json_file: Path, output: Optional[Path], output_format: str) -> None:
    """Analyze Claude Code prompt JSON files."""
    console.print(f"[green]Analyzing {json_file}...[/green]")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Basic analysis
        stats = _analyze_prompts(data)
        _display_stats(stats)
        
        if output:
            _save_analysis(stats, output, output_format)
            console.print(f"[green]Analysis saved to {output}[/green]")
    
    except Exception as e:
        console.print(f"[red]Error analyzing file: {e}[/red]")


@cli.command()
@click.argument('json_file', type=click.Path(exists=True, path_type=Path))
@click.option('--pattern', '-p', help='Search pattern (regex supported)')
@click.option('--category', '-c', help='Filter by category')
def search(json_file: Path, pattern: Optional[str], category: Optional[str]) -> None:
    """Search through prompts for specific patterns or categories."""
    console.print(f"[green]Searching in {json_file}...[/green]")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = _search_prompts(data, pattern, category)
        _display_search_results(results)
    
    except Exception as e:
        console.print(f"[red]Error searching file: {e}[/red]")


@cli.command()
@click.argument('json_file', type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', type=click.Path(path_type=Path), help='Output markdown file')
def extract(json_file: Path, output: Optional[Path]) -> None:
    """Extract prompts to a readable markdown format."""
    console.print(f"[green]Extracting prompts from {json_file}...[/green]")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        markdown_content = _extract_to_markdown(data)
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            console.print(f"[green]Extracted to {output}[/green]")
        else:
            console.print(markdown_content)
    
    except Exception as e:
        console.print(f"[red]Error extracting prompts: {e}[/red]")


def _analyze_prompts(data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze prompt data and return statistics."""
    stats: Dict[str, Any] = {
        'total_categories': 0,
        'total_prompts': 0,
        'categories': {},
        'avg_prompt_length': 0.0,
        'longest_prompt': '',
        'shortest_prompt': ''
    }
    
    all_prompts: List[Any] = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                stats['categories'][key] = len(value)
                stats['total_categories'] += 1
                stats['total_prompts'] += len(value)
                all_prompts.extend(value)
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, list):
                        category_name = f"{key}.{subkey}"
                        stats['categories'][category_name] = len(subvalue)
                        stats['total_categories'] += 1
                        stats['total_prompts'] += len(subvalue)
                        all_prompts.extend(subvalue)
    
    if all_prompts:
        lengths = [len(str(prompt)) for prompt in all_prompts]
        stats['avg_prompt_length'] = sum(lengths) / len(lengths)
        
        longest_idx = lengths.index(max(lengths))
        shortest_idx = lengths.index(min(lengths))
        
        stats['longest_prompt'] = str(all_prompts[longest_idx])[:200] + "..." if len(str(all_prompts[longest_idx])) > 200 else str(all_prompts[longest_idx])
        stats['shortest_prompt'] = str(all_prompts[shortest_idx])[:200] + "..." if len(str(all_prompts[shortest_idx])) > 200 else str(all_prompts[shortest_idx])
    
    return stats


def _display_stats(stats: Dict[str, Any]) -> None:
    """Display analysis statistics in a formatted table."""
    table = Table(title="Prompt Analysis Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Total Categories", str(stats['total_categories']))
    table.add_row("Total Prompts", str(stats['total_prompts']))
    table.add_row("Average Prompt Length", f"{stats['avg_prompt_length']:.1f} chars")
    
    console.print(table)
    
    if stats['categories']:
        cat_table = Table(title="Categories Breakdown")
        cat_table.add_column("Category", style="cyan")
        cat_table.add_column("Count", style="green")
        
        for category, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True):
            cat_table.add_row(category, str(count))
        
        console.print(cat_table)


def _search_prompts(data: Dict[str, Any], pattern: Optional[str], category: Optional[str]) -> List[Dict[str, Any]]:
    """Search prompts based on pattern and category."""
    import re
    
    results: List[Dict[str, Any]] = []
    
    def search_in_list(prompts: List[Any], cat_name: str) -> None:
        for i, prompt in enumerate(prompts):
            prompt_str = str(prompt)
            if pattern and not re.search(pattern, prompt_str, re.IGNORECASE):
                continue
            if category and category.lower() not in cat_name.lower():
                continue
            
            results.append({
                'category': cat_name,
                'index': i,
                'prompt': prompt_str[:300] + "..." if len(prompt_str) > 300 else prompt_str
            })
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                search_in_list(value, key)
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, list):
                        search_in_list(subvalue, f"{key}.{subkey}")
    
    return results


def _display_search_results(results: List[Dict[str, Any]]) -> None:
    """Display search results."""
    if not results:
        console.print("[yellow]No results found.[/yellow]")
        return
    
    console.print(f"[green]Found {len(results)} results:[/green]")
    
    for result in results:
        console.print(f"\n[cyan]Category:[/cyan] {result['category']}")
        console.print(f"[cyan]Index:[/cyan] {result['index']}")
        console.print(f"[cyan]Prompt:[/cyan]")
        console.print(result['prompt'])
        console.print("-" * 80)


def _extract_to_markdown(data: Dict[str, Any]) -> str:
    """Extract prompts to markdown format."""
    markdown_lines = [
        "# Claude Code System Prompts",
        "",
        "Extracted prompts organized by category.",
        ""
    ]
    
    def process_prompts(prompts: List[Any], category_name: str, level: int = 2) -> None:
        markdown_lines.append(f"{'#' * level} {category_name}")
        markdown_lines.append("")
        
        for i, prompt in enumerate(prompts):
            markdown_lines.append(f"{i + 1}. {str(prompt)}")
            markdown_lines.append("")
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                process_prompts(value, key)
            elif isinstance(value, dict):
                markdown_lines.append(f"## {key}")
                markdown_lines.append("")
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, list):
                        process_prompts(subvalue, subkey, level=3)
    
    return "\n".join(markdown_lines)


def _save_analysis(stats: Dict[str, Any], output_path: Path, format: str) -> None:
    """Save analysis results to file."""
    if format == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
    elif format == 'md':
        content = _stats_to_markdown(stats)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    elif format == 'txt':
        content = _stats_to_text(stats)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)


def _stats_to_markdown(stats: Dict[str, Any]) -> str:
    """Convert stats to markdown format."""
    lines = [
        "# Prompt Analysis Results",
        "",
        f"- **Total Categories:** {stats['total_categories']}",
        f"- **Total Prompts:** {stats['total_prompts']}",
        f"- **Average Prompt Length:** {stats['avg_prompt_length']:.1f} characters",
        "",
        "## Categories Breakdown",
        ""
    ]
    
    for category, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"- **{category}:** {count} prompts")
    
    return "\n".join(lines)


def _stats_to_text(stats: Dict[str, Any]) -> str:
    """Convert stats to plain text format."""
    lines = [
        "PROMPT ANALYSIS RESULTS",
        "=" * 25,
        "",
        f"Total Categories: {stats['total_categories']}",
        f"Total Prompts: {stats['total_prompts']}",
        f"Average Prompt Length: {stats['avg_prompt_length']:.1f} characters",
        "",
        "CATEGORIES BREAKDOWN",
        "-" * 20
    ]
    
    for category, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"{category}: {count} prompts")
    
    return "\n".join(lines)


if __name__ == "__main__":
    cli()