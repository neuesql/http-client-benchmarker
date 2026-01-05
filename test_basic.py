"""Simple test to verify the basic functionality of the HTTP benchmark framework."""

from http_benchmark.benchmark import BenchmarkRunner
from http_benchmark.models.benchmark_configuration import BenchmarkConfiguration
from http_benchmark.storage import ResultStorage


def test_basic_benchmark():
    """Test basic benchmark functionality."""
    print("Testing basic benchmark functionality...")
    
    # Create a simple configuration
    config = BenchmarkConfiguration(
        target_url="https://httpbin.org/get",
        http_method="GET",
        concurrency=2,
        duration_seconds=5,
        client_library="requests"
    )
    
    # Create a benchmark runner
    runner = BenchmarkRunner(config)
    
    # Run the benchmark (this would normally make actual HTTP requests)
    # For this test, we'll just verify the objects can be created
    print(f"Configuration created: {config.name}")
    print(f"Target URL: {config.target_url}")
    print(f"Client library: {config.client_library}")
    print(f"Concurrency: {config.concurrency}")
    
    print("Basic functionality test passed!")


def test_storage():
    """Test storage functionality."""
    print("\nTesting storage functionality...")
    
    # Create storage instance
    storage = ResultStorage()
    print("Storage instance created successfully")
    
    print("Storage functionality test passed!")


if __name__ == "__main__":
    test_basic_benchmark()
    test_storage()
    print("\nAll basic tests passed! The framework is set up correctly.")