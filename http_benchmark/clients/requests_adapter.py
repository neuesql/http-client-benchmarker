"""Requests HTTP client adapter for the HTTP benchmark framework."""

import requests
from typing import Dict, Any
from .base import BaseHTTPAdapter
from ..models.http_request import HTTPRequest


class RequestsAdapter(BaseHTTPAdapter):
    """HTTP adapter for the requests library."""

    def __init__(self):
        super().__init__("requests")
        self.session = requests.Session()

    def make_request(self, request: HTTPRequest) -> Dict[str, Any]:
        """Make an HTTP request using the requests library."""
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
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                timeout=timeout,
                verify=verify_ssl,
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
        """Make an async HTTP request using the requests library.

        Note: The requests library is synchronous, so this just calls the sync version.
        For true async support, use the httpx or aiohttp adapters.
        """
        return self.make_request(request)

    def close(self) -> None:
        """Close the requests session."""
        self.session.close()
