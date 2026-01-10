# ⚡ HTTP Client & Server Performance Benchmark Framework

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Introduction

**Stop guessing. Start measuring.** 🎯 Engineering decisions should be backed by hard data, not hunches. Make data-driven choices for your HTTP stack with precision, high-concurrency benchmarking.

In the high-stakes world of performance-critical services, your choice of HTTP client, server infrastructure, and request handling isn't just a detail—it's the backbone of your application's scalability. This framework eliminates the guesswork by providing comprehensive, real-world benchmarks across your entire HTTP ecosystem.

### 🎯 Why This Framework?

Most benchmarking tools focus on either just the client or just the server. We take a holistic, **multi-dimensional approach** to help you optimize the three critical pillars of your HTTP infrastructure:

#### 🔧 **1. HTTP Client Selection** — *Choose Your Weapon*
Find the perfect library for your specific workload. Compare the battle-tested `requests`, the modern `httpx`, or the high-performance `aiohttp` and `pycurl`. Get the numbers, not the hype.

**Available Arsenal:**
- 🐍 **`requests`** — The battle-tested industry standard
- ⚡ **`httpx`** — Modern, feature-rich HTTP/1.1 & HTTP/2 with sync/async flexibility
- 🌊 **`aiohttp`** — The high-performance async engine for non-blocking I/O
- 🔗 **`pycurl`** — Blazing fast C-level bindings via libcurl
- 🚄 **`requestx`** — Performance-tuned dual-mode execution
- 🔌 **`urllib3`** — Rock-solid connection pooling at the core

#### 🏗️ **2. Server Infrastructure** — *Build Your Battlefield*
Don't test in a vacuum. Benchmark against production-grade environments. Compare how different reverse proxies and load balancers handle the heat.

**Battlefield Scenarios:**
- 🎈 **Simple HTTPBin** — Lightning-fast validation with a lightweight instance
- 🎪 **Traefik Load Balancer** — Modern, cloud-native proxying across triple backend instances
- 🚀 **Nginx Load Balancer** — Battle-hardened, high-throughput reverse proxy simulation

#### 📮 **3. HTTP Methods** — *Test What Matters*
Performance isn't uniform. A GET request behaves differently than a heavy POST. Benchmark the exact operations your users actually perform with **full support for the entire HTTP method specification.**

---

### 💎 Key Features

✅ **Infinite Combinations** — Mix and match any client, server, and method for 360° coverage  
✅ **Granular Telemetry** — Track throughput (RPS), p95/p99 latency, and real-time CPU/Memory usage  
✅ **Long-term Analysis** — Built-in SQLite persistence for historical trend tracking and regression testing  
✅ **Production Parity** — Fully supports HTTPS, load balancers, and multi-instance topologies  
✅ **Stealth Monitoring** — Background resource sampling ensures zero interference with benchmark accuracy  
✅ **Developer First** — Modular adapter pattern makes adding custom clients a breeze  

---

### 🎬 Quick Example

Run a head-to-head comparison between top libraries using high-concurrency POST requests against an Nginx-backed cluster:

```bash
python -m http_benchmark.cli \
  --url https://localhost/post \
  --method POST \
  --body '{"test": "data"}' \
  --compare requests httpx aiohttp \
  --concurrency 5 \
  --duration 1
```

**The Result?** Cold, hard facts delivered straight to your console. End the architecture debates and start building on a foundation of measured performance.

---

## 🗺️ Architecture

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
│   Console       │◀────│   Results       │◀────│   Performance   │
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

**Data Flow:**
1. **Configure**: Define client, server, method, and concurrency parameters.
2. **Execute**: Launch high-frequency requests while monitoring system resources in the background.
3. **Analyze**: Aggregate performance metrics including throughput and latency percentiles.
4. **Persist**: Store detailed results in SQLite for historical analysis.
5. **Report**: Visualize comparative data directly in your terminal.

---

## 🚀 Installation

### 📋 Prerequisites
- **Python 3.12+**
- **Docker & Docker Compose** (for running isolated test servers)

### 🔧 Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/http-client-benchmarker.git
   cd http-client-benchmarker
   ```

2. **Install dependencies** using `uv` (recommended for speed):
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e ".[dev]"
   ```
   
   *Or using standard `pip`:*
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

---

## ⚡ Quick Start

### 🖥️ Step 1: Launch Your Test Server

Choose a server configuration that mirrors your production environment:

```bash
# Option 1: Simple HTTPBin (single instance, HTTP only)
docker-compose -f httpbin_server/docker-compose.httpbin.yml up -d

# Option 2: Traefik Load Balancer (3 instances, HTTP/HTTPS, cloud-native)
docker-compose -f httpbin_server/docker-compose.traefik.yml up -d

# Option 3: Nginx Load Balancer (3 instances, HTTP/HTTPS, high performance)
docker-compose -f httpbin_server/docker-compose.nginx.yml up -d
```

