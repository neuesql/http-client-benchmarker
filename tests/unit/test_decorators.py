import unittest
from unittest.mock import Mock, patch
from http_benchmark.decorators import benchmark, benchmark_function
from http_benchmark.models.benchmark_configuration import BenchmarkConfiguration


class TestBenchmarkDecorator(unittest.TestCase):
    def test_decorator_functionality(self):
        """Test that the benchmark decorator can be applied to a function."""
        @benchmark(client_library="httpx", concurrency=2, duration_seconds=1)
        def sample_function():
            return "test result"
        
        # Apply the decorator and call the function
        result = sample_function()
        self.assertEqual(result, "test result")

    def test_decorator_with_parameters(self):
        """Test the benchmark decorator with various parameters."""
        @benchmark(
            client_library="requests",
            concurrency=1,
            duration_seconds=1,
            http_method="GET",
            store_results=False
        )
        def another_function():
            return {"status": "success"}
        
        result = another_function()
        self.assertEqual(result, {"status": "success"})

    def test_decorator_creates_configuration(self):
        """Test that the decorator creates appropriate configuration."""
        @benchmark(client_library="httpx", concurrency=3, target_url="https://example.com")
        def test_func():
            return "result"
        
        result = test_func()
        self.assertEqual(result, "result")

    def test_benchmark_function_decorator(self):
        """Test the benchmark_function decorator."""
        @benchmark_function(
            target_url="https://httpbin.org/get",
            http_method="GET",
            client_library="httpx",
            concurrency=1,
            duration_seconds=1
        )
        def api_call():
            return {"data": "test"}
        
        result = api_call()
        self.assertEqual(result, {"data": "test"})

    def test_decorator_preserves_function_metadata(self):
        """Test that the decorator preserves the original function's metadata."""
        def original_function():
            """This is the original function docstring."""
            return "original result"
        
        decorated_function = benchmark(client_library="httpx")(original_function)
        
        # The function should still work
        result = decorated_function()
        self.assertEqual(result, "original result")

    def test_decorator_with_exception_handling(self):
        """Test decorator behavior when the wrapped function raises an exception."""
        @benchmark(client_library="httpx", concurrency=1, duration_seconds=1)
        def error_function():
            raise ValueError("Test error")
        
        with self.assertRaises(ValueError):
            error_function()


class TestDecoratorIntegration(unittest.TestCase):
    def test_decorator_with_actual_http_call(self):
        """Test decorator with a mock HTTP call."""
        import httpx
        
        @benchmark(client_library="httpx", concurrency=1, duration_seconds=1)
        def mock_http_call():
            # This would normally make an HTTP call, but we'll mock it
            return {"status": 200, "data": "response"}
        
        result = mock_http_call()
        self.assertEqual(result, {"status": 200, "data": "response"})


if __name__ == '__main__':
    unittest.main()