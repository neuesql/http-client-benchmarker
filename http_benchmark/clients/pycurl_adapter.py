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
        self.curl = None

    def __enter__(self):
        """Initialize curl object when entering sync context."""
        self.curl = pycurl.Curl()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close curl object when exiting sync context."""
        if self.curl:
            self.curl.close()

    def make_request(self, request: HTTPRequest) -> Dict[str, Any]:
        """Make an HTTP request using the pycurl library."""
        try:
            method = request.method.upper()
            url = request.url
            headers = request.headers
            timeout = request.timeout
            verify_ssl = request.verify_ssl

            buffer = BytesIO()

            self.curl.reset()
            self.curl.setopt(pycurl.URL, url)

            header_list = [f"{key}: {value}" for key, value in headers.items()]
            self.curl.setopt(pycurl.HTTPHEADER, header_list)

            self.curl.setopt(pycurl.TIMEOUT, timeout)

            if not verify_ssl:
                self.curl.setopt(pycurl.SSL_VERIFYPEER, 0)
                self.curl.setopt(pycurl.SSL_VERIFYHOST, 0)

            if method == "GET":
                self.curl.setopt(pycurl.HTTPGET, 1)
            elif method == "POST":
                self.curl.setopt(pycurl.POST, 1)
                if request.body:
                    self.curl.setopt(pycurl.POSTFIELDS, request.body)
            elif method == "PUT":
                self.curl.setopt(pycurl.CUSTOMREQUEST, "PUT")
                if request.body:
                    self.curl.setopt(pycurl.POSTFIELDS, request.body)
            elif method == "DELETE":
                self.curl.setopt(pycurl.CUSTOMREQUEST, "DELETE")
            elif method == "PATCH":
                self.curl.setopt(pycurl.CUSTOMREQUEST, "PATCH")
                if request.body:
                    self.curl.setopt(pycurl.POSTFIELDS, request.body)
            elif method == "HEAD":
                self.curl.setopt(pycurl.NOBODY, 1)
            elif method == "OPTIONS":
                self.curl.setopt(pycurl.CUSTOMREQUEST, "OPTIONS")

            self.curl.setopt(pycurl.WRITEDATA, buffer)

            start_time = time.time()

            self.curl.perform()

            response_time = time.time() - start_time

            status_code = self.curl.getinfo(pycurl.RESPONSE_CODE)

            response_data = buffer.getvalue().decode("utf-8")

            return {
                "status_code": status_code,
                "headers": headers,
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
        raise NotImplementedError("pycurl is sync-only, use make_request instead")
