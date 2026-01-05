# Quickstart Guide: HTTP Client Performance Benchmark Framework

## Overview
This guide provides a quick introduction to setting up and using the HTTP Client Performance Benchmark Framework.

## Prerequisites
- Python 3.12
- uv package manager
- Access to target HTTP endpoints for benchmarking

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd http-client-benchmarker
```

2. Install dependencies using uv:
```bash
uv venv
uv pip install -r requirements.txt
# or if using pyproject.toml
uv pip install -e .
```

## Basic Usage

### 1. Simple Benchmark
Run a basic benchmark against a target URL:

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

### 2. Using Decorators
Apply benchmarking to existing code with decorators:

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

### 3. Async Benchmarking
Run benchmarks with async clients:

```python
import asyncio
from http_benchmark.benchmark import AsyncBenchmarkRunner
from http_benchmark.config import BenchmarkConfiguration

async def run_async_benchmark():
    config = BenchmarkConfiguration(
        target_url="https://httpbin.org/get",
        http_method="GET",
        concurrency=20,
        total_requests=1000,
        client_library="aiohttp",
        is_async=True
    )
    
    runner = AsyncBenchmarkRunner(config)
    result = await runner.run()
    
    print(f"Async benchmark result: {result.requests_per_second} RPS")

asyncio.run(run_async_benchmark())
```

### 4. Configuration Options
Create detailed benchmark configurations:

```python
from http_benchmark.config import BenchmarkConfiguration

config = BenchmarkConfiguration(
    name="API Performance Test",
    target_url="https://api.example.com/data",
    http_method="POST",
    headers={"Content-Type": "application/json", "Authorization": "Bearer token"},
    body='{"query": "test"}',
    concurrency=50,
    duration_seconds=60,
    client_library="httpx",
    timeout=10,
    retry_attempts=2
)
```

### 5. Storing Results
Save benchmark results to SQLite:

```python
from http_benchmark.storage import ResultStorage
from http_benchmark.benchmark import BenchmarkRunner

# Run benchmark
config = BenchmarkConfiguration(target_url="https://httpbin.org/get", ...)
runner = BenchmarkRunner(config)
result = runner.run()

# Store result
storage = ResultStorage()
storage.save_result(result)

# Retrieve and compare results
previous_results = storage.get_results_by_name("API Performance Test")
```

## Available HTTP Client Libraries
The framework supports the following HTTP client libraries:
- `requests` - Synchronous HTTP requests
- `requestx` - Enhanced HTTP client with additional features
- `httpx` - Both synchronous and asynchronous requests
- `aiohttp` - Asynchronous HTTP requests
- `urllib3` - Low-level HTTP client
- `pycurl` - High-performance HTTP client

## Command Line Interface
The framework also provides a command-line interface:

```bash
# Basic benchmark
python -m http_benchmark.cli --url https://httpbin.org/get --client requests --concurrency 10

# With configuration file
python -m http_benchmark.cli --config benchmark_config.json

# Compare multiple clients
python -m http_benchmark.cli --compare requests httpx aiohttp --url https://httpbin.org/get
```

## Configuration File Format
You can also define benchmarks using JSON configuration files:

```json
{
  "name": "Production API Test",
  "target_url": "https://api.example.com/v1/users",
  "http_method": "GET",
  "headers": {
    "Authorization": "Bearer your-token-here"
  },
  "concurrency": 25,
  "duration_seconds": 120,
  "client_library": "httpx",
  "timeout": 15
}
```

## Next Steps
- Review the API reference documentation
- Explore advanced configuration options
- Set up integration tests with your specific endpoints
- Configure monitoring for resource usage metrics