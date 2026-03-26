"""
Report Factory - Main Package
"""

__version__ = "2.0.0"
__author__ = "Report Factory Contributors"

from .config import Config
from .detector import DomainDetector
from .fetcher import ContentFetcher
from .extractor import DataExtractor
from .validator import QualityValidator
from .exporter import CanvasExporter, PPTExporter

__all__ = [
    "Config",
    "DomainDetector",
    "ContentFetcher",
    "DataExtractor",
    "QualityValidator",
    "CanvasExporter",
    "PPTExporter",
]
