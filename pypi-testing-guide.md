# PyPI Publishing Testing Guide

## 🧪 Local Testing Steps

### Step 1: Build Package
```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build package
uv build

# Check what was built
ls -la dist/
```

### Step 2: Test Local Installation
```bash
# Install locally
uv pip install dist/http_client_benchmarker-0.1.0-py3-none-any.whl

# Test import
uv run python -c "from http_benchmark import __version__; print(f'Version: {__version__}')"

# Test CLI
uv run http-benchmark --help
```

## 🚀 PyPI Publishing Commands

### Option 1: Test PyPI (Recommended First)
```bash
# Publish to Test PyPI (use test.pypi.org)
uv publish --token "your-test-pypi-token" --index https://test.pypi.org/simple/ dist/

# Install from Test PyPI to verify
uv pip install --index-url https://test.pypi.org/simple/ http-client-benchmarker
```

### Option 2: Production PyPI
```bash
# Publish to Production PyPI (requires PYPI_TOKEN environment variable)
export PYPI_TOKEN="your-pypi-token"
uv publish --token "$PYPI_TOKEN" dist/http_client_benchmarker-*.tar.gz dist/http_client_benchmarker-*.whl

# Or use the secret directly in GitHub Actions:
# UV_PUBLISH_TOKEN: ${{ secrets.PYPI_TOKEN }}
```

## 🔐 Getting PyPI Tokens

### 1. PyPI Account Setup
1. Create account at https://pypi.org/
2. Go to Account Settings → API Tokens
3. Create new token with "Entire account" scope

### 2. Test PyPI Account Setup
1. Create account at https://test.pypi.org/
2. Go to Account Settings → API Tokens
3. Create new token with "Entire account" scope

### 3. Local Token Management
```bash
# Set token as environment variable
export PYPI_TOKEN="pypi-xxxxx"

# Or create ~/.pypirc file
cat > ~/.pypirc << EOF
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = your-pypi-token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = your-test-pypi-token
EOF
```

## ✅ Verification Steps

### After Publishing
1. **Check PyPI**: Visit https://pypi.org/project/http-client-benchmarker/
2. **Check Test PyPI**: Visit https://test.pypi.org/project/http-client-benchmarker/
3. **Install and test**: `pip install http-client-benchmarker`
4. **Verify CLI**: `http-benchmark --help`

### Expected Output After Successful Publish
- Package appears on PyPI website
- `pip install http-client-benchmarker` works
- `http-benchmark --help` shows help
- Import works: `from http_benchmark import BenchmarkRunner`

## 🔄 CI/CD Integration

The GitHub Actions workflow will handle this automatically:
1. Build package: `uv build`
2. Publish to PyPI: `uv publish --token "$UV_PUBLISH_TOKEN" dist/http_client_benchmarker-*.tar.gz dist/http_client_benchmarker-*.whl`
3. Create GitHub release with artifacts

Manual triggers available in GitHub Actions → "Release to PyPI and GitHub"

## 🐛 Troubleshooting

### Common Issues
1. **Token not working**: Check token scope and expiration
2. **Package name exists**: PyPI requires unique package names
3. **Version conflicts**: Update version in pyproject.toml
4. **Build fails**: Check dependencies and imports

### Debug Commands
```bash
# Check package contents
uv run python -m zipfile -l dist/http_client_benchmarker-*.whl

# Test import manually
uv run python -c "
import sys
sys.path.insert(0, '.')
from http_benchmark import BenchmarkRunner
print('✅ Import successful')
"

# Check entry points
uv run python -c "
from pkg_resources import get_distribution
dist = get_distribution('http-client-benchmarker')
print(f'Entry points: {list(dist.get_entry_map().keys())}')
"