#!/bin/bash
case "${1:-patch}" in
    patch)
        bump="patch"
        ;;
    minor)
        bump="minor"
        ;;
    major)
        bump="major"
        ;;
    *)
        echo "Usage: $0 [patch|minor|major]"
        exit 1
        ;;
esac

echo "🔄 Bumping $bump version..."

uv run python scripts/bump-version.py $bump