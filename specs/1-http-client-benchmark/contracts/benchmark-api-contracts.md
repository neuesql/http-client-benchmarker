# API Contracts: HTTP Client Benchmark Framework

## Overview
This document defines the API contracts for the HTTP Client Benchmark Framework, specifying the interfaces for creating client test cases based on API specifications.

## Benchmark Configuration API

### Create Benchmark Configuration
**Endpoint**: `POST /api/configurations`
**Description**: Creates a new benchmark configuration

**Request Body**:
```json
{
  "name": "string, required - Name of the configuration",
  "target_url": "string, required - URL to benchmark",
  "http_method": "string, required - HTTP method (GET, POST, PUT, DELETE, PATCH, STREAM)",
  "headers": {
    "object, optional - HTTP headers to include in requests"
  },
  "body": "string, optional - Request body content",
  "concurrency": "integer, optional, default: 10 - Number of concurrent requests",
  "duration_seconds": "integer, optional, default: 30 - Duration of benchmark in seconds",
  "total_requests": "integer, optional - Total number of requests to make",
  "client_library": "string, required - HTTP client library to use",
  "is_async": "boolean, optional, default: false - Whether to use async requests",
  "timeout": "integer, optional, default: 30 - Request timeout in seconds",
  "verify_ssl": "boolean, optional, default: true - Whether to verify SSL certificates",
  "retry_attempts": "integer, optional, default: 3 - Number of retry attempts for failed requests",
  "delay_between_requests": "number, optional, default: 0 - Delay between requests in seconds"
}
```

**Response**:
```json
{
  "id": "string - Unique identifier for the configuration",
  "name": "string - Name of the configuration",
  "target_url": "string - URL to benchmark",
  "http_method": "string - HTTP method",
  "headers": {
    "object - HTTP headers"
  },
  "concurrency": "integer - Number of concurrent requests",
  "duration_seconds": "integer - Duration of benchmark in seconds",
  "client_library": "string - HTTP client library to use",
  "is_async": "boolean - Whether to use async requests",
  "timeout": "integer - Request timeout in seconds",
  "verify_ssl": "boolean - Whether to verify SSL certificates",
  "retry_attempts": "integer - Number of retry attempts",
  "delay_between_requests": "number - Delay between requests in seconds",
  "created_at": "string - ISO 8601 timestamp of creation"
}
```

### Get Benchmark Configuration
**Endpoint**: `GET /api/configurations/{id}`
**Description**: Retrieves a specific benchmark configuration

**Response**:
```json
{
  "id": "string - Unique identifier for the configuration",
  "name": "string - Name of the configuration",
  "target_url": "string - URL to benchmark",
  "http_method": "string - HTTP method",
  "headers": {
    "object - HTTP headers"
  },
  "concurrency": "integer - Number of concurrent requests",
  "duration_seconds": "integer - Duration of benchmark in seconds",
  "client_library": "string - HTTP client library to use",
  "is_async": "boolean - Whether to use async requests",
  "timeout": "integer - Request timeout in seconds",
  "verify_ssl": "boolean - Whether to verify SSL certificates",
  "retry_attempts": "integer - Number of retry attempts",
  "delay_between_requests": "number - Delay between requests in seconds",
  "created_at": "string - ISO 8601 timestamp of creation"
}
```

## Benchmark Execution API

### Run Benchmark
**Endpoint**: `POST /api/benchmarks/run`
**Description**: Executes a benchmark run with the specified configuration

**Request Body**:
```json
{
  "configuration_id": "string, required - ID of the configuration to use",
  "override_params": {
    "object, optional - Parameters to override from the configuration"
  }
}
```

