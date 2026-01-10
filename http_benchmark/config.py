"""Configuration management for the HTTP benchmark framework."""

from pydantic_settings import BaseSettings
from typing import List, Optional


class BenchmarkSettings(BaseSettings):
    """Settings for the benchmark framework."""

    # General settings
    app_name: str = "HTTP Client Benchmark Framework"
    app_version: str = "0.1.0"

    # Benchmark settings
    default_concurrency: int = 10
    default_duration_seconds: int = 30
    default_timeout: int = 30
    default_retry_attempts: int = 3
    max_concurrency: int = 10000
    max_duration_seconds: int = 3600  # 1 hour

    # Resource monitoring settings
    resource_monitoring_interval: float = 0.1  # seconds
    cpu_monitoring_enabled: bool = True
    memory_monitoring_enabled: bool = True
    network_monitoring_enabled: bool = True

    # Storage settings
    sqlite_db_path: str = "benchmark_results.db"
    results_retention_days: int = 90

    # Supported HTTP client libraries
    supported_client_libraries: List[str] = [
        "requests",
        "requestx",
        "httpx",
        "aiohttp",
        "urllib3",
        "pycurl",
    ]

    # Supported HTTP methods
    supported_http_methods: List[str] = [
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "PATCH",
        "HEAD",
        "OPTIONS",
        "STREAM",
    ]

    class Config:
        env_prefix = "HTTP_BENCHMARK_"
        case_sensitive = False


# Create a global settings instance
settings = BenchmarkSettings()
