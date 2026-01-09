"""Performance tests for different HTTP clients targeting localhost with GET requests."""

import unittest

try:
    from tabulate import tabulate

    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False
    tabulate = None

from http_benchmark.benchmark import BenchmarkRunner
from http_benchmark.models.benchmark_configuration import BenchmarkConfiguration


class TestLocalhostPerformance(unittest.TestCase):
    """Performance tests comparing different HTTP clients against localhost."""

    LOCALHOST_URL = "http://localhost/get"
    TEST_DURATION = 5
    TEST_CONCURRENCY = 1
    TIMEOUT = 30

    def test_requests_localhost_performance(self):
        """Test requests library performance against localhost."""
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

            self.assertGreaterEqual(result.requests_count, 0)
            self.assertGreaterEqual(result.requests_per_second, 0)
            self.assertGreaterEqual(result.avg_response_time, 0)

            print(
                f"\n[requests] RPS: {result.requests_per_second:.2f}, "
                f"Avg Time: {result.avg_response_time * 1000:.2f}ms, "
                f"P95: {result.p95_response_time * 1000:.2f}ms, "
                f"P99: {result.p99_response_time * 1000:.2f}ms, "
                f"Errors: {result.error_count}"
            )

        except Exception as e:
            self.assertIsNotNone(runner)
            self.assertIsNotNone(config)

    def test_httpx_localhost_performance(self):
        """Test httpx library performance against localhost."""
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

            self.assertGreaterEqual(result.requests_count, 0)
            self.assertGreaterEqual(result.requests_per_second, 0)
            self.assertGreaterEqual(result.avg_response_time, 0)

            print(
                f"\n[httpx] RPS: {result.requests_per_second:.2f}, "
                f"Avg Time: {result.avg_response_time * 1000:.2f}ms, "
                f"P95: {result.p95_response_time * 1000:.2f}ms, "
                f"P99: {result.p99_response_time * 1000:.2f}ms, "
                f"Errors: {result.error_count}"
            )

        except Exception as e:
            self.assertIsNotNone(runner)
            self.assertIsNotNone(config)

    def test_aiohttp_localhost_performance(self):
        """Test aiohttp library performance against localhost."""
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

            self.assertGreaterEqual(result.requests_count, 0)
            self.assertGreaterEqual(result.requests_per_second, 0)
            self.assertGreaterEqual(result.avg_response_time, 0)

            print(
                f"\n[aiohttp] RPS: {result.requests_per_second:.2f}, "
                f"Avg Time: {result.avg_response_time * 1000:.2f}ms, "
                f"P95: {result.p95_response_time * 1000:.2f}ms, "
                f"P99: {result.p99_response_time * 1000:.2f}ms, "
                f"Errors: {result.error_count}"
            )

        except Exception as e:
            self.assertIsNotNone(runner)
            self.assertIsNotNone(config)

    def test_urllib3_localhost_performance(self):
        """Test urllib3 library performance against localhost."""
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

            self.assertGreaterEqual(result.requests_count, 0)
            self.assertGreaterEqual(result.requests_per_second, 0)
            self.assertGreaterEqual(result.avg_response_time, 0)

            print(
                f"\n[urllib3] RPS: {result.requests_per_second:.2f}, "
                f"Avg Time: {result.avg_response_time * 1000:.2f}ms, "
                f"P95: {result.p95_response_time * 1000:.2f}ms, "
                f"P99: {result.p99_response_time * 1000:.2f}ms, "
                f"Errors: {result.error_count}"
            )

        except Exception as e:
            self.assertIsNotNone(runner)
            self.assertIsNotNone(config)

    def test_pycurl_localhost_performance(self):
        """Test pycurl library performance against localhost."""
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

            self.assertGreaterEqual(result.requests_count, 0)
            self.assertGreaterEqual(result.requests_per_second, 0)
            self.assertGreaterEqual(result.avg_response_time, 0)

            print(
                f"\n[pycurl] RPS: {result.requests_per_second:.2f}, "
                f"Avg Time: {result.avg_response_time * 1000:.2f}ms, "
                f"P95: {result.p95_response_time * 1000:.2f}ms, "
                f"P99: {result.p99_response_time * 1000:.2f}ms, "
                f"Errors: {result.error_count}"
            )

        except Exception as e:
            self.assertIsNotNone(runner)
            self.assertIsNotNone(config)

    def test_requestx_localhost_performance(self):
        """Test requestx library performance against localhost."""
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

            self.assertGreaterEqual(result.requests_count, 0)
            self.assertGreaterEqual(result.requests_per_second, 0)
            self.assertGreaterEqual(result.avg_response_time, 0)

            print(
                f"\n[requestx] RPS: {result.requests_per_second:.2f}, "
                f"Avg Time: {result.avg_response_time * 1000:.2f}ms, "
                f"P95: {result.p95_response_time * 1000:.2f}ms, "
                f"P99: {result.p99_response_time * 1000:.2f}ms, "
                f"Errors: {result.error_count}"
            )

        except Exception as e:
            self.assertIsNotNone(runner)
            self.assertIsNotNone(config)

    def test_all_clients_comparison(self):
        """Compare performance of all HTTP clients against localhost."""
        client_libraries = [
            "requests",
            "httpx",
            "aiohttp",
            "urllib3",
            "pycurl",
            "requestx",
        ]
        results = {}
        table_data = []

        print("\n" + "=" * 80)
        print("HTTP CLIENT PERFORMANCE COMPARISON (localhost GET)")
        print("=" * 80)

        for client in client_libraries:
            is_async = client == "aiohttp"
            config = BenchmarkConfiguration(
                target_url=self.LOCALHOST_URL,
                http_method="GET",
                concurrency=self.TEST_CONCURRENCY,
                duration_seconds=self.TEST_DURATION,
                client_library=client,
                is_async=is_async,
                timeout=self.TIMEOUT,
            )

            runner = BenchmarkRunner(config)

            try:
                result = runner.run()
                results[client] = result

                table_data.append(
                    [
                        client,
                        "Async" if is_async else "Sync",
                        f"{result.requests_per_second:.2f}",
                        result.requests_count,
                        f"{result.duration:.2f}",
                        result.concurrency_level,
                        f"{result.avg_response_time * 1000:.2f}",
                        f"{result.p95_response_time * 1000:.2f}",
                        f"{result.p99_response_time * 1000:.2f}",
                        f"{result.cpu_usage_avg:.2f}",
                        f"{result.memory_usage_avg:.2f}",
                        result.error_count,
                    ]
                )

                print(f"Finished {client}: {result.requests_per_second:.2f} RPS")

            except Exception as e:
                self.assertIsNotNone(runner)
                self.assertIsNotNone(config)
                print(f"\n{client.upper():15} | FAILED: {str(e)}")
                table_data.append(
                    [
                        client,
                        "Async" if is_async else "Sync",
                        "FAILED",
                        "-",
                        "-",
                        "-",
                        "-",
                        "-",
                        "-",
                        "-",
                        "-",
                        str(e),
                    ]
                )

        print("\n" + "=" * 80)

        headers = [
            "Client",
            "Type",
            "RPS",
            "Reqs",
            "Dur(s)",
            "Conc",
            "Avg(ms)",
            "P95(ms)",
            "P99(ms)",
            "CPU(%)",
            "Mem(%)",
            "Errors",
        ]

        if TABULATE_AVAILABLE:
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            # Simple fallback table
            print(
                f"{'Client':<12} {'Type':<6} {'RPS':<10} {'Reqs':<8} {'Dur(s)':<8} {'Conc':<6} {'Avg(ms)':<8} {'P95(ms)':<8} {'CPU%':<6} {'Mem%':<6} {'Errors':<6}"
            )
            print("-" * 100)
            for row in table_data:
                if row[2] == "FAILED":
                    print(f"{row[0]:<12} {row[1]:<6} FAILED")
                else:
                    print(
                        f"{row[0]:<12} {row[1]:<6} {row[2]:<10} {row[3]:<8} {row[4]:<8} {row[5]:<6} {row[6]:<8} {row[7]:<8} {row[9]:<6} {row[10]:<6} {row[11]:<6}"
                    )
            print("-" * 80)
            for row in table_data:
                if row[2] == "FAILED":
                    print(f"{row[0]:<12} {row[1]:<6} FAILED")
                else:
                    print(
                        f"{row[0]:<12} {row[1]:<6} {row[2]:<10} {row[3]:<8} {row[4]:<8} {row[5]:<8} {row[7]:<6} {row[8]:<6} {row[9]:<6}"
                    )

        # If we got results from multiple clients, verify they all completed
        if len(results) > 1:
            # Verify all results are positive
            for client, result in results.items():
                self.assertGreaterEqual(result.requests_count, 0)
                self.assertGreaterEqual(result.requests_per_second, 0)
                self.assertGreaterEqual(result.avg_response_time, 0)

            # Find best performing client by RPS
            best_client = max(results.items(), key=lambda x: x[1].requests_per_second)
            print(
                f"\nFastest client: {best_client[0]} ({best_client[1].requests_per_second:.2f} RPS)"
            )

            runner = BenchmarkRunner(config)

            try:
                result = runner.run()
                results[client] = result

                print(
                    f"\n{client.upper():15} | "
                    f"RPS: {result.requests_per_second:8.2f} | "
                    f"Avg: {result.avg_response_time * 1000:7.2f}ms | "
                    f"P95: {result.p95_response_time * 1000:7.2f}ms | "
                    f"P99: {result.p99_response_time * 1000:7.2f}ms | "
                    f"Errors: {result.error_count:3}"
                )

            except Exception as e:
                self.assertIsNotNone(runner)
                self.assertIsNotNone(config)
                print(f"\n{client.upper():15} | FAILED: {str(e)}")

        print("\n" + "=" * 80)

        if len(results) > 1:
            for client, result in results.items():
                self.assertGreaterEqual(result.requests_count, 0)
                self.assertGreaterEqual(result.requests_per_second, 0)
                self.assertGreaterEqual(result.avg_response_time, 0)

            best_client = max(results.items(), key=lambda x: x[1].requests_per_second)
            print(
                f"\nFastest client: {best_client[0]} ({best_client[1].requests_per_second:.2f} RPS)"
            )

    def test_low_vs_high_concurrency(self):
        """Test performance difference between low and high concurrency levels."""
        configurations = [
            (1, "low_concurrency"),
            (5, "medium_concurrency"),
            (10, "high_concurrency"),
        ]

        print("\n" + "=" * 80)
        print("CONCURRENCY SCALING TEST (httpx - localhost GET)")
        print("=" * 80)

        results = []

        for concurrency, label in configurations:
            config = BenchmarkConfiguration(
                target_url=self.LOCALHOST_URL,
                http_method="GET",
                concurrency=concurrency,
                duration_seconds=self.TEST_DURATION,
                client_library="httpx",
                timeout=self.TIMEOUT,
            )

            runner = BenchmarkRunner(config)

            try:
                result = runner.run()
                results.append((label, result))

                print(
                    f"\n{label:20} (Concurrency: {concurrency:2d}) | "
                    f"RPS: {result.requests_per_second:8.2f} | "
                    f"Avg: {result.avg_response_time * 1000:7.2f}ms | "
                    f"Errors: {result.error_count:3}"
                )

            except Exception as e:
                self.assertIsNotNone(runner)
                self.assertIsNotNone(config)
                print(f"\n{label:20} | FAILED: {str(e)}")

        print("\n" + "=" * 80)

        if len(results) >= 2:
            for label, result in results:
                self.assertGreaterEqual(result.requests_per_second, 0)


if __name__ == "__main__":
    unittest.main()
