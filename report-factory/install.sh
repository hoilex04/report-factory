#!/bin/bash
# Report Factory Quick Install Script

echo "📚 Report Factory - Quick Install"
echo "=================================="
echo ""

# Check if Claude Code is installed
if ! command -v claude &> /dev/null; then
    echo "⚠️  Claude Code not found. Please install it first:"
    echo "   https://claude.ai/code"
    exit 1
fi

# Determine OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    SKILLS_DIR="$HOME/.claude/skills"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    SKILLS_DIR="$HOME/.claude/skills"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    SKILLS_DIR="$USERPROFILE/.claude/skills"
else
    echo "⚠️  Unknown OS. Please manually copy to ~/.claude/skills/"
    exit 1
fi

# Create directory
mkdir -p "$SKILLS_DIR"

# Copy skill
echo "📁 Installing to: $SKILLS_DIR/report-factory"
cp -r . "$SKILLS_DIR/report-factory"

# Create config directory
mkdir -p "$HOME/.report-factory"

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Open Claude Code"
echo "2. Run: /setup-domains"
echo "3. Start processing: /process https://arxiv.org/abs/2602.xxxxx"
echo ""
echo "📖 Documentation: $SKILLS_DIR/report-factory/README.md"
echo ""
