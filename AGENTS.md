# AGENTS.md

This file provides essential guidance for agentic coding systems working in this repository.

## Build, Lint, Test Commands

### Development Dependencies
```bash
# Install with dev tools
uv pip install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests
python -m unittest discover tests/

# Run specific test suite
python -m unittest tests.unit.test_models
python -m unittest tests.integration.test_end_to_end
python -m unittest tests.performance.test_accuracy

# Run a specific test class
python -m unittest tests.unit.test_models.TestBenchmarkResult

# Run a single test method
python -m unittest tests.unit.test_models.TestBenchmarkResult.test_benchmark_result_creation
```

### Linting and Formatting
```bash
# Format code
black http_benchmark/ tests/

# Check for linting issues
flake8 http_benchmark/ tests/

# Type checking
mypy http_benchmark/
```

## Code Style Guidelines

### Import Organization
```python
# 1. Standard library imports
import time
import asyncio
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

# 2. Third-party imports
import requests
import httpx
from pydantic_settings import BaseSettings

# 3. Local imports
from .base import BaseHTTPAdapter
from ..models.http_request import HTTPRequest
from ..utils.logging import app_logger
```

### Naming Conventions
- **Classes**: PascalCase (e.g., `BenchmarkRunner`, `BaseHTTPAdapter`, `BenchmarkResult`)
- **Functions/Variables**: snake_case (e.g., `make_request`, `run_sync_benchmark`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `app_name`, `DEFAULT_CONCURRENCY`)
- **Private members**: Prefixed with underscore (e.g., `_run_sync_benchmark`)

### Type Hints
Always use type hints for function signatures and class attributes:
```python
def make_request(self, request: HTTPRequest) -> Dict[str, Any]:
    """Make an HTTP request and return response data."""
    pass

async def make_request_async(self, request: HTTPRequest) -> Dict[str, Any]:
    """Make an async HTTP request and return response data."""
    pass
```

### Docstrings
Every class and public method must have a docstring:
```python
class BenchmarkRunner:
    """Core benchmarking functionality for HTTP client performance testing."""

    def run(self) -> BenchmarkResult:
        """Run the benchmark with the given configuration."""
        pass
```

### Error Handling Pattern

**DO NOT raise exceptions for request failures.** Instead, return structured dictionaries:
```python
def make_request(self, request: HTTPRequest) -> Dict[str, Any]:
    try:
        # ... perform request ...
        return {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'content': response.text,
            'response_time': response.elapsed.total_seconds(),
            'url': str(response.url),
            'success': True,
            'error': None
        }
    except Exception as e:
        return {
            'status_code': None,
            'headers': {},
            'content': '',
            'response_time': 0,
            'url': request.url,
            'success': False,
            'error': str(e)
        }
```

**Logging**:
- Use `app_logger` from `utils.logging` (loguru-based)
- `INFO`: Benchmark lifecycle events (start/stop, results)
- `ERROR`: Request failures (throttled to prevent log flooding)
- Use throttled error logging in high-concurrency contexts: `if error_count <= 5: app_logger.error(...)`

### Base Classes

**Use ABC for abstract base classes**:
```python
from abc import ABC, abstractmethod

class BaseHTTPAdapter(ABC):
    """Base class for all HTTP client adapters."""

    @abstractmethod
    def make_request(self, request: HTTPRequest) -> Dict[str, Any]:
        """Make an HTTP request and return response data."""
        pass
```

**Inherit from BaseModel for data classes**:
```python
from .base import BaseModel

class BenchmarkResult(BaseModel):
    """Holds benchmark execution results."""
    # ... model implementation ...
```

### Configuration Management

**Use pydantic-settings for application settings**:
```python
from pydantic_settings import BaseSettings

class BenchmarkSettings(BaseSettings):
    """Settings for the benchmark framework."""
    default_concurrency: int = 10
    max_concurrency: int = 10000

    class Config:
        env_prefix = 'HTTP_BENCHMARK_'
        case_sensitive = False
```

**Environment variables**: Prefix with `HTTP_BENCHMARK_` (e.g., `HTTP_BENCHMARK_DEFAULT_CONCURRENCY=20`)

### Architecture Patterns

**Adapter Pattern**: All HTTP client adapters inherit from `BaseHTTPAdapter` and implement `make_request()` and `make_request_async()`

**Sync/Async Duality**: Support both synchronous and asynchronous execution paths. Provide fallback for sync-only libraries (like requests) in async methods.

**Resource Management**:
- Use `ThreadPoolExecutor` for sync concurrency
- Use `asyncio.create_task()` for async concurrency
- Maintain constant concurrency by replenishing tasks/futures as they complete

### Testing

Tests use `unittest` framework. Test files are organized under `tests/`:
- `tests/unit/`: Unit tests for individual components
- `tests/integration/`: Integration tests
- `tests/performance/`: Performance and accuracy tests

All test files should import from `http_benchmark` using absolute imports.

### Project Structure

```
http_benchmark/
├── cli/              # Command-line interface
├── clients/          # HTTP client adapters (adapter pattern)
├── models/           # Data models (with BaseModel)
├── utils/            # Shared utilities (logging, resource monitoring)
├── benchmark.py      # Core benchmark execution logic
├── config.py         # Application settings
└── storage.py        # SQLite result persistence
```

### Prohibited Practices

- **NEVER** use `as any`, `@ts-ignore`, or `@ts-expect-error` (not applicable to Python, but the principle stands: no type suppression)
- **NEVER** raise exceptions for request failures in adapters (return structured dicts instead)
- **NEVER** create empty catch blocks for exceptions during benchmark execution (even broad catches must handle or log)
- **NEVER** modify `.env` files in version control (they're in .gitignore)

### Important Notes

- Database files (`*.db`) are generated during runtime and should not be committed
- The project uses SQLite for result storage by default (`benchmark_results.db`)
- All benchmarks support concurrent execution with configurable concurrency levels
- Error logging is throttled in high-concurrency scenarios to prevent log flooding
