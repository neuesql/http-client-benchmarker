"""Urllib3 HTTP client adapter for the HTTP benchmark framework."""

import urllib3
import time
from typing import Dict, Any
from .base import BaseHTTPAdapter
from ..models.http_request import HTTPRequest


class Urllib3Adapter(BaseHTTPAdapter):
    """HTTP adapter for the urllib3 library."""

    def __init__(self):
        super().__init__("urllib3")
        # Disable SSL warnings if not verifying SSL
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.pool = urllib3.PoolManager()
        self.pool_no_verify = urllib3.PoolManager(
            cert_reqs="CERT_NONE", assert_hostname=False
        )

    def make_request(self, request: HTTPRequest) -> Dict[str, Any]:
        """Make an HTTP request using the urllib3 library."""
        try:
            # Prepare the request
            method = request.method.upper()
            url = request.url
            headers = request.headers
            timeout = request.timeout
            verify_ssl = request.verify_ssl

            # Select the appropriate pool manager
            http = self.pool if verify_ssl else self.pool_no_verify

            # Prepare data based on method
            body = request.body if request.body else None

            # Make the request
            start_time = time.time()
            response = http.request(
                method=method, url=url, headers=headers, body=body, timeout=timeout
            )
            end_time = time.time()

            # Return response data
            return {
                "status_code": response.status,
                "headers": dict(response.headers),
                "content": response.data.decode("utf-8"),
                "response_time": end_time - start_time,
                "url": url,
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
        """Make an async HTTP request using the urllib3 library."""
        raise NotImplementedError("urllib3 is sync-only")

    def close(self) -> None:
        """Close the urllib3 pool managers."""
        self.pool.clear()
        self.pool_no_verify.clear()
