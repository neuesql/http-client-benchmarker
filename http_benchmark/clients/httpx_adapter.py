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
        self.client = httpx.Client()
        self.async_client = httpx.AsyncClient()

    def make_request(self, request: HTTPRequest) -> Dict[str, Any]:
        """Make an HTTP request using the httpx library."""
        try:
            # Prepare the request
            method = request.method.upper()
            url = request.url
            headers = request.headers
            timeout = request.timeout
            verify_ssl = request.verify_ssl

            # Prepare data based on method
            data = request.body if request.body else None

            # Make the request
            response = self.client.request(
                method=method, url=url, headers=headers, content=data, timeout=timeout
            )

            # Return response data
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
            # Prepare the request
            method = request.method.upper()
            url = request.url
            headers = request.headers
            timeout = request.timeout
            verify_ssl = request.verify_ssl

            # Prepare data based on method
            data = request.body if request.body else None

            # Make the async request
            start_time = asyncio.get_event_loop().time()
            response = await self.async_client.request(
                method=method, url=url, headers=headers, content=data, timeout=timeout
            )
            end_time = asyncio.get_event_loop().time()

            # Return response data
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

    def close(self) -> None:
        """Close the httpx clients."""
        if hasattr(self, "client"):
            self.client.close()

        if hasattr(self, "async_client"):
            try:
                loop = asyncio.get_event_loop()
                if not loop.is_running():
                    loop.run_until_complete(self.async_client.aclose())
            except Exception:
                pass

    async def close_async(self) -> None:
        """Close the httpx clients asynchronously."""
        if hasattr(self, "client"):
            self.client.close()

        if hasattr(self, "async_client"):
            await self.async_client.aclose()
