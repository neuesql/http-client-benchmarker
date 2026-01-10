"""HTTPX HTTP client adapter for the HTTP benchmark framework."""

import asyncio
from typing import Any, Dict

import httpx

from ..models.http_request import HTTPRequest
from .base import BaseHTTPAdapter


class HttpxAdapter(BaseHTTPAdapter):
    """HTTP adapter for the httpx library."""

    def __init__(self):
        super().__init__("httpx")
        self.client = None
        self.async_client = None
        self.verify_ssl = True

    def __enter__(self):
        """Initialize sync client when entering sync context."""
        self.client = httpx.Client(verify=self.verify_ssl)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close sync client when exiting sync context."""
        if self.client:
            self.client.close()

    async def __aenter__(self):
        """Initialize async client when entering async context."""
        self.async_client = httpx.AsyncClient(verify=self.verify_ssl)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close async client when exiting async context."""
        if self.async_client:
            await self.async_client.aclose()

    def make_request(self, request: HTTPRequest) -> Dict[str, Any]:
        """Make an HTTP request using the httpx library."""
        try:
            method = request.method.upper()
            url = request.url
            headers = request.headers
            timeout = request.timeout

            data = request.body if request.body else None

            response = self.client.request(method=method, url=url, headers=headers, content=data, timeout=timeout)

            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.text,
                "response_time": response.elapsed.total_seconds(),
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
        """Make an async HTTP request using the httpx library."""
        try:
            method = request.method.upper()
            url = request.url
            headers = request.headers
            timeout = request.timeout

            data = request.body if request.body else None

            start_time = asyncio.get_event_loop().time()
            response = await self.async_client.request(method=method, url=url, headers=headers, content=data, timeout=timeout)
            end_time = asyncio.get_event_loop().time()

            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.text,
                "response_time": end_time - start_time,
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
