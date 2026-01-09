"""RequestX HTTP client adapter for the HTTP benchmark framework."""

import time
import asyncio
from typing import Any, Dict

import requestx

from ..models.http_request import HTTPRequest
from .base import BaseHTTPAdapter


class RequestXAdapter(BaseHTTPAdapter):
    """HTTP adapter for the requestx library."""

    def __init__(self):
        super().__init__("requestx")
        self.session = None
        self.async_session = None

    def __enter__(self):
        """Initialize session when entering sync context."""
        self.session = requestx.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close session when exiting sync context."""
        if self.session:
            self.session.close()

    async def __aenter__(self):
        """Initialize session when entering async context."""
        self.async_session = requestx.Session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close session when exiting async context."""
        if self.async_session:
            self.async_session.close()

    def make_request(self, request: HTTPRequest) -> Dict[str, Any]:
        """Make an HTTP request using the requestx library."""
        try:
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
            response = self.session.request(method, url, **kwargs)
            end_time = time.time()

            response_time = end_time - start_time
            if hasattr(response, "elapsed"):
                response_time = response.elapsed.total_seconds()

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
            method = request.method.upper()
            url = request.url
            headers = request.headers
            timeout = request.timeout
            verify_ssl = request.verify_ssl

            data = request.body if request.body else None

            kwargs = {"headers": headers, "timeout": timeout, "verify": verify_ssl}
            if data is not None:
                kwargs["data"] = data

            start_time = asyncio.get_event_loop().time()
            response = await self.async_session.request(method, url, **kwargs)
            end_time = asyncio.get_event_loop().time()

            response_time = end_time - start_time
            if hasattr(response, "elapsed"):
                response_time = response.elapsed.total_seconds()

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
