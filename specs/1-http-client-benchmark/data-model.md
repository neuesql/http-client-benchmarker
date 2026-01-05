# Data Model: HTTP Client Performance Benchmark Framework

## Overview
This document defines the data models for the HTTP Client Performance Benchmark Framework, including entities, relationships, and validation rules.

## Core Entities

### BenchmarkResult
**Description**: Contains performance metrics from a single benchmark run
**Fields**:
- `id` (UUID): Unique identifier for the benchmark result
- `name` (str): Name/description of the benchmark
- `client_library` (str): HTTP client library used (requests, requestx, httpx, aiohttp, urllib3, pycurl)
- `http_method` (str): HTTP method used (GET, POST, PUT, DELETE, PATCH, STREAM)
- `url` (str): Target URL for the benchmark
- `start_time` (datetime): When the benchmark started
- `end_time` (datetime): When the benchmark ended
- `duration` (float): Total duration in seconds
- `requests_count` (int): Number of requests made
- `requests_per_second` (float): Throughput measurement
- `avg_response_time` (float): Average response time in milliseconds
- `min_response_time` (float): Minimum response time in milliseconds
- `max_response_time` (float): Maximum response time in milliseconds
- `p95_response_time` (float): 95th percentile response time in milliseconds
- `p99_response_time` (float): 99th percentile response time in milliseconds
- `cpu_usage_avg` (float): Average CPU usage during benchmark (%)
- `memory_usage_avg` (float): Average memory usage during benchmark (MB)
- `network_io` (dict): Network I/O metrics (bytes sent/received)
- `error_count` (int): Number of failed requests
- `error_rate` (float): Percentage of failed requests
- `concurrency_level` (int): Number of concurrent requests
- `config_snapshot` (dict): Configuration used for this benchmark

### BenchmarkConfiguration
**Description**: Holds configurable parameters for benchmark execution
**Fields**:
- `id` (UUID): Unique identifier for the configuration
- `name` (str): Name/description of the configuration
- `target_url` (str): URL to benchmark
- `http_method` (str): HTTP method to use (default: GET)
- `headers` (dict): HTTP headers to include in requests
- `body` (str): Request body content (for POST, PUT, etc.)
- `concurrency` (int): Number of concurrent requests (default: 10)
- `duration_seconds` (int): Duration of benchmark in seconds (default: 30)
- `total_requests` (int): Total number of requests to make (alternative to duration)
- `client_library` (str): HTTP client library to use
- `is_async` (bool): Whether to use async or sync requests
- `timeout` (int): Request timeout in seconds (default: 30)
- `verify_ssl` (bool): Whether to verify SSL certificates (default: True)
- `retry_attempts` (int): Number of retry attempts for failed requests (default: 3)
- `delay_between_requests` (float): Delay between requests in seconds (default: 0)

### HTTPRequest
**Description**: Represents an HTTP request with method, URL, headers, and body for benchmarking
**Fields**:
- `id` (UUID): Unique identifier for the request
- `method` (str): HTTP method (GET, POST, PUT, DELETE, PATCH, STREAM)
- `url` (str): Target URL
- `headers` (dict): HTTP headers
- `body` (str): Request body content
- `timeout` (int): Request timeout in seconds
- `verify_ssl` (bool): Whether to verify SSL certificates

### ResourceMetrics
**Description**: Captures system resource usage during benchmark execution
**Fields**:
- `id` (UUID): Unique identifier for the metrics collection
- `benchmark_id` (UUID): Reference to the associated benchmark
- `timestamp` (datetime): When metrics were collected
- `cpu_percent` (float): CPU usage percentage
- `memory_mb` (float): Memory usage in MB
- `bytes_sent` (int): Network bytes sent
- `bytes_received` (int): Network bytes received
- `disk_read_mb` (float): Disk read in MB
- `disk_write_mb` (float): Disk write in MB

## Relationships
- `BenchmarkResult` 1:M `ResourceMetrics` (one benchmark result can have many resource metric snapshots)
- `BenchmarkConfiguration` 1:M `BenchmarkResult` (one configuration can be used for many benchmark runs)

## Validation Rules
1. `BenchmarkResult`:
   - `requests_count` must be greater than 0
   - `requests_per_second` must be greater than 0
   - `avg_response_time` must be greater than 0
   - `concurrency_level` must be greater than 0
   - `client_library` must be one of the supported libraries

2. `BenchmarkConfiguration`:
   - `concurrency` must be between 1 and 10000
   - `duration_seconds` must be greater than 0
   - `total_requests` must be greater than 0
   - `timeout` must be greater than 0
   - `client_library` must be one of the supported libraries: requests, requestx, httpx, aiohttp, urllib3, pycurl
   - `delay_between_requests` must be greater than or equal to 0

3. `HTTPRequest`:
   - `url` must be a valid URL format
   - `method` must be one of the supported HTTP methods

4. `ResourceMetrics`:
   - `cpu_percent` must be between 0 and 100
   - `memory_mb` must be greater than 0
   - `bytes_sent` and `bytes_received` must be greater than or equal to 0

## State Transitions
- `BenchmarkConfiguration` can be in states: DRAFT, ACTIVE, ARCHIVED
- `BenchmarkResult` can be in states: RUNNING, COMPLETED, FAILED