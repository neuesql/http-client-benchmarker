# HTTP Client Performance Benchmark Framework

A comprehensive Python framework for benchmarking HTTP client performance and resource usage across different libraries with detailed metrics and comparison capabilities.

## Features

- **Multi-library Support**: Benchmark multiple HTTP client libraries including requests, requestx, httpx, aiohttp, urllib3, and pycurl
- **Sync & Async Support**: Full support for both synchronous and asynchronous requests with performance comparison
- **Resource Monitoring**: Detailed monitoring of CPU, memory, and network usage during benchmarking
- **Flexible Configuration**: Configuration via pydantic-settings with environment variable support
- **Result Storage**: Persistent storage of benchmark results in SQLite with comparison capabilities
- **Command-Line Interface**: Full-featured CLI for easy benchmark execution and comparison
- **Comprehensive Metrics**: Detailed performance metrics including response times, throughput, error rates, and percentiles
- **Extensive Testing**: Complete test coverage with unit, integration, and performance tests

## Installation

```bash
# Using uv (recommended)
uv venv
uv pip install -e .

# Or using pip
pip install -e .
```

## Usage

### Command Line Interface

```bash
# Basic benchmark with specific client
python -m http_benchmark.cli.main --url https://httpbin.org/get --client httpx --concurrency 10 --duration 30

# Compare multiple clients
python -m http_benchmark.cli.main --url https://httpbin.org/get --compare requests httpx aiohttp --concurrency 5 --duration 20

# Advanced benchmark with custom parameters
python -m http_benchmark.cli.main --url https://api.example.com/data --client httpx --method POST --concurrency 20 --duration 60 --headers '{"Content-Type": "application/json"}'

# Async benchmarking
python -m http_benchmark.cli.main --url https://httpbin.org/get --client httpx --async --concurrency 10
```


```bash
# Basic benchmark with specific client
python -m http_benchmark.cli.main --url http://localhost/get --client httpx --concurrency 10 --duration 30

# Compare multiple clients
python -m http_benchmark.cli.main --url http://localhost/get --compare requests aiohttp pycurl urllib3 --concurrency 5 --duration 20

# Advanced benchmark with custom parameters
python -m http_benchmark.cli.main --url http://localhost/data --client httpx --method POST --concurrency 20 --duration 60 --headers '{"Content-Type": "application/json"}'

# Async benchmarking
python -m http_benchmark.cli.main --url http://localhost/get --client httpx --async --method GET --concurrency 10
```



### Python API

```python
from http_benchmark.benchmark import BenchmarkRunner
from http_benchmark.config import BenchmarkConfiguration

# Create a detailed configuration
config = BenchmarkConfiguration(
    target_url="https://httpbin.org/get",
    http_method="GET",
    headers={"User-Agent": "Benchmark-Client/1.0"},
    concurrency=10,
    duration_seconds=30,
    client_library="httpx",
    is_async=False,
    timeout=30
)

# Run the benchmark
runner = BenchmarkRunner(config)
result = runner.run()

# Access detailed metrics
print(f"Client Library: {result.client_library}")
print(f"Requests per second: {result.requests_per_second}")
print(f"Average response time: {result.avg_response_time:.3f}s")
print(f"95th percentile: {result.p95_response_time:.3f}s")
print(f"99th percentile: {result.p99_response_time:.3f}s")
print(f"Error rate: {result.error_rate:.2f}%")
print(f"CPU usage (avg): {result.cpu_usage_avg:.2f}%")
print(f"Memory usage (avg): {result.memory_usage_avg:.2f}MB")
```


### Result Storage and Comparison

```python
from http_benchmark.storage import ResultStorage

# Store results
storage = ResultStorage()
storage.save_result(result)

# Retrieve and compare results
all_results = storage.get_all_results()
comparison = storage.compare_results([result1.id, result2.id, result3.id])

for comparison_item in comparison:
    print(f"Client: {comparison_item['client_library']}")
    print(f"RPS: {comparison_item['requests_per_second']}")
    print(f"Avg Time: {comparison_item['avg_response_time']:.3f}s")
    print(f"CPU: {comparison_item['cpu_usage_avg']:.2f}%")
```

## Supported HTTP Client Libraries

- `requests` - Synchronous HTTP requests with extensive ecosystem
- `requestx` - Enhanced HTTP client with additional features and performance optimizations
- `httpx` - Modern HTTP client supporting both synchronous and asynchronous requests
- `aiohttp` - Asynchronous HTTP client built on asyncio
- `urllib3` - Low-level HTTP client with connection pooling and other advanced features
- `pycurl` - High-performance HTTP client based on libcurl

## Configuration Options

The framework uses pydantic-settings for configuration. You can configure via:

1. **Environment variables**: Prefix with `HTTP_BENCHMARK_`
   ```bash
   export HTTP_BENCHMARK_DEFAULT_CONCURRENCY=20
   export HTTP_BENCHMARK_MAX_CONCURRENCY=10000
   ```

2. **Configuration file**: Create a `.env` file with settings

3. **Code-based configuration**: Using the BenchmarkConfiguration class

### Available Configuration Settings

- `default_concurrency`: Default number of concurrent requests (default: 10)
- `default_duration_seconds`: Default benchmark duration (default: 30)
- `max_concurrency`: Maximum allowed concurrency (default: 10000)
- `resource_monitoring_interval`: Interval for resource monitoring (default: 0.1s)
- `sqlite_db_path`: Path to SQLite database (default: "benchmark_results.db")

## Metrics Collected

The framework collects comprehensive performance metrics:

- **Throughput**: Requests per second (RPS)
- **Response Times**: Average, minimum, maximum, 95th percentile, 99th percentile
- **Error Rates**: Percentage of failed requests
- **Resource Usage**: CPU, memory, and network I/O
- **HTTP Details**: Status codes, headers, response sizes

## Testing

The framework includes comprehensive test coverage:

```bash
# Run all tests
python -m unittest discover tests/

# Run specific test suites
python -m unittest tests.unit.test_models
python -m unittest tests.integration.test_end_to_end
python -m unittest tests.performance.test_accuracy
```

## Architecture

The framework follows a clean architecture with distinct layers:

- **Models**: Data models for benchmark results, configurations, and metrics
- **Clients**: Adapters for different HTTP client libraries
- **Benchmark**: Core benchmarking logic with sync/async support
- **Storage**: SQLite-based result storage and retrieval
- **CLI**: Command-line interface
- **Utils**: Utilities for logging, resource monitoring, and configuration

## License

MIT