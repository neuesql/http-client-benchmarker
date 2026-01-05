"""Core benchmarking functionality for the HTTP benchmark framework."""

import time
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, Any, List, Optional
from .models.benchmark_result import BenchmarkResult
from .models.benchmark_configuration import BenchmarkConfiguration
from .models.http_request import HTTPRequest
from .clients.requests_adapter import RequestsAdapter
from .clients.requestx_adapter import RequestXAdapter
from .clients.httpx_adapter import HttpxAdapter
from .clients.aiohttp_adapter import AiohttpAdapter
from .clients.urllib3_adapter import Urllib3Adapter
from .clients.pycurl_adapter import PycurlAdapter
from .utils.resource_monitor import resource_monitor
from .utils.logging import app_logger


class BenchmarkRunner:
    """Core benchmarking functionality for HTTP client performance testing."""
    
    def __init__(self, config: BenchmarkConfiguration):
        self.config = config
        self.adapters = {
            'requests': RequestsAdapter(),
            'requestx': RequestXAdapter(),
            'httpx': HttpxAdapter(),
            'aiohttp': AiohttpAdapter(),
            'urllib3': Urllib3Adapter(),
            'pycurl': PycurlAdapter()
        }
        self.results = []
        self.resource_metrics = []
    
    def run(self) -> BenchmarkResult:
        """Run the benchmark with the given configuration."""
        app_logger.info(f"Starting benchmark for {self.config.target_url} using {self.config.client_library}")
        
        start_time = datetime.now()
        
        # Validate configuration
        if self.config.client_library not in self.adapters:
            raise ValueError(f"Unsupported client library: {self.config.client_library}")
        
        # Get the appropriate adapter
        adapter = self.adapters[self.config.client_library]
        
        # Prepare the HTTP request
        http_request = HTTPRequest(
            method=self.config.http_method,
            url=self.config.target_url,
            headers=self.config.headers,
            body=self.config.body,
            timeout=self.config.timeout,
            verify_ssl=self.config.verify_ssl
        )
        
        # Collect initial resource metrics
        initial_metrics = resource_monitor.get_all_metrics()
        
        # Run the benchmark based on sync/async configuration
        if self.config.is_async:
            result = asyncio.run(self._run_async_benchmark(adapter, http_request))
        else:
            result = self._run_sync_benchmark(adapter, http_request)
        
        # Collect final resource metrics
        final_metrics = resource_monitor.get_all_metrics()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Calculate average resource usage
        cpu_usage_avg = (initial_metrics['cpu_percent'] + final_metrics['cpu_percent']) / 2
        memory_usage_avg = (initial_metrics['memory_info']['percent'] + final_metrics['memory_info']['percent']) / 2
        
        # Create and return the benchmark result
        benchmark_result = BenchmarkResult(
            name=self.config.name,
            client_library=self.config.client_library,
            http_method=self.config.http_method,
            url=self.config.target_url,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            requests_count=result['requests_count'],
            requests_per_second=result['requests_per_second'],
            avg_response_time=result['avg_response_time'],
            min_response_time=result['min_response_time'],
            max_response_time=result['max_response_time'],
            p95_response_time=result['p95_response_time'],
            p99_response_time=result['p99_response_time'],
            cpu_usage_avg=cpu_usage_avg,
            memory_usage_avg=memory_usage_avg,
            network_io=final_metrics['network_io'],
            error_count=result['error_count'],
            error_rate=result['error_rate'],
            concurrency_level=self.config.concurrency,
            config_snapshot=self.config.to_dict()
        )
        
        app_logger.info(f"Benchmark completed: {benchmark_result.requests_per_second} RPS")
        return benchmark_result
    
    def _run_sync_benchmark(self, adapter, http_request: HTTPRequest) -> Dict[str, Any]:
        """Run a synchronous benchmark."""
        app_logger.info("Running synchronous benchmark")
        
        response_times = []
        error_count = 0
        total_requests = self.config.total_requests or 1
        
        # If duration is specified instead of total_requests, calculate based on estimated RPS
        if self.config.total_requests is None:
            # For now, just run for the specified duration with a reasonable number of requests
            total_requests = self.config.concurrency * 10  # 10 requests per concurrent thread
        
        # Create HTTP requests for the benchmark
        requests = [http_request for _ in range(total_requests)]
        
        # Execute requests concurrently using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=self.config.concurrency) as executor:
            futures = [executor.submit(adapter.make_request, req) for req in requests]
            
            for future in as_completed(futures):
                result = future.result()
                if result['success']:
                    response_times.append(result['response_time'])
                else:
                    error_count += 1
        
        # Calculate metrics
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            
            # Calculate percentiles
            sorted_times = sorted(response_times)
            p95_idx = int(0.95 * len(sorted_times))
            p99_idx = int(0.99 * len(sorted_times))
            
            p95_response_time = sorted_times[min(p95_idx, len(sorted_times) - 1)] if sorted_times else 0
            p99_response_time = sorted_times[min(p99_idx, len(sorted_times) - 1)] if sorted_times else 0
        else:
            avg_response_time = 0
            min_response_time = 0
            max_response_time = 0
            p95_response_time = 0
            p99_response_time = 0
        
        total_completed_requests = len(response_times) + error_count
        duration = time.time() - time.time()  # Placeholder - in real implementation, track actual duration
        requests_per_second = total_completed_requests / self.config.duration_seconds if self.config.duration_seconds > 0 else 0
        error_rate = (error_count / total_completed_requests) * 100 if total_completed_requests > 0 else 0
        
        return {
            'requests_count': total_completed_requests,
            'requests_per_second': requests_per_second,
            'avg_response_time': avg_response_time,
            'min_response_time': min_response_time,
            'max_response_time': max_response_time,
            'p95_response_time': p95_response_time,
            'p99_response_time': p99_response_time,
            'error_count': error_count,
            'error_rate': error_rate
        }
    
    async def _run_async_benchmark(self, adapter, http_request: HTTPRequest) -> Dict[str, Any]:
        """Run an asynchronous benchmark."""
        app_logger.info("Running asynchronous benchmark")
        
        response_times = []
        error_count = 0
        total_requests = self.config.total_requests or 1
        
        # If duration is specified instead of total_requests, calculate based on estimated RPS
        if self.config.total_requests is None:
            # For now, just run for the specified duration with a reasonable number of requests
            total_requests = self.config.concurrency * 10  # 10 requests per concurrent task
        
        # Create tasks for concurrent execution
        tasks = []
        for _ in range(total_requests):
            task = adapter.make_request_async(http_request)
            tasks.append(task)
        
        # Execute tasks concurrently
        for coro in asyncio.as_completed(tasks):
            result = await coro
            if result['success']:
                response_times.append(result['response_time'])
            else:
                error_count += 1
        
        # Calculate metrics
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            
            # Calculate percentiles
            sorted_times = sorted(response_times)
            p95_idx = int(0.95 * len(sorted_times))
            p99_idx = int(0.99 * len(sorted_times))
            
            p95_response_time = sorted_times[min(p95_idx, len(sorted_times) - 1)] if sorted_times else 0
            p99_response_time = sorted_times[min(p99_idx, len(sorted_times) - 1)] if sorted_times else 0
        else:
            avg_response_time = 0
            min_response_time = 0
            max_response_time = 0
            p95_response_time = 0
            p99_response_time = 0
        
        total_completed_requests = len(response_times) + error_count
        duration = time.time() - time.time()  # Placeholder - in real implementation, track actual duration
        requests_per_second = total_completed_requests / self.config.duration_seconds if self.config.duration_seconds > 0 else 0
        error_rate = (error_count / total_completed_requests) * 100 if total_completed_requests > 0 else 0
        
        return {
            'requests_count': total_completed_requests,
            'requests_per_second': requests_per_second,
            'avg_response_time': avg_response_time,
            'min_response_time': min_response_time,
            'max_response_time': max_response_time,
            'p95_response_time': p95_response_time,
            'p99_response_time': p99_response_time,
            'error_count': error_count,
            'error_rate': error_rate
        }


class AsyncBenchmarkRunner(BenchmarkRunner):
    """Asynchronous benchmark runner that extends the base functionality."""
    
    async def run(self) -> BenchmarkResult:
        """Run the benchmark asynchronously."""
        return await self._run_async_benchmark(
            self.adapters[self.config.client_library],
            HTTPRequest(
                method=self.config.http_method,
                url=self.config.target_url,
                headers=self.config.headers,
                body=self.config.body,
                timeout=self.config.timeout,
                verify_ssl=self.config.verify_ssl
            )
        )