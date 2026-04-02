# Contribution Guidelines

Thank you for your interest in contributing to Report Factory!

## How to Contribute

### Reporting Bugs

1. Check if the issue already exists
2. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Claude Code version)

### Suggesting Features

1. Open a feature request issue
2. Describe the use case
3. Explain why it benefits the community

### Submitting Changes

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/your-feature`
3. **Make changes** following our guidelines
4. **Test** your changes
5. **Submit a pull request**

## Development Guidelines

### Code Style

- Follow existing patterns
- Keep changes minimal and focused
- Document new commands in `docs/api.md`

### Documentation

- Update `README.md` if adding major features
- Add examples to `examples/` directory
- Update API docs for new commands

### Testing

- Test with sample articles
- Verify card generation works
- Check Obsidian compatibility

## Domain Packs

### Submitting a New Domain Pack

1. Define domains with:
   - Code (3-4 uppercase letters)
   - Name (human-readable)
   - Keywords (8-12 terms)
   - Color (hex code)
   - Default metrics

2. Example submission:
```json
{
  "code": "QUANT",
  "name": "Quantum Computing",
  "keywords": ["Qubit", "Quantum Gate", "Superposition", "Entanglement"],
  "color": "#9933CC",
  "metrics": ["qubit_count", "coherence_time", "gate_fidelity"]
}
```

3. Include:
   - Sample cards generated with the pack
   - Use case description
   - Keywords rationale

## Pull Request Process

1. Update documentation
2. Add test cases if applicable
3. Ensure no breaking changes (or document them)
4. Request review from maintainers

## Code of Conduct

- Be respectful and constructive
- Focus on the problem, not the person
- Welcome newcomers
- Help others learn

## Questions?

- Open a discussion for general questions
- Join our community chat (if available)
- Check existing documentation first

Thank you for contributing!