#### 📊 Server Comparison Matrix

| Feature | 🎈 Simple HTTPBin | 🎪 Traefik | 🚀 Nginx |
|:---|:---:|:---:|:---:|
| **Backend Instances** | 1 | 3 | 3 |
| **HTTP Support** | ✅ | ✅ | ✅ |
| **HTTPS Support** | ❌ | ✅ | ✅ |
| **Load Balancing** | ❌ | ✅ | ✅ |
| **Resource Overhead** | Low | High | Medium |
| **Best For** | **Quick tests** | **Real-world simulation** | **Raw performance** |

---

### ▶️ Step 2: Run Your Benchmark

#### 🖥️ Using CLI

**Single Client Benchmark:**
```bash
python -m http_benchmark.cli \
  --url http://localhost/get \
  --client httpx \
  --concurrency 5 \
  --duration 2
```

**Head-to-Head Comparison:**
```bash
python -m http_benchmark.cli \
  --url http://localhost/get \
  --compare requests httpx aiohttp \
  --concurrency 5 \
  --duration 2
```

**Different HTTP Methods:**
```bash
# POST with payload
python -m http_benchmark.cli --url http://localhost/post --method POST --body '{"user": "test"}' --client httpx --concurrency 1 --duration 1

# PUT, PATCH, DELETE
python -m http_benchmark.cli --url http://localhost/put --method PUT --client aiohttp --concurrency 1 --duration 1
```

---

#### 🐍 Using Python Library

The framework can be used programmatically as a Python library for fine-grained control and integration into your own testing infrastructure.

**Basic Usage:**

```python
from http_benchmark.benchmark import BenchmarkRunner
from http_benchmark.models.benchmark_configuration import BenchmarkConfiguration
from http_benchmark.storage import ResultStorage

# Configure your benchmark
config = BenchmarkConfiguration(
    target_url="http://localhost/get",
    http_method="GET",
    concurrency=10,
    duration_seconds=30,
    client_library="requests",
    is_async=False,
    verify_ssl=False,
    timeout=30,
)

# Run the benchmark
runner = BenchmarkRunner(config)
result = runner.run()

# Access results
print(f"RPS: {result.requests_per_second:.2f}")
print(f"Avg Latency: {result.avg_response_time * 1000:.2f}ms")
print(f"P95 Latency: {result.p95_response_time * 1000:.2f}ms")

# Persist results
storage = ResultStorage()
storage.save_result(result)
```

**Compare Multiple Clients:**

```python
# Compare multiple HTTP clients
clients = ["requests", "httpx", "aiohttp", "urllib3", "pycurl", "requestx"]
results = {}

for client in clients:
    is_async = client in ("aiohttp", "requestx-async")
    actual_client = client.replace("-async", "")
    
    config = BenchmarkConfiguration(
        target_url="http://localhost/get",
        http_method="GET",
        concurrency=5,
        duration_seconds=10,
        client_library=actual_client,
        is_async=is_async,
    )
    
    runner = BenchmarkRunner(config)
    result = runner.run()
    results[client] = result
    
    print(f"{client}: {result.requests_per_second:.2f} RPS")

# Find the fastest
best = max(results.items(), key=lambda x: x[1].requests_per_second)
print(f"\nFastest: {best[0]} ({best[1].requests_per_second:.2f} RPS)")
```

**Async Usage:**

```python
# For async clients (aiohttp, httpx with is_async=True)
config = BenchmarkConfiguration(
    target_url="http://localhost/get",
    http_method="GET",
    concurrency=100,
    duration_seconds=30,
    client_library="aiohttp",
    is_async=True,
)

runner = BenchmarkRunner(config)
result = runner.run()
print(f"Async RPS: {result.requests_per_second:.2f}")
```

---

## 🎯 Use Cases

### 🔍 Client Selection & Migration
**Scenario:** Your team is considering migrating from `requests` to `httpx` to leverage HTTP/2.  
**Solution:** Run a 60-second high-concurrency comparison to quantify RPS, latency, and resource usage.

### 📈 Method-Specific Optimization
**Scenario:** Your API's POST endpoints feel sluggish compared to GET requests.  
**Solution:** Separately benchmark GET and POST methods with realistic payloads to identify the bottleneck.

### 🏗️ Infrastructure Comparison
**Scenario:** Choosing between Nginx and Traefik for your production load balancer.  
**Solution:** Swap Docker Compose environments and run identical benchmark suites to see which proxy handles the load better.

