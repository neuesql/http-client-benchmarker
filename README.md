# ⚡ HTTP Client & Server Performance Benchmark Framework

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Introduction

**Stop guessing, start measuring.** Make data-driven decisions about your HTTP stack with precision benchmarking.

In the world of high-performance Python services, the right combination of HTTP client, server infrastructure, and request methods can make or break your application's performance. This framework eliminates the guesswork by providing comprehensive, real-world benchmarks across your entire HTTP stack.

### 🎯 Why This Framework?

Traditional benchmarking tools focus on a single dimension—either the client OR the server. We take a holistic approach, enabling you to optimize **three critical dimensions** of your HTTP infrastructure:

#### 🔧 **1. HTTP Client Selection** — *Choose Your Weapon*
Pick the perfect client library for your workload. Should you migrate from `requests` to `httpx`? Is `aiohttp` worth the async complexity? Get concrete answers.

**Available Clients:**
- 🐍 **`requests`** — The battle-tested synchronous standard
- ⚡ **`httpx`** — Modern HTTP/1.1 and HTTP/2 with sync/async modes
- 🌊 **`aiohttp`** — Pure async powerhouse for non-blocking I/O
- 🔗 **`pycurl`** — Low-level libcurl bindings for minimal overhead
- 🚄 **`requestx`** — Performance-optimized dual-mode client
- 🔌 **`urllib3`** — Thread-safe connection pooling at the foundation layer

#### 🏗️ **2. Server Infrastructure** — *Build Your Battlefield*
Test against production-realistic environments. Compare reverse proxies, load balancers, and server configurations to find your infrastructure sweet spot.

**Available Servers:**
- 🎈 **Simple HTTPBin** — Lightweight single-instance for quick validation
- 🎪 **Traefik Load Balancer** — Cloud-native proxy with 3 backend instances
- 🚀 **Nginx Load Balancer** — Battle-hardened reverse proxy with superior throughput

#### 📮 **3. HTTP Methods** — *Test What Matters*
Different HTTP methods have wildly different performance characteristics. Benchmark the operations your application actually uses. **All standard HTTP methods are supported.**

**Common Methods (Examples):**
- 📥 **GET** — Read operations and caching behavior
- 📤 **POST** — Payload submission and data creation
- 🔄 **PUT** — Full resource updates
- 🩹 **PATCH** — Partial modifications
- 🗑️ **DELETE** — Resource cleanup operations
- 🔍 **HEAD**, **OPTIONS**, **TRACE**, **CONNECT** — And more...

### 💎 Key Features

✅ **Mix & Match Testing** — Any client × any server × any method = complete coverage  
✅ **Real-World Metrics** — Throughput (RPS), latency percentiles (p95/p99), CPU, and memory  
✅ **Persistent Storage** — SQLite database for historical trend analysis  
✅ **Production-Ready** — Test with HTTPS, load balancers, and multi-instance deployments  
✅ **Zero Interference** — Non-blocking resource monitoring doesn't skew results  
✅ **Extensible Design** — Clean adapter pattern for adding custom clients  

### 🎬 Quick Example

```bash
# Compare all clients against Nginx with POST requests
python -m http_benchmark.cli \
  --url https://localhost/post \
  --method POST \
  --body '{"test": "data"}' \
  --compare requests httpx aiohttp \
  --concurrency 50 \
  --duration 60
```

**The Result?** Hard data showing which client handles your specific workload best. No more architecture debates based on hunches.

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
1. Configure your benchmark (client, server, method, concurrency)
2. Execute requests while monitoring system resources
3. Collect and aggregate performance metrics
4. Persist results to SQLite for analysis
5. Display comparative results in the console

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

Choose a server configuration that mirrors your production environment. Each option provides different levels of complexity and realism.

#### **Option 1: Simple HTTPBin** 🎈
*Perfect for quick validation and debugging*

**Features:**
- Single instance, minimal overhead
- HTTP-only support
- Ideal for baseline measurements

**Launch:**
```bash
docker-compose -f httpbin_server/docker-compose.httpbin.yml up -d
```

**Endpoints:**
- `http://localhost/get`, `/post`, `/put`, `/patch`, `/delete`

**Test it:**
```bash
curl http://localhost/get
```

---

