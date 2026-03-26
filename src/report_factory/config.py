"""
Configuration handling for Report Factory.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional


class Config:
    """Manages user configuration for Report Factory."""

    DEFAULT_CONFIG_DIR = Path.home() / ".report-factory"
    CONFIG_FILE = "config.json"
    PATHS_FILE = "paths.json"

    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or self.DEFAULT_CONFIG_DIR
        self.config_path = self.config_dir / self.CONFIG_FILE
        self.paths_path = self.config_dir / self.PATHS_FILE

        # Default values
        self.defaults = {
            "version": "2.0-generic",
            "userId": "default",
            "domains": {},
            "priority": [],
            "autoHarvest": {
                "wechat": True,
                "arxiv": True,
                "blogs": False
            },
            "harvestDays": 7,
            "similarityThreshold": 0.85,
            "language": "en",
            "outputFormat": ["card", "canvas"],
            "paths": {
                "cards": str(Path.home() / "Cards"),
                "index": str(Path.home() / "master_index.json")
            }
        }

        self.config = self.defaults.copy()
        self.paths = {}

    def load(self) -> bool:
        """Load configuration from file."""
        if not self.config_path.exists():
            return False

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                self.config.update(loaded)
            return True
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config: {e}")
            return False

    def save(self) -> bool:
        """Save configuration to file."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error saving config: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.config[key] = value

    def get_domain(self, code: str) -> Optional[Dict]:
        """Get domain configuration by code."""
        domains = self.config.get("domains", {})
        return domains.get(code)

    def add_domain(self, code: str, name: str, keywords: List[str],
                   color: str = "#0066CC", metrics: Optional[List[str]] = None) -> None:
        """Add or update a domain."""
        if "domains" not in self.config:
            self.config["domains"] = {}

        self.config["domains"][code] = {
            "name": name,
            "keywords": keywords,
            "color": color,
            "metrics": metrics or []
        }

    def remove_domain(self, code: str) -> bool:
        """Remove a domain."""
        if code in self.config.get("domains", {}):
            del self.config["domains"][code]
            return True
        return False

    def get_priority(self) -> List[str]:
        """Get domain priority order."""
        return self.config.get("priority", [])

    def set_priority(self, priority: List[str]) -> None:
        """Set domain priority order."""
        self.config["priority"] = priority

    def get_output_path(self) -> Path:
        """Get cards output directory."""
        paths = self.config.get("paths", {})
        return Path(paths.get("cards", str(Path.home() / "Cards")))

    def get_index_path(self) -> Path:
        """Get master index path."""
        paths = self.config.get("paths", {})
        return Path(paths.get("index", str(Path.home() / "master_index.json")))

    def validate(self) -> tuple[bool, List[str]]:
        """Validate configuration.

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Check domains
        domains = self.config.get("domains", {})
        if not domains:
            errors.append("No domains configured. Run setup first.")

        for code, domain in domains.items():
            if not domain.get("keywords"):
                errors.append(f"Domain {code} has no keywords.")
            if not domain.get("name"):
                errors.append(f"Domain {code} has no name.")

        # Check priority
        priority = self.config.get("priority", [])
        if not priority and domains:
            errors.append("No domain priority set.")

        return (len(errors) == 0, errors)
