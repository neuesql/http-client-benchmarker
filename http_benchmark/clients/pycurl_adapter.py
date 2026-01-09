"""PycURL HTTP client adapter for the HTTP benchmark framework."""

import pycurl
from io import BytesIO
from typing import Dict, Any
from .base import BaseHTTPAdapter
from ..models.http_request import HTTPRequest
import time


class PycurlAdapter(BaseHTTPAdapter):
    """HTTP adapter for the pycurl library."""

    def __init__(self):
        super().__init__("pycurl")

    def make_request(self, request: HTTPRequest) -> Dict[str, Any]:
        """Make an HTTP request using the pycurl library."""
        try:
            # Prepare the request
            method = request.method.upper()
            url = request.url
            headers = request.headers
            timeout = request.timeout
            verify_ssl = request.verify_ssl

            # Create a buffer to capture response
            buffer = BytesIO()

            # Create curl object
            c = pycurl.Curl()

            # Set URL
            c.setopt(pycurl.URL, url)

            # Set headers
            header_list = [f"{key}: {value}" for key, value in headers.items()]
            c.setopt(pycurl.HTTPHEADER, header_list)

            # Set timeout
            c.setopt(pycurl.TIMEOUT, timeout)

            # Set SSL options
            if not verify_ssl:
                c.setopt(pycurl.SSL_VERIFYPEER, 0)
                c.setopt(pycurl.SSL_VERIFYHOST, 0)

            # Set method-specific options
            if method == "GET":
                c.setopt(pycurl.HTTPGET, 1)
            elif method == "POST":
                c.setopt(pycurl.POST, 1)
                if request.body:
                    c.setopt(pycurl.POSTFIELDS, request.body)
            elif method == "PUT":
                c.setopt(pycurl.CUSTOMREQUEST, "PUT")
                if request.body:
                    c.setopt(pycurl.POSTFIELDS, request.body)
            elif method == "DELETE":
                c.setopt(pycurl.CUSTOMREQUEST, "DELETE")
            elif method == "PATCH":
                c.setopt(pycurl.CUSTOMREQUEST, "PATCH")
                if request.body:
                    c.setopt(pycurl.POSTFIELDS, request.body)
            elif method == "HEAD":
                c.setopt(pycurl.NOBODY, 1)
            elif method == "OPTIONS":
                c.setopt(pycurl.CUSTOMREQUEST, "OPTIONS")

            # Set response buffer
            c.setopt(pycurl.WRITEDATA, buffer)

            # Track start time
            start_time = time.time()

            # Perform the request
            c.perform()

            # Get response time
            response_time = time.time() - start_time

            # Get status code
            status_code = c.getinfo(pycurl.RESPONSE_CODE)

            # Get response data
            response_data = buffer.getvalue().decode("utf-8")

            # Close curl object
            c.close()

            # Return response data
            return {
                "status_code": status_code,
                "headers": headers,  # We don't capture response headers in this simple implementation
                "content": response_data,
                "response_time": response_time,
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
        """Make an async HTTP request using the pycurl library."""
        raise NotImplementedError("pycurl is sync-only")

    def close(self) -> None:
        pass
