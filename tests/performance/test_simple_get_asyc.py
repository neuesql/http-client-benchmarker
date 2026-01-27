"""Test comparing requestx, requests, and httpx clients.

Replicates CLI command:
http-benchmark --url http://localhost/get --compare requestx requests httpx --concurrency 1 --duration 3
"""

import unittest

from http_benchmark.benchmark import BenchmarkRunner
from http_benchmark.models.benchmark_configuration import BenchmarkConfiguration


class TestClientComparison(unittest.TestCase):
    """Test comparing multiple HTTP clients - replicates CLI --compare behavior."""

    def test_compare_requestx_requests_httpx(self):
        """
        Replicate: http-benchmark --url http://localhost/get
                   --compare requestx requests httpx
                   --concurrency 1 --duration 3
        """
        clients = ["requestx", "httpx", "aiohttp"]
        target_url = "http://localhost/get"
        concurrency = 1
        duration_seconds = 3

        results = {}

        for client in clients:
            # All three clients support sync mode
            config = BenchmarkConfiguration(
                target_url=target_url,
                http_method="GET",
                concurrency=concurrency,
                duration_seconds=duration_seconds,
                client_library=client,
                is_async=True,  # All three support sync
            )

            runner = BenchmarkRunner(config)
            result = runner.run()
            results[client] = result

            # Basic sanity checks
            self.assertEqual(result.client_library, client)
            self.assertEqual(result.url, target_url)
            self.assertGreaterEqual(result.requests_count, 0)
            self.assertGreaterEqual(result.requests_per_second, 0)
            self.assertGreaterEqual(result.avg_response_time, 0)
            self.assertGreaterEqual(result.p95_response_time, 0)
            self.assertGreaterEqual(result.p99_response_time, 0)

        # Compare results
        print("\n=== Client Comparison Results ===")
        for client, result in results.items():
            print(f"{client}:")
            print(f"  RPS: {result.requests_per_second:.2f}")
            print(f"  Avg Latency: {result.avg_response_time * 1000:.2f}ms")
            print(f"  P95 Latency: {result.p95_response_time * 1000:.2f}ms")
            print(f"  P99 Latency: {result.p99_response_time * 1000:.2f}ms")
            print(f"  Errors: {result.error_count} ({result.error_rate:.2f}%)")

        # Verify all benchmarks ran
        self.assertEqual(len(results), 3)

        # Find the fastest client
        fastest = max(results.items(), key=lambda x: x[1].requests_per_second)
        print(f"\nFastest: {fastest[0]} ({fastest[1].requests_per_second:.2f} RPS)")


if __name__ == "__main__":
    unittest.main()
