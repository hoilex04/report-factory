"""
Command-line interface for Report Factory.
"""

import click
from rich.console import Console

from .config import Config
from .detector import DomainDetector

console = Console()


@click.group()
@click.version_option(version="2.0.0")
def main():
    """Report Factory - Universal Knowledge Card Generator

    Transform any technical content into standardized Obsidian cards.
    """
    pass


@main.command()
def setup():
    """Interactive domain setup wizard."""
    from .scripts import setup as setup_wizard
    setup_wizard.main()


@main.command()
@click.argument('url')
@click.option('--domain', '-d', help='Force specific domain code')
@click.option('--output', '-o', help='Output directory')
def process(url, domain, output):
    """Process a single article or paper.

    URL can be arXiv, WeChat, blog, or any web article.
    """
    config = Config()
    config.load()

    console.print(f"[blue]Processing:[/] {url}")

    # Domain detection
    if domain:
        console.print(f"[yellow]Forcing domain:[/] {domain}")
        detected_domain = domain
    else:
        detector = DomainDetector(config)
        # detected_domain = detector.detect(url)
        console.print("[yellow]Auto-detecting domain...[/]")

    console.print("[green]✓ Processing complete[/]")


@main.command()
@click.argument('source', type=click.Choice(['wechat', 'arxiv', 'inbox']))
@click.option('--days', '-d', default=7, help='Number of days to harvest')
@click.option('--limit', '-l', default=30, help='Max items to process')
def harvest(source, days, limit):
    """Batch harvest from RSS feeds.

    SOURCE: wechat, arxiv, or inbox
    """
    config = Config()
    config.load()

    console.print(f"[blue]Harvesting:[/] {source}")
    console.print(f"Days: {days}, Limit: {limit}")

    # Harvest logic would go here
    console.print("[green]✓ Harvest complete[/]")


@main.command()
@click.argument('topic')
@click.option('--depth', '-d', default=3, help='Analysis depth')
def analyze(topic, depth):
    """Deep analysis on a topic.

    TOPIC: Research question or topic to analyze
    """
    config = Config()
    config.load()

    console.print(f"[blue]Analyzing:[/] {topic}")
    console.print(f"Depth: {depth}")

    # Analysis logic would go here
    console.print("[green]✓ Analysis complete[/]")


@main.command()
def show_domains():
    """Show current domain configuration."""
    config = Config()
    config.load()

    domains = config.get("domains", {})

    if not domains:
        console.print("[yellow]No domains configured. Run 'rf setup' first.[/]")
        return

    console.print("[bold]Configured Domains:[/]\n")

    for code, domain in domains.items():
        console.print(f"[cyan]{code}[/] - {domain.get('name', 'Unknown')}")
        keywords = domain.get('keywords', [])
        console.print(f"   Keywords: {', '.join(keywords[:5])}")
        if len(keywords) > 5:
            console.print(f"   ... and {len(keywords) - 5} more")

    priority = config.get_priority()
    if priority:
        console.print(f"\n[bold]Priority:[/] {' > '.join(priority)}")


@main.command()
@click.argument('code')
@click.argument('keywords')
@click.option('--name', '-n', help='Domain name')
@click.option('--color', '-c', default='#0066CC', help='Domain color')
def add_domain(code, keywords, name, color):
    """Add a new domain.

    CODE: Domain code (e.g., 'QC' for Quantum Computing)

    KEYWORDS: Comma-separated keywords
    """
    config = Config()
    config.load()

    keyword_list = [k.strip() for k in keywords.split(",")]

    if not name:
        name = code.title()

    config.add_domain(code.upper(), name, keyword_list, color)
    config.save()

    console.print(f"[green]✓ Domain {code.upper()} added[/]")


@main.command()
@click.argument('code')
@click.option('--reassign', '-r', help='Reassign cards to this domain')
def remove_domain(code, reassign):
    """Remove a domain.

    CODE: Domain code to remove
    """
    config = Config()
    config.load()

    if config.remove_domain(code.upper()):
        config.save()
        console.print(f"[green]✓ Domain {code.upper()} removed[/]")
    else:
        console.print(f"[red]✗ Domain {code.upper()} not found[/]")


@main.command()
def validate():
    """Validate configuration."""
    config = Config()
    config.load()

    is_valid, errors = config.validate()

    if is_valid:
        console.print("[green]✓ Configuration is valid[/]")
    else:
        console.print("[red]✗ Configuration errors:[/]")
        for error in errors:
            console.print(f"  - {error}")


if __name__ == "__main__":
    main()