---

## 🔧 Supported HTTP Clients

| Library | Sync | Async | Key Characteristics |
|:---|:---:|:---:|:---|
| **aiohttp** | ❌ | ✅ | Non-blocking I/O, optimal for async services, built-in connection pooling |
| **httpx** | ✅ | ✅ | HTTP/2 support, requests-compatible API, modern design |
| **pycurl** | ✅ | ❌ | libcurl bindings, minimal overhead, C-level performance |
| **requests** | ✅ | ❌ | Industry standard, extensive ecosystem, blocking I/O |
| **requestx** | ✅ | ✅ | Performance-optimized fork, dual-mode execution |
| **urllib3** | ✅ | ❌ | Foundation library, thread-safe pooling, low-level control |

---

## 💾 Database Schema & Analysis

All benchmark results are persisted to SQLite for long-term trend analysis and data-driven decision making.

### 📋 Schema: `benchmark_results`

| Field | Type | Description |
|:---|:---|:---|
| `id` | TEXT | Primary key (UUID) |
| `name` | TEXT | Benchmark run identifier |
| `client_library` | TEXT | Library name (e.g., "httpx") |
| `client_type` | TEXT | Execution model ("sync" or "async") |
| `http_method` | TEXT | HTTP method (GET, POST, etc.) |
| `url` | TEXT | Target URL |
| `start_time` | TEXT | Start timestamp (ISO 8601) |
| `end_time` | TEXT | End timestamp (ISO 8601) |
| `duration` | REAL | Total execution time (seconds) |
| `requests_count` | INTEGER | Total requests completed |
| `requests_per_second` | REAL | Average throughput (RPS) |
| `avg_response_time` | REAL | Mean latency (seconds) |
| `p95_response_time` | REAL | 95th percentile latency (seconds) |
| `p99_response_time` | REAL | 99th percentile latency (seconds) |
| `cpu_usage_avg` | REAL | Average CPU usage (%) |
| `memory_usage_avg` | REAL | Average RSS memory (MB) |
| `error_count` | INTEGER | Total failed requests |
| `error_rate` | REAL | Failure percentage (0-100) |
| `concurrency_level` | INTEGER | Configured concurrency |
| `config_snapshot` | TEXT | JSON snapshot of full configuration |
| `created_at` | TEXT | Record creation timestamp (ISO 8601) |

### 🔍 Analysis Examples

**Compare Client Performance:**
```sql
SELECT 
    client_library,
    ROUND(AVG(requests_per_second), 2) as avg_rps,
    ROUND(AVG(avg_response_time) * 1000, 2) as avg_latency_ms,
    ROUND(AVG(cpu_usage_avg), 2) as avg_cpu_pct
FROM benchmark_results
WHERE http_method = 'GET'
GROUP BY client_library
ORDER BY avg_rps DESC;
```

**Track Performance Over Time:**
```sql
SELECT 
    DATE(created_at) as benchmark_date,
    client_library,
    AVG(requests_per_second) as daily_avg_rps
FROM benchmark_results
WHERE client_library = 'httpx'
GROUP BY DATE(created_at), client_library
ORDER BY benchmark_date DESC;
```

---

## 🧪 Development

### ✅ Running Tests
```bash
# Run all tests
python -m unittest discover tests

# Run specific suite
python -m unittest discover tests/unit
python -m unittest discover tests/integration
python -m unittest discover tests/performance
```

### 🎨 Code Quality
```bash
# Format and lint
black http_benchmark/ tests/ --line-length 120
flake8 http_benchmark/ tests/ --max-line-length=120
mypy http_benchmark/
```

### 🔧 Adding a New HTTP Client
1. Create a new adapter in `http_benchmark/clients/` inheriting from `BaseAdapter`.
2. Register the adapter in `http_benchmark/benchmark.py` within `BenchmarkRunner`.
3. Add corresponding unit tests in `tests/unit/`.

---

## 🏗️ Architecture Deep Dive

### 🔌 Adapter Pattern
The framework uses a clean adapter pattern to decouple the benchmarking engine from specific HTTP client implementations. Each adapter implements a unified interface, making it trivial to add new clients without modifying core logic.

### 📊 Non-Blocking Resource Monitoring
A background thread continuously samples system metrics using `psutil` without interfering with benchmark execution. Metrics are collected at high frequency and aggregated post-benchmark.

### ⚡ Concurrency Management
- **Synchronous Clients**: Managed via `ThreadPoolExecutor` with optimized pool sizing.
- **Asynchronous Clients**: Powered by `asyncio` with task-based concurrency for maximum efficiency.

---

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.

---

**Ready to optimize your HTTP stack? Start benchmarking now! 🚀**
