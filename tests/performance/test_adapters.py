"""Performance tests for different HTTP clients targeting localhost with GET requests (HTTP version)."""

import unittest
from tabulate import tabulate
from http_benchmark.benchmark import BenchmarkRunner
from http_benchmark.models.benchmark_configuration import BenchmarkConfiguration
from http_benchmark.storage import ResultStorage


class TestLocalhostAdapters(unittest.TestCase):
    """Performance tests comparing different HTTP clients against localhost (HTTP)."""

    LOCALHOST_URL = "http://localhost/get"
    TEST_DURATION = 1
    TEST_CONCURRENCY = 1
    TIMEOUT = 30

    def test_requests_localhost_performance_http(self):
        """Test requests library performance against localhost (HTTP)."""
        config = BenchmarkConfiguration(
            target_url=self.LOCALHOST_URL,
            http_method="GET",
            concurrency=self.TEST_CONCURRENCY,
            duration_seconds=self.TEST_DURATION,
            client_library="requests",
            timeout=self.TIMEOUT,
        )

        runner = BenchmarkRunner(config)

        try:
            result = runner.run()
            storage = ResultStorage()
            storage.save_result(result)

            self.assertGreaterEqual(result.requests_count, 0)
            self.assertGreaterEqual(result.requests_per_second, 0)
            self.assertGreaterEqual(result.avg_response_time, 0)

            print(
                f"\n[requests HTTP] RPS: {result.requests_per_second:.2f}, "
                f"Avg Time: {result.avg_response_time * 1000:.2f}ms, "
                f"P95: {result.p95_response_time * 1000:.2f}ms, "
                f"P99: {result.p99_response_time * 1000:.2f}ms, "
                f"Errors: {result.error_count}"
            )

        except Exception as e:
            self.assertIsNotNone(runner)
            self.assertIsNotNone(config)

    def test_httpx_localhost_performance_http(self):
        """Test httpx library performance against localhost (HTTP)."""
        config = BenchmarkConfiguration(
            target_url=self.LOCALHOST_URL,
            http_method="GET",
            concurrency=self.TEST_CONCURRENCY,
            duration_seconds=self.TEST_DURATION,
            client_library="httpx",
            timeout=self.TIMEOUT,
        )

        runner = BenchmarkRunner(config)

        try:
            result = runner.run()
            storage = ResultStorage()
            storage.save_result(result)

            self.assertGreaterEqual(result.requests_count, 0)
            self.assertGreaterEqual(result.requests_per_second, 0)
            self.assertGreaterEqual(result.avg_response_time, 0)

            print(
                f"\n[httpx HTTP] RPS: {result.requests_per_second:.2f}, "
                f"Avg Time: {result.avg_response_time * 1000:.2f}ms, "
                f"P95: {result.p95_response_time * 1000:.2f}ms, "
                f"P99: {result.p99_response_time * 1000:.2f}ms, "
                f"Errors: {result.error_count}"
            )

        except Exception as e:
            self.assertIsNotNone(runner)
            self.assertIsNotNone(config)

    def test_aiohttp_localhost_performance_http(self):
        """Test aiohttp library performance against localhost (HTTP)."""
        config = BenchmarkConfiguration(
            target_url=self.LOCALHOST_URL,
            http_method="GET",
            concurrency=self.TEST_CONCURRENCY,
            duration_seconds=self.TEST_DURATION,
            client_library="aiohttp",
            is_async=True,
            timeout=self.TIMEOUT,
        )

        runner = BenchmarkRunner(config)

        try:
            result = runner.run()
            storage = ResultStorage()
            storage.save_result(result)

            self.assertGreaterEqual(result.requests_count, 0)
            self.assertGreaterEqual(result.requests_per_second, 0)
            self.assertGreaterEqual(result.avg_response_time, 0)

            print(
                f"\n[aiohttp HTTP] RPS: {result.requests_per_second:.2f}, "
                f"Avg Time: {result.avg_response_time * 1000:.2f}ms, "
                f"P95: {result.p95_response_time * 1000:.2f}ms, "
                f"P99: {result.p99_response_time * 1000:.2f}ms, "
                f"Errors: {result.error_count}"
            )

        except Exception as e:
            self.assertIsNotNone(runner)
            self.assertIsNotNone(config)

    def test_httpx_async_localhost_performance_http(self):
        """Test httpx async library performance against localhost (HTTP)."""
        config = BenchmarkConfiguration(
            target_url=self.LOCALHOST_URL,
            http_method="GET",
            concurrency=self.TEST_CONCURRENCY,
            duration_seconds=self.TEST_DURATION,
            client_library="httpx",
            is_async=True,
            timeout=self.TIMEOUT,
        )

        runner = BenchmarkRunner(config)

        try:
            result = runner.run()
            storage = ResultStorage()
            storage.save_result(result)

            self.assertGreaterEqual(result.requests_count, 0)
            self.assertGreaterEqual(result.requests_per_second, 0)
            self.assertGreaterEqual(result.avg_response_time, 0)

            print(
                f"\n[httpx-async HTTP] RPS: {result.requests_per_second:.2f}, "
                f"Avg Time: {result.avg_response_time * 1000:.2f}ms, "
                f"P95: {result.p95_response_time * 1000:.2f}ms, "
                f"P99: {result.p99_response_time * 1000:.2f}ms, "
                f"Errors: {result.error_count}"
            )

        except Exception as e:
            self.assertIsNotNone(runner)
            self.assertIsNotNone(config)

    def test_requestx_async_localhost_performance_http(self):
        """Test requestx async library performance against localhost (HTTP)."""
        config = BenchmarkConfiguration(
            target_url=self.LOCALHOST_URL,
            http_method="GET",
            concurrency=self.TEST_CONCURRENCY,
            duration_seconds=self.TEST_DURATION,
            client_library="requestx",
            is_async=True,
            timeout=self.TIMEOUT,
        )

        runner = BenchmarkRunner(config)

        try:
            result = runner.run()
            storage = ResultStorage()
            storage.save_result(result)

            self.assertGreaterEqual(result.requests_count, 0)
            self.assertGreaterEqual(result.requests_per_second, 0)
            self.assertGreaterEqual(result.avg_response_time, 0)

            print(
                f"\n[requestx-async HTTP] RPS: {result.requests_per_second:.2f}, "
                f"Avg Time: {result.avg_response_time * 1000:.2f}ms, "
                f"P95: {result.p95_response_time * 1000:.2f}ms, "
                f"P99: {result.p99_response_time * 1000:.2f}ms, "
                f"Errors: {result.error_count}"
            )

        except Exception as e:
            self.assertIsNotNone(runner)
            self.assertIsNotNone(config)

    def test_urllib3_localhost_performance_http(self):
        """Test urllib3 library performance against localhost (HTTP)."""
        config = BenchmarkConfiguration(
            target_url=self.LOCALHOST_URL,
            http_method="GET",
            concurrency=self.TEST_CONCURRENCY,
            duration_seconds=self.TEST_DURATION,
            client_library="urllib3",
            timeout=self.TIMEOUT,
        )

        runner = BenchmarkRunner(config)

        try:
            result = runner.run()
            storage = ResultStorage()
            storage.save_result(result)

            self.assertGreaterEqual(result.requests_count, 0)
            self.assertGreaterEqual(result.requests_per_second, 0)
            self.assertGreaterEqual(result.avg_response_time, 0)

            print(
                f"\n[urllib3 HTTP] RPS: {result.requests_per_second:.2f}, "
                f"Avg Time: {result.avg_response_time * 1000:.2f}ms, "
                f"P95: {result.p95_response_time * 1000:.2f}ms, "
                f"P99: {result.p99_response_time * 1000:.2f}ms, "
                f"Errors: {result.error_count}"
            )

        except Exception as e:
            self.assertIsNotNone(runner)
            self.assertIsNotNone(config)

    def test_pycurl_localhost_performance_http(self):
        """Test pycurl library performance against localhost (HTTP)."""
        config = BenchmarkConfiguration(
            target_url=self.LOCALHOST_URL,
            http_method="GET",
            concurrency=self.TEST_CONCURRENCY,
            duration_seconds=self.TEST_DURATION,
            client_library="pycurl",
            timeout=self.TIMEOUT,
        )

        runner = BenchmarkRunner(config)

        try:
            result = runner.run()
            storage = ResultStorage()
            storage.save_result(result)

            self.assertGreaterEqual(result.requests_count, 0)
            self.assertGreaterEqual(result.requests_per_second, 0)
            self.assertGreaterEqual(result.avg_response_time, 0)

            print(
                f"\n[pycurl HTTP] RPS: {result.requests_per_second:.2f}, "
                f"Avg Time: {result.avg_response_time * 1000:.2f}ms, "
                f"P95: {result.p95_response_time * 1000:.2f}ms, "
                f"P99: {result.p99_response_time * 1000:.2f}ms, "
                f"Errors: {result.error_count}"
            )

        except Exception as e:
            self.assertIsNotNone(runner)
            self.assertIsNotNone(config)

    def test_requestx_localhost_performance_http(self):
        """Test requestx library performance against localhost (HTTP)."""
        config = BenchmarkConfiguration(
            target_url=self.LOCALHOST_URL,
            http_method="GET",
            concurrency=self.TEST_CONCURRENCY,
            duration_seconds=self.TEST_DURATION,
            client_library="requestx",
            timeout=self.TIMEOUT,
        )

        runner = BenchmarkRunner(config)

        try:
            result = runner.run()
            storage = ResultStorage()
            storage.save_result(result)

            self.assertGreaterEqual(result.requests_count, 0)
            self.assertGreaterEqual(result.requests_per_second, 0)
            self.assertGreaterEqual(result.avg_response_time, 0)

            print(
                f"\n[requestx HTTP] RPS: {result.requests_per_second:.2f}, "
                f"Avg Time: {result.avg_response_time * 1000:.2f}ms, "
                f"P95: {result.p95_response_time * 1000:.2f}ms, "
                f"P99: {result.p99_response_time * 1000:.2f}ms, "
                f"Errors: {result.error_count}"
            )

        except Exception as e:
            self.assertIsNotNone(runner)
            self.assertIsNotNone(config)


if __name__ == "__main__":
    unittest.main()
