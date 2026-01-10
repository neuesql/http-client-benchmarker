# HTTP Client Performance Benchmark Framework

Technical framework for benchmarking and comparing Python HTTP client library performance. Supports synchronous and asynchronous execution models, providing metrics for throughput, latency, and system resource utilization.

## 🏗️ Architecture

The framework consists of a CLI/API entry point, an extensible adapter layer for HTTP clients, a resource monitoring system, and a persistence layer.

### System Flow

```text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLI/API       │    │   HTTP Client   │    │   HTTP Server   │
│   Benchmark     │───▶│   (requests/    │───▶│   (httpbin)     │
│   Config        │    │    httpx/etc)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                │                       │
                                ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Console       │◀───│   Results       │◀───│   Response      │
│   Output        │    │   Processing    │    │   Collection    │
│                 │    │   (RPS, Latency│    │                 │
└─────────────────┘    │   Error Rate)   │    └─────────────────┘
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   SQLite DB     │
                       │   Storage       │
                       └─────────────────┘
```

The benchmark framework compares HTTP client performance by measuring response times, throughput, and resource usage to help choose optimal client libraries.

## 🚀 Installation

### 📋 Prerequisites
- Python 3.12+
- Docker and Docker Compose (for test server)

### 🔧 Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/http-client-benchmarker.git
   cd http-client-benchmarker
   ```

2. Install dependencies using `uv` (recommended):
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   ```
   Or using `pip`:
   ```bash
   pip install -e ".[dev]"
   ```

## ⚡ Quick Start

### 🖥️ 1. Start Test Server
Select a server configuration:
- **Load Balanced (Recommended)**: Traefik + 3 httpbin instances
  ```bash
  docker-compose -f httpbin_server/docker-compose.yml up -d
  ```
- **Simple**: Single httpbin instance
  ```bash
  docker-compose -f httpbin_server/docker-compose.simple.yml up -d
  ```

### ▶️ 2. Execute Benchmark
Run a benchmark for a specific client:
```bash
python -m http_benchmark.cli.main --url http://localhost/get --client httpx --concurrency 20 --duration 30
```

Compare multiple clients:
```bash
python -m http_benchmark.cli.main --url http://localhost/get --compare requests httpx aiohttp --concurrency 10 --duration 10
```

## 🔧 Client Support

| Library | Sync | Async | Key Characteristics |
|:---|:---:|:---:|:---|
| `aiohttp` | ❌ | ✅ | 🎯 Non-blocking I/O, optimized for async services |
| `httpx` | ✅ | ✅ | 🎯 HTTP/2 support, requests-compatible API |
| `pycurl` | ✅ | ❌ | 🎯 libcurl bindings, minimal overhead |
| `requests` | ✅ | ❌ | 🎯 Standard synchronous client, blocking I/O |
| `requestx` | ✅ | ✅ | 🎯 Performance-optimized dual-mode client |
| `urllib3` | ✅ | ❌ | 🎯 Thread-safe connection pooling, low-level |

## ⚙️ Configuration

Configuration is managed via `pydantic-settings`. Environment variables use the `HTTP_BENCHMARK_` prefix.

| 📊 Environment Variable | Default | Description |
|:---|:---|:---|
| `HTTP_BENCHMARK_DEFAULT_CONCURRENCY` | `10` | Default concurrent workers |
| `HTTP_BENCHMARK_DEFAULT_DURATION_SECONDS` | `30` | Default benchmark duration (seconds) |
| `HTTP_BENCHMARK_MAX_CONCURRENCY` | `10000` | Safety limit for concurrency |
| `HTTP_BENCHMARK_SQLITE_DB_PATH` | `benchmark_results.db` | SQLite storage path |
| `HTTP_BENCHMARK_RESOURCE_MONITORING_INTERVAL` | `0.1` | Metrics polling interval (seconds) |

## 💾 Database Schema

Results are persisted in the `benchmark_results` table.

### 📋 Table Structure

| Field | Type | Description |
|:---|:---|:---|
| `id` | TEXT | Primary key (UUID) |
| `name` | TEXT | Benchmark run identifier |
| `client_library` | TEXT | Library name (e.g., "httpx") |
| `client_type` | TEXT | Execution model ("sync" or "async") |
| `http_method` | TEXT | HTTP method utilized |
| `url` | TEXT | Target URL |
| `start_time` | TEXT | Start timestamp (ISO) |
| `end_time` | TEXT | End timestamp (ISO) |
| `duration` | REAL | Total execution time (seconds) |
| `requests_count` | INTEGER | Total requests completed |
| `requests_per_second` | REAL | Average throughput |
| `avg_response_time` | REAL | Mean latency (seconds) |
| `p95_response_time` | REAL | 95th percentile latency |
| `p99_response_time` | REAL | 99th percentile latency |
| `cpu_usage_avg` | REAL | Average CPU usage (%) |
| `memory_usage_avg` | REAL | Average RSS memory (MB) |
| `error_count` | INTEGER | Total failed requests |
| `error_rate` | REAL | Failure percentage |
| `concurrency_level` | INTEGER | Configured concurrency |
| `config_snapshot` | TEXT | JSON snapshot of configuration |
| `created_at` | TEXT | Record creation timestamp |

### 🔍 Sample Queries
```sql
-- Get average RPS and latency per client library
SELECT 
    client_library, 
    AVG(requests_per_second) as avg_rps, 
    AVG(avg_response_time) * 1000 as avg_latency_ms 
FROM benchmark_results 
GROUP BY client_library;
```

## 🧪 Development

### ✅ Testing
Execute the following commands to run the test suites:
```bash
# Unit tests
python -m unittest discover tests/unit

# Integration tests
python -m unittest discover tests/integration

# Performance tests
python -m unittest discover tests/performance
```

### 🎨 Linting and Formatting
```bash
# Code formatting
black http_benchmark/ tests/

# Linting
flake8 http_benchmark/ tests/
```

## 🏗️ Architecture Details

### 🔌 Adapter Pattern
Standardizes interactions with diverse HTTP libraries. Each adapter implements a unified interface, decoupling the core `BenchmarkRunner` from library-specific implementations.

### 📊 Resource Monitoring
Background execution via `psutil` captures system metrics (CPU, Memory, Network I/O) without blocking primary benchmark operations.

### ⚡ Concurrency Management
Uses `ThreadPoolExecutor` for synchronous clients and `asyncio` tasks for asynchronous clients to maintain constant concurrency levels throughout the benchmark duration.
