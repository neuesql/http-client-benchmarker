# HTTP Client & Server Performance Benchmark Framework

Technical framework for benchmarking and comparing Python HTTP client library performance. Supports synchronous and asynchronous execution models, providing metrics for throughput, latency, and system resource utilization.

## 🌟 Motivation & Purpose

This framework helps developers test and evaluate HTTP clients and servers across different use cases including streaming, GET, POST, PUT, PATCH, DELETE operations. By providing comprehensive performance metrics with persistent storage, teams can make data-driven decisions to select the best HTTP client library or server configuration for their specific needs.

**Key Value**: Persistent results storage enables data-driven decisions for optimal performance.

## 🏗️ Architecture

The framework consists of a CLI/API entry point, an extensible adapter layer for HTTP clients, a resource monitoring system, and a persistence layer.

### System Flow

```text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLI/API       │    │   HTTP Client   │    │   Test Server   │
│   Benchmark     │───▶│   (requests/    │───▶│   (httpbin/     │
│   Config        │    │    httpx/etc)   │    │    traefik/     │
└─────────────────┘    └─────────────────┘    │    nginx)       │
                                 │            └─────────────────┘
                                 │                       │
                                 ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Console       │◀───│   Results       │◀───│   Performance   │
│   Output        │    │   Processing    │    │   Metrics       │
│                 │    │                 │    │   Collection    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
          │                       │
          │                       ▼
          │            ┌─────────────────┐
          └───────────▶│   SQLite DB     │
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

Select one of the following server configurations based on your testing requirements:

#### **Option 1: Simple HTTPBin (Single Instance)**
- **File**: `httpbin_server/docker-compose.httpbin.yml`
- **Features**: Single httpbin instance, HTTP only, minimal resource usage
- **Use case**: Basic testing, debugging, quick validation
- **Command**: `docker-compose -f httpbin_server/docker-compose.httpbin.yml up -d`
- **Endpoint**: `http://localhost/`

#### **Option 2: Traefik Load Balancer (3 Instances)**
- **File**: `httpbin_server/docker-compose.traefik.yml`
- **Features**: Traefik reverse proxy, 3 load-balanced httpbin instances, HTTP/HTTPS support
- **Use case**: Production-like load balancing, advanced routing, comprehensive benchmarking
- **Command**: `docker-compose -f httpbin_server/docker-compose.traefik.yml up -d`
- **Endpoints**: `http://localhost/` and `https://localhost/`

#### **Option 3: Nginx Load Balancer (3 Instances)**
- **File**: `httpbin_server/docker-compose.nginx.yml`
- **Features**: Nginx reverse proxy, 3 load-balanced httpbin instances, HTTP/HTTPS support without redirects
- **Use case**: High-performance load balancing, simple configuration, dual protocol support
- **Command**: `docker-compose -f httpbin_server/docker-compose.nginx.yml up -d`
- **Endpoints**: `http://localhost/` and `https://localhost/`

### 📊 Server Comparison

| Feature | Simple HTTPBin | Traefik | Nginx |
|:---|:---:|:---:|:---:|
| Instances | 1 | 3 | 3 |
| HTTP Support | ✅ | ✅ | ✅ |
| HTTPS Support | ❌ | ✅ | ✅ |
| Load Balancing | ❌ | ✅ | ✅ |
| Health Checks | ❌ | ✅ | ✅ |
| SSL/TLS Termination | ❌ | ✅ | ✅ |
| Configuration Complexity | Low | High | Medium |
| Resource Usage | Low | High | Medium |
| Best For | Quick tests | Production-like | High-performance |

### 🔍 Server Testing Examples

#### **Testing Simple HTTPBin:**
```bash
# Test HTTP endpoint
curl http://localhost/get

# Quick benchmark (1 second)
./.venv/bin/python -m http_benchmark.cli --url http://localhost/get --client requests --concurrency 1 --duration 1
```

#### **Testing Traefik Load Balancer:**
```bash
# Test HTTP endpoint
curl http://localhost/get

# Test HTTPS endpoint (self-signed cert)
curl -k https://localhost/get

# Quick benchmark with HTTP
./.venv/bin/python -m http_benchmark.cli --url http://localhost/get --client requests --concurrency 1 --duration 1

# Quick benchmark with HTTPS
./.venv/bin/python -m http_benchmark.cli --url https://localhost/get --client requests --concurrency 1 --duration 1
```

#### **Testing Nginx Load Balancer:**
```bash
# Test HTTP endpoint
curl http://localhost/get

# Test HTTPS endpoint (self-signed cert)
curl -k https://localhost/get

# Quick benchmark with HTTP
./.venv/bin/python -m http_benchmark.cli --url http://localhost/get --client httpx --concurrency 1 --duration 1

# Quick benchmark with HTTPS
./.venv/bin/python -m http_benchmark.cli --url https://localhost/get --client httpx --concurrency 1 --duration 1
```

### ▶️ 2. Execute Benchmark
Run a benchmark for a specific client:
```bash
python -m http_benchmark.cli --url http://localhost/get --client httpx --concurrency 20 --duration 30
```

Compare multiple clients:
```bash
python -m http_benchmark.cli --url http://localhost/get --compare requests httpx aiohttp --concurrency 10 --duration 10
```

### 🔗 Testing Different HTTP Methods
The framework supports all standard HTTP methods: GET, POST, PUT, PATCH, and DELETE.

#### Quick Tests (1 worker, 1 second)
```bash
# GET - Retrieve data
python -m http_benchmark.cli --url http://localhost/get --method GET --client requests --concurrency 1 --duration 1

# POST - Create resources
python -m http_benchmark.cli --url http://localhost/post --method POST --client requests --concurrency 1 --duration 1 --body '{"key": "value"}'

# PUT - Update resources
python -m http_benchmark.cli --url http://localhost/put --method PUT --client requests --concurrency 1 --duration 1 --body '{"updated": "data"}'

# PATCH - Partial updates
python -m http_benchmark.cli --url http://localhost/patch --method PATCH --client requests --concurrency 1 --duration 1 --body '{"patched": "value"}'

# DELETE - Remove resources
python -m http_benchmark.cli --url http://localhost/delete --method DELETE --client requests --concurrency 1 --duration 1
```

## 🎯 Use Cases

#### **Use Case 1: HTTP Client Selection**
Compare different HTTP client libraries (requests, httpx, aiohttp, etc.) to find the best performer for your application.

#### **Use Case 2: HTTP Method Optimization**
Test GET, POST, PUT, PATCH, DELETE methods to identify performance characteristics and optimize API interactions.

#### **Use Case 3: Server Configuration Comparison**
Evaluate different server setups (simple, load-balanced, nginx vs traefik) to optimize infrastructure.

#### **Use Case 4: Resource Usage Analysis**
Monitor CPU, memory, and network I/O to make informed decisions about resource allocation.

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
black http_benchmark/

# Linting
flake8 http_benchmark/ --max-line-length=250
```

## 🏗️ Architecture Details

### 🔌 Adapter Pattern
Standardizes interactions with diverse HTTP libraries. Each adapter implements a unified interface, decoupling the core `BenchmarkRunner` from library-specific implementations.

### 📊 Resource Monitoring
Background execution via `psutil` captures system metrics (CPU, Memory, Network I/O) without blocking primary benchmark operations.

### ⚡ Concurrency Management
Uses `ThreadPoolExecutor` for synchronous clients and `asyncio` tasks for asynchronous clients to maintain constant concurrency levels throughout the benchmark duration.