**Response**:
```json
{
  "id": "string - Unique identifier for the benchmark run",
  "configuration_id": "string - ID of the configuration used",
  "status": "string - Status of the benchmark (RUNNING, COMPLETED, FAILED)",
  "start_time": "string - ISO 8601 timestamp of start",
  "end_time": "string - ISO 8601 timestamp of end (null if still running)",
  "result_summary": {
    "requests_count": "integer - Number of requests made",
    "requests_per_second": "number - Throughput measurement",
    "avg_response_time": "number - Average response time in milliseconds",
    "error_rate": "number - Percentage of failed requests"
  }
}
```

### Get Benchmark Result
**Endpoint**: `GET /api/benchmarks/{id}`
**Description**: Retrieves the results of a benchmark run

**Response**:
```json
{
  "id": "string - Unique identifier for the benchmark run",
  "configuration_id": "string - ID of the configuration used",
  "name": "string - Name/description of the benchmark",
  "client_library": "string - HTTP client library used",
  "http_method": "string - HTTP method used",
  "url": "string - Target URL for the benchmark",
  "start_time": "string - ISO 8601 timestamp of start",
  "end_time": "string - ISO 8601 timestamp of end",
  "duration": "number - Total duration in seconds",
  "requests_count": "integer - Number of requests made",
  "requests_per_second": "number - Throughput measurement",
  "avg_response_time": "number - Average response time in milliseconds",
  "min_response_time": "number - Minimum response time in milliseconds",
  "max_response_time": "number - Maximum response time in milliseconds",
  "p95_response_time": "number - 95th percentile response time in milliseconds",
  "p99_response_time": "number - 99th percentile response time in milliseconds",
  "cpu_usage_avg": "number - Average CPU usage during benchmark (%)",
  "memory_usage_avg": "number - Average memory usage during benchmark (MB)",
  "network_io": {
    "bytes_sent": "integer - Network bytes sent",
    "bytes_received": "integer - Network bytes received"
  },
  "error_count": "integer - Number of failed requests",
  "error_rate": "number - Percentage of failed requests",
  "concurrency_level": "integer - Number of concurrent requests",
  "config_snapshot": "object - Configuration used for this benchmark"
}
```

## Results Management API

### List Benchmark Results
**Endpoint**: `GET /api/results`
**Description**: Lists benchmark results with optional filtering

**Query Parameters**:
- `client_library`: Filter by HTTP client library
- `http_method`: Filter by HTTP method
- `limit`: Number of results to return (default: 10)
- `offset`: Number of results to skip (default: 0)

**Response**:
```json
{
  "results": [
    {
      "id": "string - Unique identifier for the benchmark run",
      "name": "string - Name/description of the benchmark",
      "client_library": "string - HTTP client library used",
      "http_method": "string - HTTP method used",
      "url": "string - Target URL for the benchmark",
      "start_time": "string - ISO 8601 timestamp of start",
      "duration": "number - Total duration in seconds",
      "requests_per_second": "number - Throughput measurement",
      "avg_response_time": "number - Average response time in milliseconds",
      "error_rate": "number - Percentage of failed requests"
    }
  ],
  "total_count": "integer - Total number of results matching the filter"
}
```

### Compare Benchmark Results
**Endpoint**: `POST /api/results/compare`
**Description**: Compares multiple benchmark results

**Request Body**:
```json
{
  "result_ids": ["string - Array of benchmark result IDs to compare"]
}
```

**Response**:
```json
{
  "comparison": [
    {
      "id": "string - Unique identifier for the benchmark run",
      "name": "string - Name/description of the benchmark",
      "client_library": "string - HTTP client library used",
      "requests_per_second": "number - Throughput measurement",
      "avg_response_time": "number - Average response time in milliseconds",
      "error_rate": "number - Percentage of failed requests",
      "cpu_usage_avg": "number - Average CPU usage (%)",
      "memory_usage_avg": "number - Average memory usage (MB)"
    }
  ],
  "summary": {
    "fastest_avg_response_time": "string - ID of the fastest result",
    "highest_throughput": "string - ID of the highest throughput result",
    "lowest_error_rate": "string - ID of the lowest error rate result"
  }
}
```