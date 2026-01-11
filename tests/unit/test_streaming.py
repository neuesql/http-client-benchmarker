"""Streaming tests for HTTP client adapters against httpbin.org/stream/2."""

import unittest
from http_benchmark.models.http_request import HTTPRequest
from http_benchmark.clients.requests_adapter import RequestsAdapter
from http_benchmark.clients.httpx_adapter import HttpxAdapter
from http_benchmark.clients.aiohttp_adapter import AiohttpAdapter
from http_benchmark.clients.urllib3_adapter import Urllib3Adapter
from http_benchmark.clients.pycurl_adapter import PycurlAdapter
from http_benchmark.clients.requestx_adapter import RequestXAdapter


class TestRequestsStreaming(unittest.TestCase):
    """Test streaming functionality for RequestsAdapter."""

    def setUp(self):
        self.adapter = RequestsAdapter()
        self.adapter.__enter__()
        self.request = HTTPRequest(
            method="GET",
            url="https://httpbin.org/stream/2",
            stream=True,
            timeout=30,
        )

    def tearDown(self):
        self.adapter.__exit__(None, None, None)

    def test_requests_stream_request(self):
        """Test streaming request with requests adapter."""
        result = self.adapter.make_request_stream(self.request)

        self.assertTrue(result["success"])
        self.assertEqual(result["status_code"], 200)
        self.assertTrue(result["streamed"])
        self.assertIn("chunk_count", result)
        self.assertGreater(result["chunk_count"], 0)
        # httpbin.org/stream/2 returns newline-delimited JSON
        self.assertIn("id", result["content"])
        self.assertIn('"id": 0', result["content"])


class TestHttpxStreaming(unittest.TestCase):
    """Test streaming functionality for HttpxAdapter."""

    def setUp(self):
        self.adapter = HttpxAdapter()
        self.adapter.__enter__()
        self.request = HTTPRequest(
            method="GET",
            url="https://httpbin.org/stream/2",
            stream=True,
            timeout=30,
        )

    def tearDown(self):
        self.adapter.__exit__(None, None, None)

    def test_httpx_stream_request(self):
        """Test streaming request with httpx adapter."""
        result = self.adapter.make_request_stream(self.request)

        self.assertTrue(result["success"])
        self.assertEqual(result["status_code"], 200)
        self.assertTrue(result["streamed"])
        self.assertIn("chunk_count", result)
        self.assertGreater(result["chunk_count"], 0)
        # httpbin.org/stream/2 returns newline-delimited JSON
        self.assertIn("id", result["content"])


class TestHttpxAsyncStreaming(unittest.IsolatedAsyncioTestCase):
    """Test async streaming functionality for HttpxAdapter."""

    async def asyncSetUp(self):
        self.adapter = HttpxAdapter()
        await self.adapter.__aenter__()
        self.request = HTTPRequest(
            method="GET",
            url="https://httpbin.org/stream/2",
            stream=True,
            timeout=30,
        )

    async def asyncTearDown(self):
        await self.adapter.__aexit__(None, None, None)

    async def test_httpx_stream_async_request(self):
        """Test async streaming request with httpx adapter."""
        result = await self.adapter.make_request_stream_async(self.request)

        self.assertTrue(result["success"])
        self.assertEqual(result["status_code"], 200)
        self.assertTrue(result["streamed"])
        self.assertIn("chunk_count", result)
        self.assertGreater(result["chunk_count"], 0)
        # httpbin.org/stream/2 returns newline-delimited JSON
        self.assertIn("id", result["content"])


class TestAiohttpStreaming(unittest.IsolatedAsyncioTestCase):
    """Test async streaming functionality for AiohttpAdapter."""

    async def asyncSetUp(self):
        self.adapter = AiohttpAdapter()
        await self.adapter.__aenter__()
        self.request = HTTPRequest(
            method="GET",
            url="https://httpbin.org/stream/2",
            stream=True,
            timeout=30,
        )

    async def asyncTearDown(self):
        await self.adapter.__aexit__(None, None, None)

    async def test_aiohttp_stream_async_request(self):
        """Test async streaming request with aiohttp adapter."""
        result = await self.adapter.make_request_stream_async(self.request)

        self.assertTrue(result["success"])
        self.assertEqual(result["status_code"], 200)
        self.assertTrue(result["streamed"])
        self.assertIn("chunk_count", result)
        self.assertGreater(result["chunk_count"], 0)
        # httpbin.org/stream/2 returns newline-delimited JSON
        self.assertIn("id", result["content"])


