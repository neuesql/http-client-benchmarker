# ⚡ HTTP Client & Server Performance Benchmark Framework

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-performance technical framework for benchmarking and comparing Python HTTP client libraries. Make data-driven decisions with precision metrics on throughput, latency, and system resource utilization across both synchronous and asynchronous execution models.

---

## 🌟 Motivation & Purpose

**Stop guessing, start measuring.** 🚀

In the world of high-performance Python services, choosing the right HTTP client can be the difference between a snappy API and a bottleneck. This framework empowers developers to evaluate HTTP clients and servers under real-world conditions—streaming, heavy POST payloads, or rapid-fire GET requests.

**Key Value**: Persistent results storage in SQLite enables long-term trend analysis and objective, data-driven architecture decisions.

---

## 🏗️ Architecture

The framework is built with extensibility in mind, featuring a clean adapter layer for HTTP clients, a non-blocking resource monitoring system, and a robust persistence layer.

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

The framework measures response times, throughput (RPS), and resource usage (CPU/Memory) to help you find the sweet spot for your specific workload.

---

## 🚀 Installation

### 📋 Prerequisites
- **Python 3.12+**
- **Docker & Docker Compose** (for running the isolated test servers)

### 🔧 Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/http-client-benchmarker.git
   cd http-client-benchmarker
   ```

2. **Install dependencies** using `uv` (highly recommended for speed):
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   ```
   *Or using standard `pip`:*
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

---

## ⚡ Quick Start

### 🖥️ 1. Start your Test Server

Spin up an isolated environment to ensure benchmark consistency. Choose the one that matches your production target:

#### **Option 1: Simple HTTPBin (Low Overhead)**
*Perfect for quick debugging and validation.*
- **Features**: Single instance, HTTP-only, minimal resource footprint.
- **Command**: `docker-compose -f httpbin_server/docker-compose.httpbin.yml up -d`
- **Endpoint**: `http://localhost/`

#### **Option 2: Traefik Load Balancer (Production-Like)**
*Simulate a real-world distributed architecture.*
- **Features**: Traefik proxy, 3 load-balanced instances, HTTP/HTTPS support.
- **Command**: `docker-compose -f httpbin_server/docker-compose.traefik.yml up -d`
- **Endpoints**: `http://localhost/` and `https://localhost/`

#### **Option 3: Nginx Load Balancer (High Performance)**
*Test against the industry-standard reverse proxy.*
- **Features**: Nginx proxy, 3 load-balanced instances, dual protocol support.
- **Command**: `docker-compose -f httpbin_server/docker-compose.nginx.yml up -d`
- **Endpoints**: `http://localhost/` and `https://localhost/`

### 📊 Server Comparison Matrix

| Feature | Simple HTTPBin | Traefik | Nginx |
|:---|:---:|:---:|:---:|
| Instances | 1 | 3 | 3 |
| HTTP Support | ✅ | ✅ | ✅ |
| HTTPS Support | ❌ | ✅ | ✅ |
| Load Balancing | ❌ | ✅ | ✅ |
| Health Checks | ❌ | ✅ | ✅ |
| SSL/TLS Termination | ❌ | ✅ | ✅ |
| Complexity | Low | High | Medium |
| Resource Usage | Low | High | Medium |
| **Best For** | **Quick tests** | **Real-world simulation** | **Raw performance** |

### 🔍 Server Testing Examples

#### **Testing Simple HTTPBin:**
```bash
# Verify it's alive
curl http://localhost/get

# Quick benchmark (1 second, 1 worker)
./.venv/bin/python -m http_benchmark.cli --url http://localhost/get --client requests --concurrency 1 --duration 1
```

#### **Testing Traefik/Nginx Load Balancers:**
```bash
# Test HTTPS (ignore self-signed cert)
curl -k https://localhost/get

# Benchmark with HTTP
./.venv/bin/python -m http_benchmark.cli --url http://localhost/get --client requests --concurrency 1 --duration 1

# Benchmark with HTTPS
./.venv/bin/python -m http_benchmark.cli --url https://localhost/get --client requests --concurrency 1 --duration 1
```

---

### ▶️ 2. Execute Benchmark

Run a benchmark for a specific client:
```bash
./.venv/bin/python -m http_benchmark.cli --url http://localhost/get --client httpx --concurrency 20 --duration 30
```

**Compare multiple clients head-to-head**:
```bash
./.venv/bin/python -m http_benchmark.cli --url http://localhost/get --compare requests httpx aiohttp --concurrency 10 --duration 10
```

