import unittest
from datetime import datetime
from http_benchmark.models.benchmark_result import BenchmarkResult
from http_benchmark.models.benchmark_configuration import BenchmarkConfiguration
from http_benchmark.models.http_request import HTTPRequest
from http_benchmark.models.resource_metrics import ResourceMetrics


class TestBenchmarkResult(unittest.TestCase):
    def test_benchmark_result_creation(self):
        """Test creating a BenchmarkResult instance."""
        result = BenchmarkResult(
            name="Test Benchmark",
            client_library="requests",
            http_method="GET",
            url="https://example.com",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration=10.0,
            requests_count=100,
            requests_per_second=10.0,
            avg_response_time=0.1,
            min_response_time=0.05,
            max_response_time=0.2,
            p95_response_time=0.15,
            p99_response_time=0.18,
            cpu_usage_avg=25.0,
            memory_usage_avg=100.0,
            network_io={'bytes_sent': 1000, 'bytes_recv': 2000},
            error_count=0,
            error_rate=0.0,
            concurrency_level=5,
            config_snapshot={}
        )
        
        self.assertEqual(result.name, "Test Benchmark")
        self.assertEqual(result.client_library, "requests")
        self.assertEqual(result.http_method, "GET")
        self.assertEqual(result.requests_count, 100)
        self.assertEqual(result.requests_per_second, 10.0)

    def test_to_dict_method(self):
        """Test the to_dict method."""
        result = BenchmarkResult(
            name="Test Benchmark",
            client_library="requests",
            http_method="GET",
            url="https://example.com",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration=10.0,
            requests_count=100,
            requests_per_second=10.0,
            avg_response_time=0.1,
            min_response_time=0.05,
            max_response_time=0.2,
            p95_response_time=0.15,
            p99_response_time=0.18,
            cpu_usage_avg=25.0,
            memory_usage_avg=100.0,
            network_io={'bytes_sent': 1000, 'bytes_recv': 2000},
            error_count=0,
            error_rate=0.0,
            concurrency_level=5,
            config_snapshot={}
        )
        
        result_dict = result.to_dict()
        self.assertIn('name', result_dict)
        self.assertIn('client_library', result_dict)
        self.assertEqual(result_dict['client_library'], 'requests')


class TestBenchmarkConfiguration(unittest.TestCase):
    def test_benchmark_configuration_creation(self):
        """Test creating a BenchmarkConfiguration instance."""
        config = BenchmarkConfiguration(
            target_url="https://example.com",
            http_method="POST",
            concurrency=10,
            duration_seconds=30,
            client_library="httpx"
        )
        
        self.assertEqual(config.target_url, "https://example.com")
        self.assertEqual(config.http_method, "POST")
        self.assertEqual(config.concurrency, 10)
        self.assertEqual(config.duration_seconds, 30)
        self.assertEqual(config.client_library, "httpx")

    def test_default_values(self):
        """Test default values for BenchmarkConfiguration."""
        config = BenchmarkConfiguration(
            target_url="https://example.com"
        )
        
        self.assertEqual(config.http_method, "GET")  # Default value
        self.assertEqual(config.concurrency, 10)      # Default value
        self.assertEqual(config.duration_seconds, 30) # Default value
        self.assertEqual(config.client_library, "requests")  # Default value


class TestHTTPRequest(unittest.TestCase):
    def test_http_request_creation(self):
        """Test creating an HTTPRequest instance."""
        request = HTTPRequest(
            method="POST",
            url="https://example.com/api",
            headers={"Content-Type": "application/json"},
            body='{"test": "data"}',
            timeout=30
        )
        
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.url, "https://example.com/api")
        self.assertEqual(request.headers["Content-Type"], "application/json")
        self.assertEqual(request.body, '{"test": "data"}')
        self.assertEqual(request.timeout, 30)

    def test_default_values(self):
        """Test default values for HTTPRequest."""
        request = HTTPRequest(
            method="GET",
            url="https://example.com"
        )
        
        self.assertEqual(request.method, "GET")
        self.assertEqual(request.headers, {})  # Default empty dict
        self.assertEqual(request.body, "")     # Default empty string
        self.assertEqual(request.timeout, 30)  # Default value


class TestResourceMetrics(unittest.TestCase):
    def test_resource_metrics_creation(self):
        """Test creating a ResourceMetrics instance."""
        timestamp = datetime.now()
        metrics = ResourceMetrics(
            benchmark_id="test-benchmark-123",
            timestamp=timestamp,
            cpu_percent=25.5,
            memory_mb=100.0,
            bytes_sent=1000,
            bytes_received=2000,
            disk_read_mb=1.5,
            disk_write_mb=0.5
        )
        
        self.assertEqual(metrics.benchmark_id, "test-benchmark-123")
        self.assertEqual(metrics.cpu_percent, 25.5)
        self.assertEqual(metrics.memory_mb, 100.0)
        self.assertEqual(metrics.bytes_sent, 1000)
        self.assertEqual(metrics.disk_read_mb, 1.5)


if __name__ == '__main__':
    unittest.main()