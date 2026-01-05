import unittest
from http_benchmark.clients.requests_adapter import RequestsAdapter
from http_benchmark.clients.httpx_adapter import HttpxAdapter
from http_benchmark.clients.aiohttp_adapter import AiohttpAdapter
from http_benchmark.clients.urllib3_adapter import Urllib3Adapter
from http_benchmark.clients.pycurl_adapter import PycurlAdapter
from http_benchmark.clients.requestx_adapter import RequestXAdapter
from http_benchmark.models.http_request import HTTPRequest


class TestRequestsAdapter(unittest.TestCase):
    def test_adapter_initialization(self):
        """Test RequestsAdapter initialization."""
        adapter = RequestsAdapter()
        self.assertEqual(adapter.name, "requests")

    def test_get_supported_methods(self):
        """Test supported HTTP methods for requests adapter."""
        adapter = RequestsAdapter()
        methods = adapter.get_supported_methods()
        self.assertIn('GET', methods)
        self.assertIn('POST', methods)
        self.assertIn('PUT', methods)
        self.assertIn('DELETE', methods)
        self.assertIn('PATCH', methods)
        self.assertIn('HEAD', methods)
        self.assertIn('OPTIONS', methods)

    def test_make_request_method_exists(self):
        """Test that make_request method exists."""
        adapter = RequestsAdapter()
        self.assertTrue(callable(getattr(adapter, 'make_request', None)))

    def test_make_request_async_method_exists(self):
        """Test that make_request_async method exists."""
        adapter = RequestsAdapter()
        self.assertTrue(callable(getattr(adapter, 'make_request_async', None)))


class TestHttpxAdapter(unittest.TestCase):
    def test_adapter_initialization(self):
        """Test HttpxAdapter initialization."""
        adapter = HttpxAdapter()
        self.assertEqual(adapter.name, "httpx")

    def test_get_supported_methods(self):
        """Test supported HTTP methods for httpx adapter."""
        adapter = HttpxAdapter()
        methods = adapter.get_supported_methods()
        self.assertIn('GET', methods)
        self.assertIn('POST', methods)
        self.assertIn('PUT', methods)
        self.assertIn('DELETE', methods)
        self.assertIn('PATCH', methods)
        self.assertIn('HEAD', methods)
        self.assertIn('OPTIONS', methods)

    def test_make_request_method_exists(self):
        """Test that make_request method exists."""
        adapter = HttpxAdapter()
        self.assertTrue(callable(getattr(adapter, 'make_request', None)))

    def test_make_request_async_method_exists(self):
        """Test that make_request_async method exists."""
        adapter = HttpxAdapter()
        self.assertTrue(callable(getattr(adapter, 'make_request_async', None)))


class TestAiohttpAdapter(unittest.TestCase):
    def test_adapter_initialization(self):
        """Test AiohttpAdapter initialization."""
        adapter = AiohttpAdapter()
        self.assertEqual(adapter.name, "aiohttp")

    def test_get_supported_methods(self):
        """Test supported HTTP methods for aiohttp adapter."""
        adapter = AiohttpAdapter()
        methods = adapter.get_supported_methods()
        self.assertIn('GET', methods)
        self.assertIn('POST', methods)
        self.assertIn('PUT', methods)
        self.assertIn('DELETE', methods)
        self.assertIn('PATCH', methods)
        self.assertIn('HEAD', methods)
        self.assertIn('OPTIONS', methods)

    def test_make_request_method_exists(self):
        """Test that make_request method exists."""
        adapter = AiohttpAdapter()
        self.assertTrue(callable(getattr(adapter, 'make_request', None)))

    def test_make_request_async_method_exists(self):
        """Test that make_request_async method exists."""
        adapter = AiohttpAdapter()
        self.assertTrue(callable(getattr(adapter, 'make_request_async', None)))


