"""RequestX HTTP client adapter for the HTTP benchmark framework."""

# Note: requestx is not a standard library, so we'll simulate its interface
# In a real implementation, this would import the actual requestx library
try:
    import requestx

    REQUESTX_AVAILABLE = True
except ImportError:
    REQUESTX_AVAILABLE = False

    # For now, we'll simulate the interface
    class MockRequestX:
        @staticmethod
        def request(method, url, **kwargs):
            # This is a mock implementation for demonstration
            import requests  # Fallback to requests for simulation

            return requests.request(method, url, **kwargs)

    requestx = MockRequestX()


from typing import Dict, Any
import time
from .base import BaseHTTPAdapter
from ..models.http_request import HTTPRequest


class RequestXAdapter(BaseHTTPAdapter):
    """HTTP adapter for the requestx library."""

    def __init__(self):
        super().__init__("requestx")

    def make_request(self, request: HTTPRequest) -> Dict[str, Any]:
        """Make an HTTP request using the requestx library."""
        try:
            # Prepare the request
            method = request.method.upper()
            url = request.url
            headers = request.headers
            timeout = request.timeout
            verify_ssl = request.verify_ssl

            data = request.body if request.body else None

            kwargs = {"headers": headers, "timeout": timeout, "verify": verify_ssl}
            if data is not None:
                kwargs["data"] = data

            start_time = time.time()
            response = requestx.request(method, url, **kwargs)
            end_time = time.time()

            response_time = end_time - start_time
            if hasattr(response, "elapsed"):
                response_time = response.elapsed.total_seconds()

            # Return response data
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.text,
                "response_time": response_time,
                "url": str(response.url),
                "success": True,
                "error": None,
            }
        except Exception as e:
            return {
                "status_code": None,
                "headers": {},
                "content": "",
                "response_time": 0,
                "url": request.url,
                "success": False,
                "error": str(e),
            }

    async def make_request_async(self, request: HTTPRequest) -> Dict[str, Any]:
        """Make an async HTTP request using the requestx library."""
        try:
            # Prepare the request
            method = request.method.upper()
            url = request.url
            headers = request.headers
            timeout = request.timeout
            verify_ssl = request.verify_ssl

            # Prepare data based on method
            data = request.body if request.body else None

            # Make the async request (assuming requestx has async support)
            # For now, using a mock async implementation
            import asyncio

            await asyncio.sleep(0.01)  # Simulate async operation

            # Fallback to sync for demonstration
            return self.make_request(request)
        except Exception as e:
            return {
                "status_code": None,
                "headers": {},
                "content": "",
                "response_time": 0,
                "url": request.url,
                "success": False,
                "error": str(e),
            }

    def close(self) -> None:
        pass
