# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

HTTP Client & Server Performance Benchmark Framework - A Python 3.12+ tool for benchmarking HTTP client libraries (requests, httpx, aiohttp, urllib3, pycurl, requestx) against various server configurations (HTTPBin, Traefik, Nginx).

## Build & Development Commands

```bash
# Install dependencies (uv recommended)
uv pip install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"
```

## Testing

```bash
# Run all tests
python -m unittest discover tests/

# Run specific test suites
python -m unittest discover tests/unit
python -m unittest discover tests/integration
python -m unittest discover tests/performance

# Run specific test class
python -m unittest tests.unit.test_models.TestBenchmarkResult

# Run single test method
python -m unittest tests.unit.test_models.TestBenchmarkResult.test_benchmark_result_creation
```

## Code Quality

```bash
# Format code (line length: 200)
black http_benchmark/ tests/ --line-length 200

# Lint (line length: 200)
flake8 http_benchmark/ tests/ --max-line-length=200

# Type checking (optional - disabled in CI)
mypy http_benchmark/
```

## Running Benchmarks

```bash
# Start test server (choose one)
docker-compose -f httpbin_server/docker-compose.httpbin.yml up -d   # Simple
docker-compose -f httpbin_server/docker-compose.traefik.yml up -d   # With LB
docker-compose -f httpbin_server/docker-compose.nginx.yml up -d     # Nginx LB

# Single client benchmark
python -m http_benchmark.cli --url http://localhost/get --client httpx --concurrency 5 --duration 2

# Compare multiple clients
python -m http_benchmark.cli --url http://localhost/get --compare requests httpx aiohttp --concurrency 5 --duration 2
```

## Architecture

```
CLI (cli.py) → BenchmarkRunner (benchmark.py) → HTTP Client Adapters (clients/)
                      ↓                                    ↓
              ResourceMonitor (utils/)            ThreadPoolExecutor (sync)
                      ↓                           asyncio.create_task (async)
              Results Aggregation → SQLite Persistence (storage.py)
```

**Key patterns:**
- **Adapter Pattern**: All HTTP clients inherit from `BaseHTTPAdapter` in `clients/base.py`
- **Sync/Async duality**: Framework supports both execution modes
- **Background monitoring**: `ResourceMonitor` samples CPU/memory via psutil without affecting benchmarks

## Key Directories

- `http_benchmark/clients/` - HTTP client adapters (requests, httpx, aiohttp, urllib3, pycurl, requestx)
- `http_benchmark/models/` - Data models (BenchmarkConfiguration, BenchmarkResult, HTTPRequest)
- `http_benchmark/utils/` - Logging (loguru) and resource monitoring (psutil)
- `httpbin_server/` - Docker Compose configs for test servers

## Code Style

- **Line length**: 200 characters (enforced in CI)
- **Type hints**: Required on all function signatures
- **Imports**: stdlib → third-party → local
- **Logging**: Use `app_logger` from `utils.logging`

## Error Handling in Adapters

**Never raise exceptions for HTTP request failures.** Return structured dicts:

```python
return {
    'status_code': response.status_code,  # or None on failure
    'headers': dict(response.headers),
    'content': response.text,
    'response_time': elapsed_seconds,
    'url': str(response.url),
    'success': True,  # or False
    'error': None  # or error message string
}
```

## Supported Clients

| Library | Sync | Async |
|---------|------|-------|
| requests | ✅ | ❌ |
| httpx | ✅ | ✅ |
| aiohttp | ❌ | ✅ |
| urllib3 | ✅ | ❌ |
| pycurl | ✅ | ❌ |
| requestx | ✅ | ✅ |

## Database

Results persist to SQLite (`benchmark_results.db`, auto-created). Schema auto-manages via `ResultStorage`.
