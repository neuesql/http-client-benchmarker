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
    
    def make_request(self, request: HTTPRequest) -> Dict[str, Any]:
        """Make an HTTP request using the aiohttp library.
        
        Note: aiohttp is async-only, so this runs the async version in an event loop.
        """
        try:
            # Run the async method in a new event loop
            return asyncio.run(self.make_request_async(request))
        except Exception as e:
            return {
                'status_code': None,
                'headers': {},
                'content': '',
                'response_time': 0,
                'url': request.url,
                'success': False,
                'error': str(e)
            }
    
    async def make_request_async(self, request: HTTPRequest) -> Dict[str, Any]:
        """Make an async HTTP request using the aiohttp library."""
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
            async with aiohttp.ClientSession() as session:
                start_time = asyncio.get_event_loop().time()
                
                async with session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    data=data,
                    timeout=timeout,
                    ssl=ssl
                ) as response:
                    content = await response.text()
                
                end_time = asyncio.get_event_loop().time()
            
            # Return response data
            return {
                'status_code': response.status,
                'headers': dict(response.headers),
                'content': content,
                'response_time': end_time - start_time,
                'url': str(response.url),
                'success': True,
                'error': None
            }
        except Exception as e:
            return {
                'status_code': None,
                'headers': {},
                'content': '',
                'response_time': 0,
                'url': request.url,
                'success': False,
                'error': str(e)
            }
    
    def get_supported_methods(self) -> list:
        """Return list of supported HTTP methods."""
        return ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']