#### **Option 2: Traefik Load Balancer** 🎪
*Cloud-native proxy for real-world simulation*

**Features:**
- 3 load-balanced HTTPBin instances
- HTTP + HTTPS support (self-signed cert)
- Health checks and automatic failover
- Dynamic routing and service discovery

**Launch:**
```bash
docker-compose -f httpbin_server/docker-compose.traefik.yml up -d
```

**Endpoints:**
- `http://localhost/` (load balanced)
- `https://localhost/` (TLS termination)

**Test it:**
```bash
# HTTP
curl http://localhost/get

# HTTPS (ignore self-signed cert)
curl -k https://localhost/get
```

---

#### **Option 3: Nginx Load Balancer** 🚀
*Battle-tested reverse proxy for maximum performance*

**Features:**
- 3 load-balanced HTTPBin instances
- Optimized for raw throughput
- HTTP + HTTPS support
- Industry-standard configuration

**Launch:**
```bash
docker-compose -f httpbin_server/docker-compose.nginx.yml up -d
```

**Endpoints:**
- `http://localhost/` (load balanced)
- `https://localhost/` (SSL termination)

**Test it:**
```bash
# HTTP
curl http://localhost/get

# HTTPS
curl -k https://localhost/post -d '{"key":"value"}'
```

---

### 📊 Server Comparison Matrix

| Feature | 🎈 Simple HTTPBin | 🎪 Traefik | 🚀 Nginx |
|:---|:---:|:---:|:---:|
| **Backend Instances** | 1 | 3 | 3 |
| **HTTP Support** | ✅ | ✅ | ✅ |
| **HTTPS Support** | ❌ | ✅ | ✅ |
| **Load Balancing** | ❌ | ✅ | ✅ |
| **Health Checks** | ❌ | ✅ | ✅ |
| **SSL/TLS Termination** | ❌ | ✅ | ✅ |
| **Resource Overhead** | Low | High | Medium |
| **Configuration Complexity** | Low | High | Medium |
| **Best For** | **Quick tests** | **Real-world simulation** | **Raw performance** |

---

### ▶️ Step 2: Run Your Benchmark

#### Single Client Benchmark
Test a specific client with your chosen configuration:

```bash
python -m http_benchmark.cli \
  --url http://localhost/get \
  --client httpx \
  --concurrency 20 \
  --duration 30
```

#### Head-to-Head Comparison
Compare multiple clients simultaneously:

```bash
python -m http_benchmark.cli \
  --url http://localhost/get \
  --compare requests httpx aiohttp \
  --concurrency 10 \
  --duration 10
```

#### Full HTTP Method Coverage
Test different request types to understand method-specific performance:

```bash
# GET - Baseline read performance
python -m http_benchmark.cli \
  --url http://localhost/get \
  --method GET \
  --client requests \
  --concurrency 50 \
  --duration 30

# POST - Payload handling
python -m http_benchmark.cli \
  --url http://localhost/post \
  --method POST \
  --client httpx \
  --body '{"user": "test", "action": "create"}' \
  --concurrency 50 \
  --duration 30

# PUT - Full resource updates
python -m http_benchmark.cli \
  --url http://localhost/put \
  --method PUT \
  --client aiohttp \
  --body '{"id": 123, "status": "updated"}' \
  --concurrency 50 \
  --duration 30

# PATCH - Partial modifications
python -m http_benchmark.cli \
  --url http://localhost/patch \
  --method PATCH \
  --client urllib3 \
  --body '{"status": "modified"}' \
  --concurrency 50 \
  --duration 30

# DELETE - Resource cleanup
python -m http_benchmark.cli \
  --url http://localhost/delete \
  --method DELETE \
  --client pycurl \
  --concurrency 50 \
  --duration 30
```

---

## 🎯 Use Cases

### 🔍 Client Selection & Migration
**Scenario:** Your team is considering migrating from `requests` to `httpx` to leverage HTTP/2.

**Solution:**
```bash
python -m http_benchmark.cli \
  --url https://localhost/get \
  --compare requests httpx \
  --concurrency 100 \
  --duration 60
```

**Outcome:** Concrete RPS, latency, and resource usage data to inform your migration decision.

---

### 📈 Method-Specific Optimization
**Scenario:** Your API's POST endpoints feel sluggish compared to GET requests.

