#!/bin/bash
# Semantic versioning with conventional commits

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

# Run version bump
uv run python scripts/bump-version.py $bump

# Commit changes
if git diff --quiet; then
    echo "ℹ️ No changes to commit"
else
    git add .
    git commit -m "chore: bump version ($bump)"
fi

echo "✅ Version bump complete!"