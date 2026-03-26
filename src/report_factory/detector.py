"""
Domain detection for Report Factory.
"""

from typing import Dict, List, Optional, Tuple
from .config import Config


class DomainDetector:
    """Detects domain based on content keywords."""

    def __init__(self, config: Config):
        self.config = config
        self.domains = config.get("domains", {})
        self.priority = config.get_priority()

    def detect(self, text: str) -> Optional[str]:
        """Detect domain from text content.

        Args:
            text: Content text to analyze

        Returns:
            Domain code or None if no match
        """
        text_lower = text.lower()

        # Count keyword matches per domain
        matches: Dict[str, int] = {}

        for code, domain in self.domains.items():
            keywords = domain.get("keywords", [])
            count = sum(1 for kw in keywords if kw.lower() in text_lower)
            if count > 0:
                matches[code] = count

        if not matches:
            return None

        # If multiple domains match, use priority order
        if len(matches) > 1 and self.priority:
            for code in self.priority:
                if code in matches:
                    return code
            # Return highest match count if priority doesn't help
            return max(matches, key=matches.get)

        # Return highest match count
        return max(matches, key=matches.get)

    def detect_with_scores(self, text: str) -> List[Tuple[str, int]]:
        """Detect domain with match scores.

        Args:
            text: Content text to analyze

        Returns:
            List of (domain_code, score) tuples sorted by score
        """
        text_lower = text.lower()
        scores: List[Tuple[str, int]] = []

        for code, domain in self.domains.items():
            keywords = domain.get("keywords", [])
            score = sum(1 for kw in keywords if kw.lower() in text_lower)
            if score > 0:
                scores.append((code, score))

        return sorted(scores, key=lambda x: x[1], reverse=True)

    def get_domain_color(self, code: str) -> str:
        """Get color for domain."""
        domain = self.domains.get(code, {})
        return domain.get("color", "#808080")

    def get_domain_name(self, code: str) -> str:
        """Get display name for domain."""
        domain = self.domains.get(code, {})
        return domain.get("name", code)
