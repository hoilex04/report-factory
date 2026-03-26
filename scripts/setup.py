#!/usr/bin/env python3
"""
Interactive setup wizard for Report Factory.
"""

import json
import os
from pathlib import Path
from typing import Dict, List

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm

from .config import Config

console = Console()


def load_domain_packs() -> Dict:
    """Load pre-configured domain packs from config file."""
    pack_file = Path(__file__).parent.parent.parent / "config" / "domain-packs.json"

    if not pack_file.exists():
        return {}

    with open(pack_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get("packs", {})


def show_welcome():
    """Display welcome message."""
    console.print("""
[bold blue]╔═══════════════════════════════════════════════════════════╗[/]
[bold blue]║          Report Factory - Domain Setup Wizard            ║[/]
[bold blue]╚═══════════════════════════════════════════════════════════╝[/]

This wizard will help you configure your research domains.
You can choose a pre-configured pack or create custom domains.
""")


def show_domain_packs(packs: Dict) -> int:
    """Display available domain packs and get user choice."""
    console.print("[bold]Available Domain Packs:[/]\n")

    for i, (pack_id, pack) in enumerate(packs.items(), 1):
        console.print(f"[cyan]{i}[/]. [bold]{pack['name']}[/]")
        console.print(f"   {pack['description']}")
        console.print(f"   Domains: {', '.join(pack['domains'].keys())}\n")

    console.print("[yellow]4[/]. [bold]Custom Setup[/] - Define your own domains")

    while True:
        choice = Prompt.ask(
            "Which pack would you like",
            choices=["1", "2", "3", "4"],
            default="1"
        )
        return int(choice)


def select_pack(packs: Dict, choice: int) -> Dict:
    """Select a domain pack."""
    if choice == 4:
        return None  # Custom setup

    pack_keys = list(packs.keys())
    if 1 <= choice <= 3:
        pack_id = pack_keys[choice - 1]
        return packs[pack_id]

    return None


def customize_domain(code: str, domain: Dict) -> Dict:
    """Allow user to customize a domain."""
    console.print(f"\n[bold]Customizing: {domain['name']} ({code})[/]")
    console.print(f"Current keywords: {', '.join(domain['keywords'])}")

    if Confirm.ask("Add more keywords?", default=False):
        new_keywords = Prompt.ask("Enter additional keywords (comma-separated)")
        if new_keywords:
            additional = [k.strip() for k in new_keywords.split(",")]
            domain['keywords'].extend(additional)

    return domain


def setup_custom_domains() -> Dict:
    """Guide user through custom domain setup."""
    console.print("\n[bold]Custom Domain Setup[/]\n")

    domains = {}
    priority = []

    while True:
        name = Prompt.ask("Enter domain name (e.g., 'Quantum Computing')")
        code = Prompt.ask("Enter domain code (2-4 letters, e.g., 'QC')").upper()
        keywords = Prompt.ask("Enter keywords (comma-separated)")

        domains[code] = {
            "name": name,
            "keywords": [k.strip() for k in keywords.split(",")],
            "color": Prompt.ask("Color (hex)", default="#0066CC"),
            "metrics": []
        }
        priority.append(code)

        if not Confirm.ask("Add another domain?", default=True):
            break

    return {"domains": domains, "priority": priority}


def configure_paths(config: Config) -> None:
    """Configure output paths."""
    console.print("\n[bold]Path Configuration[/]\n")

    # Cards output directory
    cards_path = Prompt.ask(
        "Cards output directory",
        default=str(config.get_output_path())
    )
    config.set("paths", {
        "cards": cards_path,
        "index": Prompt.ask(
            "Master index file",
            default=str(config.get_index_path())
        )
    })

    # Create directory if needed
    Path(cards_path).mkdir(parents=True, exist_ok=True)


def show_summary(config: Config) -> None:
    """Show configuration summary."""
    console.print("\n[bold green]Configuration Summary[/]\n")

    table = Table(show_header=True)
    table.add_column("Domain", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Keywords", style="yellow")

    for code, domain in config.get("domains", {}).items():
        table.add_row(
            code,
            domain.get("name", ""),
            ", ".join(domain.get("keywords", [])[:5])
        )

    console.print(table)
    console.print(f"\nPriority order: {' > '.join(config.get_priority())}")


def main():
    """Main setup function."""
    show_welcome()

    config = Config()

    # Load existing config if present
    if config.load():
        console.print("[yellow]Existing configuration found.[/]")
        if not Confirm.ask("Overwrite?", default=False):
            console.print("Setup cancelled.")
            return

    # Load domain packs
    packs = load_domain_packs()

    # Get pack choice
    choice = show_domain_packs(packs)

    if choice == 4:
        # Custom setup
        result = setup_custom_domains()
        for code, domain in result["domains"].items():
            config.add_domain(code, domain["name"], domain["keywords"],
                            domain.get("color", "#0066CC"))
        config.set_priority(result["priority"])
    else:
        # Pack selection
        pack = select_pack(packs, choice)
        if pack:
            console.print(f"\n[green]Selected: {pack['name']}[/]")

            # Customize each domain
            for code, domain in pack["domains"].items():
                domain = customize_domain(code, domain)
                config.add_domain(code, domain["name"], domain["keywords"],
                                domain.get("color", "#0066CC"),
                                domain.get("metrics", []))

            config.set_priority(pack["priority"])

    # Configure paths
    configure_paths(config)

    # Show summary
    show_summary(config)

    # Save configuration
    if Confirm.ask("\nSave configuration?", default=True):
        if config.save():
            console.print("\n[bold green]✓ Configuration saved successfully![/]")
            console.print(f"  Location: {config.config_path}")
        else:
            console.print("\n[bold red]✗ Failed to save configuration.[/]")
    else:
        console.print("\n[yellow]Configuration not saved.[/]")


if __name__ == "__main__":
    main()
