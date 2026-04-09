# Changelog

All notable changes to Report Factory will be documented in this file.

## [2.0.0] - 2026-03-26

### Added
- Generic domain support - define your own research domains
- Auto domain detection based on keywords
- 7-point quality gate validation
- Deduplication with similarity matching (85% threshold)
- PPT export (McKinsey-style presentations)
- Canvas visualization (Obsidian Canvas format)
- RSS integration (WeChat, arXiv, blog dashboard)
- Arguments card type for trend analysis
- Evidence card type for technical data
- Batch harvest mode
- Research/analysis mode

### Changed
- Complete rewrite from domain-specific to generic
- New UID format: DOMAIN-E/A-YYYYMMDD-NN
- Improved card templates with callouts
- Standardized filename convention
- Enhanced tag validation

### Removed
- Legacy domain-specific hardcoding
- Old card formats

## [1.0.0] - 2026-02-09

### Added
- Initial release
- Basic card generation
- Domain classification (EAI, AIH, MM, COG, AGT)
- Evidence extraction
- Master index tracking

---

## Version Format

- `MAJOR`: Breaking changes
- `MINOR`: New features, backwards compatible
- `PATCH`: Bug fixes
