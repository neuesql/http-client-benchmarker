"""AIOHTTP HTTP client adapter for the HTTP benchmark framework."""

import aiohttp
import asyncio
from typing import Dict, Any
from .base import BaseHTTPAdapter
from ..models.http_request import HTTPRequest


class AiohttpAdapter(BaseHTTPAdapter):
    """HTTP adapter for the aiohttp library."""

    def __init__(self):
        super().__init__("aiohttp")
        self.session = None

    def make_request(self, request: HTTPRequest) -> Dict[str, Any]:
        """Make an HTTP request using the aiohttp library."""
        raise NotImplementedError("aiohttp is async-only")

    async def make_request_async(self, request: HTTPRequest) -> Dict[str, Any]:
        """Make an async HTTP request using the aiohttp library."""
        # Ensure session exists and belongs to the current loop
        loop = asyncio.get_running_loop()
        if (
            self.session is None
            or self.session.closed
            or getattr(self.session, "_loop", None) is not loop
        ):
            if self.session and not self.session.closed:
                await self.session.close()
            # Use TCPConnector with proper limit
            connector = aiohttp.TCPConnector(limit=0, ttl_dns_cache=300)
            self.session = aiohttp.ClientSession(connector=connector)

        try:
            # Prepare the request
            method = request.method.upper()
            url = request.url
            headers = request.headers
            timeout = aiohttp.ClientTimeout(total=request.timeout)
            ssl = True if request.verify_ssl else False

            # Prepare data based on method
            data = request.body if request.body else None

            # Make the async request
            start_time = asyncio.get_event_loop().time()

            async with self.session.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                timeout=timeout,
                ssl=ssl,
            ) as response:
                content = await response.text()

            end_time = asyncio.get_event_loop().time()

            # Return response data
            return {
                "status_code": response.status,
                "headers": dict(response.headers),
                "content": content,
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
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            try:
                loop = getattr(self.session, "_loop", None)
                if loop and not loop.is_closed() and not loop.is_running():
                    loop.run_until_complete(self.session.close())
            except Exception as ex:
                print(ex)

    async def close_async(self) -> None:
        """Close the aiohttp session asynchronously."""
        if self.session and not self.session.closed:
            await self.session.close()
            await asyncio.sleep(0.250)
