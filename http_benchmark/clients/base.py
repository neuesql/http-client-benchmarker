"""Base HTTP client adapter for the HTTP benchmark framework."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..models.http_request import HTTPRequest


class BaseHTTPAdapter(ABC):
    """Base class for all HTTP client adapters."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def make_request(self, request: HTTPRequest) -> Dict[str, Any]:
        """Make an HTTP request and return response data."""
        pass

    @abstractmethod
    async def make_request_async(self, request: HTTPRequest) -> Dict[str, Any]:
        """Make an async HTTP request and return response data."""
        pass

    def close(self) -> None:
        """Close any open resources (connections, sessions, etc.)."""
        pass

    async def close_async(self) -> None:
        """Close any open resources asynchronously."""
        pass