### 🔗 Testing Different HTTP Methods

The framework supports the full RESTful spectrum:

```bash
# GET - The baseline
./.venv/bin/python -m http_benchmark.cli --url http://localhost/get --method GET --client requests --concurrency 1 --duration 1

# POST - Measure payload handling
./.venv/bin/python -m http_benchmark.cli --url http://localhost/post --method POST --client requests --concurrency 1 --duration 1 --body '{"key": "value"}'

# PUT - Full updates
./.venv/bin/python -m http_benchmark.cli --url http://localhost/put --method PUT --client requests --concurrency 1 --duration 1 --body '{"updated": "data"}'

# PATCH - Partial updates
./.venv/bin/python -m http_benchmark.cli --url http://localhost/patch --method PATCH --client requests --concurrency 1 --duration 1 --body '{"patched": "value"}'

# DELETE - Cleanup performance
./.venv/bin/python -m http_benchmark.cli --url http://localhost/delete --method DELETE --client requests --concurrency 1 --duration 1
```

---

## 🎯 Use Cases

*   **Client Selection**: Is `httpx` worth the switch from `requests` for your specific API? Find out.
*   **Method Optimization**: Identify if your `POST` endpoints are significantly slower than `GET` under load.
*   **Infrastructure Tuning**: Compare `Nginx` vs `Traefik` overhead in your local environment.
*   **Resource Profiling**: Track how much Memory/CPU each client library consumes at 10k concurrency.

---

## 🔧 Client Support

| Library | Sync | Async | Key Characteristics |
|:---|:---:|:---:|:---|
| `aiohttp` | ❌ | ✅ | 🎯 Non-blocking I/O, optimized for async services |
| `httpx` | ✅ | ✅ | 🎯 HTTP/2 support, requests-compatible API |
| `pycurl` | ✅ | ❌ | 🎯 libcurl bindings, minimal overhead |
| `requests` | ✅ | ❌ | 🎯 Standard synchronous client, blocking I/O |
| `requestx` | ✅ | ✅ | 🎯 Performance-optimized dual-mode client |
| `urllib3` | ✅ | ❌ | 🎯 Thread-safe connection pooling, low-level |

---

## ⚙️ Configuration

Tweak the framework via environment variables (prefixed with `HTTP_BENCHMARK_`).

| 📊 Environment Variable | Default | Description |
|:---|:---|:---|
| `HTTP_BENCHMARK_DEFAULT_CONCURRENCY` | `10` | Default concurrent workers |
| `HTTP_BENCHMARK_DEFAULT_DURATION_SECONDS` | `30` | Default benchmark duration (seconds) |
| `HTTP_BENCHMARK_MAX_CONCURRENCY` | `10000` | Safety limit for concurrency |
| `HTTP_BENCHMARK_SQLITE_DB_PATH` | `benchmark_results.db` | SQLite storage path |
| `HTTP_BENCHMARK_RESOURCE_MONITORING_INTERVAL` | `0.1` | Metrics polling interval (seconds) |

---

## 💾 Database Schema

Results are persisted in the `benchmark_results` table for easy analysis.

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

### 🔍 Analysis Example (SQL)
```sql
-- Compare performance across all clients
SELECT 
    client_library, 
    AVG(requests_per_second) as avg_rps, 
    AVG(avg_response_time) * 1000 as avg_latency_ms 
FROM benchmark_results 
GROUP BY client_library
ORDER BY avg_rps DESC;
```

---

## 🧪 Development

### ✅ Testing
Keep the core stable with our comprehensive test suite:
```bash
# Unit tests
./.venv/bin/python -m unittest discover tests/unit

# Integration tests
./.venv/bin/python -m unittest discover tests/integration

# Performance tests
./.venv/bin/python -m unittest discover tests/performance
```

### 🎨 Linting & Formatting
```bash
# Code formatting
black http_benchmark/

# Linting
flake8 http_benchmark/ --max-line-length=250
```

---

## 🏗️ Architecture Details

### 🔌 Adapter Pattern
We decouple the core engine from the libraries. Each client has its own adapter implementing a unified interface, making it easy to add your own custom client.

### 📊 Resource Monitoring
A background thread uses `psutil` to sample system metrics (CPU, Memory, I/O) at high frequency without interfering with the benchmark itself.

### ⚡ Concurrency Management
High-efficiency execution:
- **Sync Clients**: Managed via a tuned `ThreadPoolExecutor`.
- **Async Clients**: Powered by native `asyncio` task management.
