#!/usr/bin/env python3
"""
Version management script for http-client-benchmarker
Usage: python scripts/bump-version.py [patch|minor|major|VERSION]
"""

import re
import sys
from pathlib import Path

def get_current_version():
    """Extract version string from __init__.py"""
    init_file = Path("http_benchmark/__init__.py")
    content = init_file.read_text()
    match = re.search(r'__version__ = ["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    raise ValueError("Could not find version in __init__.py")

def update_version_file(new_version):
    """Update version in __init__.py"""
    init_file = Path("http_benchmark/__init__.py")
    content = init_file.read_text()
    updated_content = re.sub(
        r'__version__ = ["\'][^"\']+["\']',
        f'__version__ = "{new_version}"',
        content
    )
    init_file.write_text(updated_content)

def update_pyproject_file(new_version):
    """Update version in pyproject.toml"""
    pyproject_file = Path("pyproject.toml")
    content = pyproject_file.read_text()
    updated_content = re.sub(
        r'version = ["\'][^"\']+["\']',
        f'version = "{new_version}"',
        content
    )
    pyproject_file.write_text(updated_content)

def calculate_new_version(current_version, bump_type):
    """Generate new version based on semantic versioning"""
    parts = [int(x) for x in current_version.split('.')]
    
    if bump_type == 'patch':
        parts[2] += 1
    elif bump_type == 'minor':
        parts[1] += 1
        parts[2] = 0
    elif bump_type == 'major':
        parts[0] += 1
        parts[1] = 0
        parts[2] = 0
    else:
        return bump_type
    
    return '.'.join(map(str, parts))

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/bump-version.py [patch|minor|major|VERSION]")
        sys.exit(1)
    
    bump_type = sys.argv[1]
    
    current_version = get_current_version()
    print(f"Current version: {current_version}")
    
    new_version = calculate_new_version(current_version, bump_type)
    
    if new_version == current_version:
        print(f"No version change for {bump_type}")
        sys.exit(1)
    
    print(f"New version: {new_version}")
    
    update_version_file(new_version)
    update_pyproject_file(new_version)
    
    print(f"✅ Version updated from {current_version} to {new_version}")
    
    import subprocess
    result = subprocess.run(["uv", "lock"], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ uv.lock regenerated")
    else:
        print("⚠️ Failed to regenerate uv.lock")
    
    print("\n📁 Adding files to git...")
    git_add_result = subprocess.run(["git", "add", "."], capture_output=True, text=True)
    if git_add_result.returncode == 0:
        print("✅ Files added to git")
    else:
        print(f"⚠️ Failed to add files: {git_add_result.stderr}")
        return
    
    print("\n📝 Committing changes...")
    commit_message = f"bump: version {current_version} → {new_version}"
    git_commit_result = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True)
    if git_commit_result.returncode == 0:
        print(f"✅ Changes committed: {commit_message}")
    else:
        print(f"⚠️ Failed to commit: {git_commit_result.stderr}")
        return
    
    print("\n🚀 Pushing to GitHub...")
    git_push_result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if git_push_result.returncode == 0:
        print("✅ Changes pushed to GitHub")
    else:
        print(f"⚠️ Failed to push: {git_push_result.stderr}")
        print("You may need to push manually: git push origin main")
    
    print(f"\n🎉 Version bump complete! Version is now {new_version}")

if __name__ == "__main__":
    main()