**Solution:**
```bash
# Test GET
python -m http_benchmark.cli --url http://localhost/get --method GET --client httpx --duration 30

# Test POST
python -m http_benchmark.cli --url http://localhost/post --method POST --body '{"data":"test"}' --client httpx --duration 30
```

**Outcome:** Quantify the performance gap and identify whether it's client-side, server-side, or payload-related.

---

### 🏗️ Infrastructure Comparison
**Scenario:** Choosing between Nginx and Traefik for your production load balancer.

**Solution:**
```bash
# Benchmark Nginx
docker-compose -f httpbin_server/docker-compose.nginx.yml up -d
python -m http_benchmark.cli --url http://localhost/get --client httpx --duration 60
docker-compose -f httpbin_server/docker-compose.nginx.yml down

# Benchmark Traefik
docker-compose -f httpbin_server/docker-compose.traefik.yml up -d
python -m http_benchmark.cli --url http://localhost/get --client httpx --duration 60
```

**Outcome:** Direct comparison of throughput, latency, and resource overhead under identical conditions.

---

### 🔬 Resource Profiling at Scale
**Scenario:** Understanding how your client behaves under extreme concurrency.

**Solution:**
```bash
python -m http_benchmark.cli \
  --url http://localhost/get \
  --client aiohttp \
  --concurrency 1000 \
  --duration 120
```

**Outcome:** CPU and memory usage patterns at high load, helping you capacity plan.

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

### When to Use Each Client

- **`requests`**: Default choice for sync applications, extensive third-party integrations
- **`httpx`**: When you need HTTP/2 or want sync/async flexibility
- **`aiohttp`**: Pure async applications with high concurrency requirements
- **`urllib3`**: When you need fine-grained control over connection pooling
- **`pycurl`**: Maximum performance for sync applications, C-level speed
- **`requestx`**: Drop-in replacement for requests with better performance

---

## ⚙️ Configuration

Customize the framework using environment variables. All variables are prefixed with `HTTP_BENCHMARK_`.

### Environment Variables

| Variable | Default | Description |
|:---|:---|:---|
| `HTTP_BENCHMARK_DEFAULT_CONCURRENCY` | `10` | Default concurrent workers |
| `HTTP_BENCHMARK_DEFAULT_DURATION_SECONDS` | `30` | Default benchmark duration (seconds) |
| `HTTP_BENCHMARK_MAX_CONCURRENCY` | `10000` | Safety limit for concurrency |
| `HTTP_BENCHMARK_SQLITE_DB_PATH` | `benchmark_results.db` | SQLite database file path |
| `HTTP_BENCHMARK_RESOURCE_MONITORING_INTERVAL` | `0.1` | Resource sampling interval (seconds) |

### Example Configuration

```bash
# Set custom defaults
export HTTP_BENCHMARK_DEFAULT_CONCURRENCY=50
export HTTP_BENCHMARK_DEFAULT_DURATION_SECONDS=60
export HTTP_BENCHMARK_SQLITE_DB_PATH=/tmp/my_benchmarks.db

# Run benchmark with custom config
python -m http_benchmark.cli --url http://localhost/get --client httpx
```

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

#### Compare Client Performance
```sql
SELECT 
    client_library,
    client_type,
    ROUND(AVG(requests_per_second), 2) as avg_rps,
    ROUND(AVG(avg_response_time) * 1000, 2) as avg_latency_ms,
    ROUND(AVG(p95_response_time) * 1000, 2) as p95_latency_ms,
    ROUND(AVG(cpu_usage_avg), 2) as avg_cpu_pct,
    ROUND(AVG(memory_usage_avg), 2) as avg_memory_mb
FROM benchmark_results
WHERE http_method = 'GET'
GROUP BY client_library, client_type
ORDER BY avg_rps DESC;
```

#### Track Performance Over Time
```sql
SELECT 
    DATE(created_at) as benchmark_date,
    client_library,
    AVG(requests_per_second) as daily_avg_rps,
    AVG(avg_response_time) * 1000 as daily_avg_latency_ms
FROM benchmark_results
WHERE client_library = 'httpx'
GROUP BY DATE(created_at), client_library
ORDER BY benchmark_date DESC
LIMIT 30;
```

