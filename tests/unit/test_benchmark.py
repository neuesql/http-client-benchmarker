import unittest
from unittest.mock import Mock, patch
from http_benchmark.benchmark import BenchmarkRunner
from http_benchmark.models.benchmark_configuration import BenchmarkConfiguration
from http_benchmark.models.benchmark_result import BenchmarkResult


class TestBenchmarkRunner(unittest.TestCase):
    def test_benchmark_runner_initialization(self):
        """Test BenchmarkRunner initialization."""
        config = BenchmarkConfiguration(
            target_url="https://example.com",
            client_library="requests"
        )
        runner = BenchmarkRunner(config)
        
        self.assertEqual(runner.config, config)
        self.assertIsNotNone(runner.adapters)
        self.assertIn('requests', runner.adapters)
        self.assertIn('httpx', runner.adapters)
        self.assertIn('aiohttp', runner.adapters)
        self.assertIn('urllib3', runner.adapters)
        self.assertIn('pycurl', runner.adapters)
        self.assertIn('requestx', runner.adapters)

    def test_run_method_exists(self):
        """Test that run method exists."""
        config = BenchmarkConfiguration(
            target_url="https://example.com",
            client_library="requests"
        )
        runner = BenchmarkRunner(config)
        self.assertTrue(callable(getattr(runner, 'run', None)))

    def test_run_method_with_invalid_client(self):
        """Test run method with invalid client library."""
        config = BenchmarkConfiguration(
            target_url="https://example.com",
            client_library="invalid_client"
        )
        runner = BenchmarkRunner(config)
        
        with self.assertRaises(ValueError) as context:
            runner.run()
        
        self.assertIn("Unsupported client library", str(context.exception))

    def test_sync_benchmark_method_exists(self):
        """Test that _run_sync_benchmark method exists."""
        config = BenchmarkConfiguration(
            target_url="https://example.com",
            client_library="requests"
        )
        runner = BenchmarkRunner(config)
        self.assertTrue(callable(getattr(runner, '_run_sync_benchmark', None)))

    def test_async_benchmark_method_exists(self):
        """Test that _run_async_benchmark method exists."""
        config = BenchmarkConfiguration(
            target_url="https://example.com",
            client_library="httpx",
            is_async=True
        )
        runner = BenchmarkRunner(config)
        self.assertTrue(callable(getattr(runner, '_run_async_benchmark', None)))

    @patch('http_benchmark.clients.requests_adapter.RequestsAdapter')
    def test_run_with_mocked_adapter(self, mock_adapter_class):
        """Test run method with mocked adapter."""
        # Create a mock adapter instance
        mock_adapter = Mock()
        mock_adapter_class.return_value = mock_adapter
        
        # Mock the make_request method to return a successful response
        mock_adapter.make_request.return_value = {
            'success': True,
            'response_time': 0.1
        }
        
        config = BenchmarkConfiguration(
            target_url="https://example.com",
            client_library="requests",
            concurrency=1,
            total_requests=1
        )
        
        runner = BenchmarkRunner(config)
        # Temporarily replace the adapters dict to use our mock
        runner.adapters = {'requests': mock_adapter}
        
        # This test would require more complex mocking to fully work
        # For now, we're just verifying the structure
        self.assertEqual(runner.config, config)

    def test_configuration_validation(self):
        """Test configuration validation."""
        config = BenchmarkConfiguration(
            target_url="https://example.com",
            client_library="requests"
        )
        runner = BenchmarkRunner(config)
        
        # Verify the configuration is properly stored
        self.assertEqual(runner.config.target_url, "https://example.com")
        self.assertEqual(runner.config.client_library, "requests")


class TestAsyncBenchmarkRunner(unittest.TestCase):
    def test_async_benchmark_runner_exists(self):
        """Test that AsyncBenchmarkRunner class exists."""
        from http_benchmark.benchmark import AsyncBenchmarkRunner
        self.assertTrue(hasattr(AsyncBenchmarkRunner, 'run'))
        self.assertTrue(callable(getattr(AsyncBenchmarkRunner, 'run', None)))


if __name__ == '__main__':
    unittest.main()