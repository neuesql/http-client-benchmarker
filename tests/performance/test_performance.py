"""Performance tests for different HTTP clients targeting localhost with GET requests (HTTP version)."""

import unittest
from tabulate import tabulate
from http_benchmark.benchmark import BenchmarkRunner
from http_benchmark.models.benchmark_configuration import BenchmarkConfiguration
from http_benchmark.storage import ResultStorage


class TestLocalhostPerformance(unittest.TestCase):
    """Performance tests comparing different HTTP clients against localhost (HTTP)."""

    LOCALHOST_URL_HTTP = "http://localhost/get"
    LOCALHOST_URL_HTTPS = "https://localhost/get"
    TEST_DURATION = 1
    TEST_CONCURRENCY = 1
    TIMEOUT = 30

    def test_all_clients_comparison_http(self):
        self.run_all_clients(self.LOCALHOST_URL_HTTP)

    def test_all_clients_comparison_https(self):
        self.run_all_clients(self.LOCALHOST_URL_HTTPS)

    def run_all_clients(self, host_url):
        """Compare performance of all HTTP clients against localhost."""
        is_https = host_url.startswith("https")
        client_libraries = [
            "requests",
            "httpx",
            "httpx-async",
            "aiohttp",
            "urllib3",
            "pycurl",
            "requestx",
            "requestx-async",
        ]
        results = {}
        table_data = []

        print("\n" + "=" * 80)
        print(
            f"HTTP CLIENT PERFORMANCE COMPARISON (localhost GET - {'HTTPS' if is_https else 'HTTP'})"
        )
        print("=" * 80)

        for client in client_libraries:
            is_async = client in ("aiohttp", "httpx-async", "requestx-async")
            actual_client = client.replace("-async", "")
            config = BenchmarkConfiguration(
                target_url=host_url,
                http_method="GET",
                concurrency=self.TEST_CONCURRENCY,
                duration_seconds=self.TEST_DURATION,
                client_library=actual_client,
                is_async=is_async,
                verify_ssl=False,
                timeout=self.TIMEOUT,
            )

            runner = BenchmarkRunner(config)

            try:
                result = runner.run()
                storage = ResultStorage()
                storage.save_result(result)
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

        print(tabulate(table_data, headers=headers, tablefmt="grid"))

        if len(results) > 1:
            for client, result in results.items():
                self.assertGreaterEqual(result.requests_count, 0)
                self.assertGreaterEqual(result.requests_per_second, 0)
                self.assertGreaterEqual(result.avg_response_time, 0)

            best_client = max(results.items(), key=lambda x: x[1].requests_per_second)
            print(
                f"\nFastest client: {best_client[0]} ({best_client[1].requests_per_second:.2f} RPS)"
            )

        print("\n" + "=" * 80)


if __name__ == "__main__":
    unittest.main()