#### Identify Performance Regressions
```sql
WITH baseline AS (
    SELECT AVG(requests_per_second) as baseline_rps
    FROM benchmark_results
    WHERE client_library = 'requests' AND created_at < '2024-01-01'
)
SELECT 
    created_at,
    client_library,
    requests_per_second,
    ((requests_per_second - baseline_rps) / baseline_rps * 100) as pct_change
FROM benchmark_results, baseline
WHERE client_library = 'requests' AND created_at >= '2024-01-01'
ORDER BY created_at;
```

#### Method-Specific Analysis
```sql
SELECT 
    http_method,
    AVG(requests_per_second) as avg_rps,
    AVG(avg_response_time) * 1000 as avg_latency_ms,
    AVG(error_rate) as avg_error_pct
FROM benchmark_results
WHERE client_library = 'httpx'
GROUP BY http_method
ORDER BY avg_rps DESC;
```

---

## 🧪 Development

### ✅ Running Tests

We maintain comprehensive test coverage across unit, integration, and performance test suites.

```bash
# Run all tests
python -m unittest discover tests

# Unit tests only
python -m unittest discover tests/unit

# Integration tests (requires Docker)
python -m unittest discover tests/integration

# Performance tests
python -m unittest discover tests/performance
```

### 🎨 Code Quality

```bash
# Format code
black http_benchmark/ tests/ --line-length 120

# Lint code
flake8 http_benchmark/ tests/ --max-line-length=120

# Type checking
mypy http_benchmark/
```

### 🔧 Adding a New HTTP Client

1. Create a new adapter in `http_benchmark/adapters/`:
   ```python
   from http_benchmark.adapters.base import BaseAdapter
   
   class MyClientAdapter(BaseAdapter):
       def execute_sync(self, url, method, **kwargs):
           # Implementation
           pass
   ```

2. Register in `http_benchmark/adapters/__init__.py`:
   ```python
   from .my_client import MyClientAdapter
   
   ADAPTERS = {
       'myclient': MyClientAdapter,
       # ... existing adapters
   }
   ```

3. Add tests in `tests/unit/adapters/test_my_client.py`

---

## 🏗️ Architecture Deep Dive

### 🔌 Adapter Pattern
The framework uses a clean adapter pattern to decouple the benchmarking engine from specific HTTP client implementations. Each adapter implements a unified interface, making it trivial to add new clients without modifying core logic.

**Benefits:**
- Add new clients in minutes
- Consistent behavior across all clients
- Easy to maintain and test

### 📊 Non-Blocking Resource Monitoring
A background thread continuously samples system metrics using `psutil` without interfering with benchmark execution. Metrics are collected at high frequency and aggregated post-benchmark.

**Monitored Resources:**
- CPU usage (per-core and aggregate)
- Memory usage (RSS, VMS)
- I/O operations (read/write bytes)
- Network statistics

### ⚡ Concurrency Management

**Synchronous Clients:**
Managed via `ThreadPoolExecutor` with optimized pool sizing based on concurrency level.

**Asynchronous Clients:**
Powered by `asyncio` with task-based concurrency for maximum efficiency. No thread overhead.

### 🎯 Request Execution Pipeline

1. **Initialization:** Create client adapter, configure parameters
2. **Warm-up:** Execute warm-up requests to stabilize connections
3. **Monitoring Start:** Spawn resource monitoring thread
4. **Execution:** Execute requests based on duration and concurrency
5. **Monitoring Stop:** Halt resource sampling
6. **Aggregation:** Calculate metrics (RPS, percentiles, resource usage)
7. **Persistence:** Store results in SQLite
8. **Reporting:** Display results to console

---

## 📚 Additional Resources

- **API Documentation**: See `docs/api.md` for programmatic usage
- **Troubleshooting**: Common issues and solutions in `docs/troubleshooting.md`
- **Performance Tuning**: Best practices in `docs/performance_tuning.md`

---

## 🤝 Contributing

We welcome contributions! Please see `CONTRIBUTING.md` for guidelines.

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## 🙏 Acknowledgments

Built with:
- `psutil` for resource monitoring
- `httpx`, `aiohttp`, `requests`, and other excellent HTTP libraries
- `sqlite3` for persistence
- Docker ecosystem for isolated testing

---

**Ready to optimize your HTTP stack? Start benchmarking now! 🚀**