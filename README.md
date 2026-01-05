# HTTP Client Performance Benchmark Framework

A Python framework for benchmarking HTTP client performance and resource usage across different libraries.

## Features

- Benchmark multiple HTTP client libraries: requests, requestx, httpx, aiohttp, urllib3, pycurl
- Support for both synchronous and asynchronous requests
- Resource usage monitoring (CPU, memory, network)
- Configuration via pydantic-settings
- Results storage and comparison using SQLite
- Decorator-based benchmarking for existing code
- Command-line interface for easy benchmarking

## Installation

```bash
# Using uv (recommended)
uv venv
uv pip install -e .

# Or using pip
pip install -e .
```

## Usage

### Command Line

```bash
# Basic benchmark
python -m http_benchmark.cli.main --url https://httpbin.org/get --client requests --concurrency 10

# Compare multiple clients
python -m http_benchmark.cli.main --url https://httpbin.org/get --compare requests httpx aiohttp --concurrency 5
```

### Python API

```python
from http_benchmark.benchmark import BenchmarkRunner
from http_benchmark.config import BenchmarkConfiguration

# Create a configuration
config = BenchmarkConfiguration(
    target_url="https://httpbin.org/get",
    http_method="GET",
    concurrency=10,
    duration_seconds=30,
    client_library="requests"
)

# Run the benchmark
runner = BenchmarkRunner(config)
result = runner.run()

print(f"Average response time: {result.avg_response_time}ms")
print(f"Requests per second: {result.requests_per_second}")
```

### Using Decorators

```python
from http_benchmark.decorators import benchmark

@benchmark(client_library="httpx", concurrency=5)
def my_http_call():
    import httpx
    response = httpx.get("https://httpbin.org/get")
    return response.json()

result = my_http_call()
print(f"Benchmark completed with {result.requests_per_second} RPS")
```

## Supported HTTP Client Libraries

- `requests` - Synchronous HTTP requests
- `requestx` - Enhanced HTTP client with additional features
- `httpx` - Both synchronous and asynchronous requests
- `aiohttp` - Asynchronous HTTP requests
- `urllib3` - Low-level HTTP client
- `pycurl` - High-performance HTTP client

## Configuration

The framework uses pydantic-settings for configuration. You can set environment variables prefixed with `HTTP_BENCHMARK_` to customize behavior.

## License

MIT