class TestUrllib3Streaming(unittest.TestCase):
    """Test streaming functionality for Urllib3Adapter."""

    def setUp(self):
        self.adapter = Urllib3Adapter()
        self.adapter.__enter__()
        self.request = HTTPRequest(
            method="GET",
            url="https://httpbin.org/stream/2",
            stream=True,
            timeout=30,
        )

    def tearDown(self):
        self.adapter.__exit__(None, None, None)

    def test_urllib3_stream_request(self):
        """Test streaming request with urllib3 adapter."""
        result = self.adapter.make_request_stream(self.request)

        self.assertTrue(result["success"])
        self.assertEqual(result["status_code"], 200)
        self.assertTrue(result["streamed"])
        self.assertIn("chunk_count", result)
        self.assertGreater(result["chunk_count"], 0)
        # httpbin.org/stream/2 returns newline-delimited JSON
        self.assertIn("id", result["content"])


class TestPycurlStreaming(unittest.TestCase):
    """Test streaming functionality for PycurlAdapter."""

    def setUp(self):
        self.adapter = PycurlAdapter()
        self.adapter.__enter__()
        self.request = HTTPRequest(
            method="GET",
            url="https://httpbin.org/stream/2",
            stream=True,
            timeout=30,
        )

    def tearDown(self):
        self.adapter.__exit__(None, None, None)

    def test_pycurl_stream_request(self):
        """Test streaming request with pycurl adapter."""
        result = self.adapter.make_request_stream(self.request)

        self.assertTrue(result["success"])
        self.assertEqual(result["status_code"], 200)
        self.assertTrue(result["streamed"])
        self.assertIn("chunk_count", result)
        self.assertGreater(result["chunk_count"], 0)
        # httpbin.org/stream/2 returns newline-delimited JSON
        self.assertIn("id", result["content"])


class TestRequestXStreaming(unittest.TestCase):
    """Test streaming functionality for RequestXAdapter."""

    def setUp(self):
        self.adapter = RequestXAdapter()
        self.adapter.__enter__()
        self.request = HTTPRequest(
            method="GET",
            url="https://httpbin.org/stream/2",
            stream=True,
            timeout=30,
        )

    def tearDown(self):
        self.adapter.__exit__(None, None, None)

    def test_requestx_stream_request(self):
        """Test streaming request with requestx adapter."""
        result = self.adapter.make_request_stream(self.request)

        self.assertTrue(result["success"])
        self.assertEqual(result["status_code"], 200)
        self.assertTrue(result["streamed"])
        self.assertIn("chunk_count", result)
        self.assertGreater(result["chunk_count"], 0)
        # httpbin.org/stream/2 returns newline-delimited JSON
        self.assertIn("id", result["content"])


class TestRequestXAsyncStreaming(unittest.IsolatedAsyncioTestCase):
    """Test async streaming functionality for RequestXAdapter."""

    async def asyncSetUp(self):
        self.adapter = RequestXAdapter()
        await self.adapter.__aenter__()
        self.request = HTTPRequest(
            method="GET",
            url="https://httpbin.org/stream/2",
            stream=True,
            timeout=30,
        )

    async def asyncTearDown(self):
        await self.adapter.__aexit__(None, None, None)

    async def test_requestx_stream_async_request(self):
        """Test async streaming request with requestx adapter."""
        result = await self.adapter.make_request_stream_async(self.request)

        self.assertTrue(result["success"])
        self.assertEqual(result["status_code"], 200)
        self.assertTrue(result["streamed"])
        self.assertIn("chunk_count", result)
        self.assertGreater(result["chunk_count"], 0)
        # httpbin.org/stream/2 returns newline-delimited JSON
        self.assertIn("id", result["content"])


class TestAllAdaptersStreamingInterface(unittest.TestCase):
    """Test that all adapters implement streaming interface."""

    def test_all_adapters_implement_streaming_methods(self):
        """Test that all adapters implement the required streaming interface methods."""
        adapters = [
            RequestsAdapter(),
            HttpxAdapter(),
            AiohttpAdapter(),
            Urllib3Adapter(),
            PycurlAdapter(),
            RequestXAdapter(),
        ]

        for adapter in adapters:
            with self.subTest(adapter=adapter.name):
                self.assertTrue(hasattr(adapter, "make_request_stream"))
                self.assertTrue(hasattr(adapter, "make_request_stream_async"))
                self.assertTrue(callable(getattr(adapter, "make_request_stream")))
                self.assertTrue(callable(getattr(adapter, "make_request_stream_async")))


if __name__ == "__main__":
    unittest.main()