class TestUrllib3Adapter(unittest.TestCase):
    def test_adapter_initialization(self):
        """Test Urllib3Adapter initialization."""
        adapter = Urllib3Adapter()
        self.assertEqual(adapter.name, "urllib3")

    def test_get_supported_methods(self):
        """Test supported HTTP methods for urllib3 adapter."""
        adapter = Urllib3Adapter()
        methods = adapter.get_supported_methods()
        self.assertIn('GET', methods)
        self.assertIn('POST', methods)
        self.assertIn('PUT', methods)
        self.assertIn('DELETE', methods)
        self.assertIn('PATCH', methods)
        self.assertIn('HEAD', methods)
        self.assertIn('OPTIONS', methods)

    def test_make_request_method_exists(self):
        """Test that make_request method exists."""
        adapter = Urllib3Adapter()
        self.assertTrue(callable(getattr(adapter, 'make_request', None)))

    def test_make_request_async_method_exists(self):
        """Test that make_request_async method exists."""
        adapter = Urllib3Adapter()
        self.assertTrue(callable(getattr(adapter, 'make_request_async', None)))


class TestPycurlAdapter(unittest.TestCase):
    def test_adapter_initialization(self):
        """Test PycurlAdapter initialization."""
        adapter = PycurlAdapter()
        self.assertEqual(adapter.name, "pycurl")

    def test_get_supported_methods(self):
        """Test supported HTTP methods for pycurl adapter."""
        adapter = PycurlAdapter()
        methods = adapter.get_supported_methods()
        self.assertIn('GET', methods)
        self.assertIn('POST', methods)
        self.assertIn('PUT', methods)
        self.assertIn('DELETE', methods)
        self.assertIn('PATCH', methods)
        self.assertIn('HEAD', methods)
        self.assertIn('OPTIONS', methods)

    def test_make_request_method_exists(self):
        """Test that make_request method exists."""
        adapter = PycurlAdapter()
        self.assertTrue(callable(getattr(adapter, 'make_request', None)))

    def test_make_request_async_method_exists(self):
        """Test that make_request_async method exists."""
        adapter = PycurlAdapter()
        self.assertTrue(callable(getattr(adapter, 'make_request_async', None)))


class TestRequestXAdapter(unittest.TestCase):
    def test_adapter_initialization(self):
        """Test RequestXAdapter initialization."""
        adapter = RequestXAdapter()
        self.assertEqual(adapter.name, "requestx")

    def test_get_supported_methods(self):
        """Test supported HTTP methods for requestx adapter."""
        adapter = RequestXAdapter()
        methods = adapter.get_supported_methods()
        self.assertIn('GET', methods)
        self.assertIn('POST', methods)
        self.assertIn('PUT', methods)
        self.assertIn('DELETE', methods)
        self.assertIn('PATCH', methods)
        self.assertIn('HEAD', methods)
        self.assertIn('OPTIONS', methods)

    def test_make_request_method_exists(self):
        """Test that make_request method exists."""
        adapter = RequestXAdapter()
        self.assertTrue(callable(getattr(adapter, 'make_request', None)))

    def test_make_request_async_method_exists(self):
        """Test that make_request_async method exists."""
        adapter = RequestXAdapter()
        self.assertTrue(callable(getattr(adapter, 'make_request_async', None)))


class TestBaseAdapterInterface(unittest.TestCase):
    def test_all_adapters_implement_required_methods(self):
        """Test that all adapters implement the required interface methods."""
        adapters = [
            RequestsAdapter(),
            HttpxAdapter(),
            AiohttpAdapter(),
            Urllib3Adapter(),
            PycurlAdapter(),
            RequestXAdapter()
        ]
        
        for adapter in adapters:
            with self.subTest(adapter=adapter.name):
                self.assertTrue(hasattr(adapter, 'make_request'))
                self.assertTrue(hasattr(adapter, 'make_request_async'))
                self.assertTrue(hasattr(adapter, 'get_supported_methods'))
                self.assertTrue(callable(getattr(adapter, 'make_request')))
                self.assertTrue(callable(getattr(adapter, 'make_request_async')))
                self.assertTrue(callable(getattr(adapter, 'get_supported_methods')))


if __name__ == '__main__':
    unittest.main()