import unittest
from http_benchmark.config import settings


class TestConfiguration(unittest.TestCase):
    def test_settings_defaults(self):
        """Test default configuration values."""
        self.assertEqual(settings.app_name, "HTTP Client Benchmark Framework")
        self.assertEqual(settings.default_concurrency, 10)
        self.assertEqual(settings.default_duration_seconds, 30)
        self.assertEqual(settings.default_timeout, 30)
        self.assertEqual(settings.max_concurrency, 10000)
        self.assertEqual(settings.sqlite_db_path, "benchmark_results.db")
        self.assertEqual(settings.results_retention_days, 90)

    def test_supported_libraries(self):
        """Test that all required HTTP client libraries are supported."""
        expected_libraries = ["requests", "requestx", "httpx", "aiohttp", "urllib3", "pycurl"]
        self.assertEqual(settings.supported_client_libraries, expected_libraries)

    def test_supported_http_methods(self):
        """Test that all required HTTP methods are supported."""
        expected_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "STREAM"]
        self.assertEqual(settings.supported_http_methods, expected_methods)

    def test_monitoring_settings(self):
        """Test resource monitoring settings."""
        self.assertTrue(settings.cpu_monitoring_enabled)
        self.assertTrue(settings.memory_monitoring_enabled)
        self.assertTrue(settings.network_monitoring_enabled)
        self.assertEqual(settings.resource_monitoring_interval, 0.1)


if __name__ == '__main__':
    unittest.main()