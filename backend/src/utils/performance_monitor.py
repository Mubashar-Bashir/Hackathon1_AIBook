"""
Performance monitoring utilities for authentication endpoints
This addresses task T054: Add performance monitoring for authentication endpoints
"""
import time
import functools
import logging
from typing import Callable, Any
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Utility class for monitoring performance of authentication endpoints."""

    def __init__(self):
        self.metrics = {}

    def log_performance(self, endpoint_name: str, execution_time: float, status_code: int = 200):
        """Log performance metrics for an endpoint."""
        timestamp = datetime.utcnow().isoformat()

        metric = {
            'endpoint': endpoint_name,
            'timestamp': timestamp,
            'execution_time_ms': round(execution_time * 1000, 2),  # Convert to milliseconds
            'status_code': status_code
        }

        logger.info(f"PERFORMANCE | {endpoint_name} | {metric['execution_time_ms']}ms | Status: {status_code}")

        # Store metrics for potential aggregation
        if endpoint_name not in self.metrics:
            self.metrics[endpoint_name] = []
        self.metrics[endpoint_name].append(metric)

    def get_endpoint_stats(self, endpoint_name: str):
        """Get performance statistics for a specific endpoint."""
        if endpoint_name not in self.metrics:
            return None

        endpoint_metrics = self.metrics[endpoint_name]
        execution_times = [m['execution_time_ms'] for m in endpoint_metrics]

        if not execution_times:
            return None

        return {
            'endpoint': endpoint_name,
            'total_calls': len(execution_times),
            'avg_execution_time_ms': round(sum(execution_times) / len(execution_times), 2),
            'min_execution_time_ms': min(execution_times),
            'max_execution_time_ms': max(execution_times),
            'p95_execution_time_ms': self._calculate_percentile(execution_times, 95),
            'p99_execution_time_ms': self._calculate_percentile(execution_times, 99)
        }

    def _calculate_percentile(self, data: list, percentile: float):
        """Calculate percentile for a list of values."""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)] if sorted_data else 0

# Global performance monitor instance
perf_monitor = PerformanceMonitor()


def monitor_performance(endpoint_name: str):
    """Decorator to monitor performance of authentication endpoints."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            status_code = 200  # Default to success

            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                # In case of exception, we might want to capture the status code
                # For now, we'll log it as an error
                status_code = 500
                raise
            finally:
                execution_time = time.time() - start_time
                perf_monitor.log_performance(endpoint_name, execution_time, status_code)

        return wrapper
    return decorator


def monitor_sync_performance(endpoint_name: str):
    """Decorator to monitor performance of synchronous functions."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            status_code = 200  # Default to success

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                status_code = 500
                raise
            finally:
                execution_time = time.time() - start_time
                perf_monitor.log_performance(endpoint_name, execution_time, status_code)

        return wrapper
    return decorator


# Example usage:
if __name__ == "__main__":
    # Example of how to use the performance monitor
    import asyncio

    @monitor_performance("test_endpoint")
    async def example_endpoint():
        # Simulate some work
        await asyncio.sleep(0.1)
        return {"message": "success"}

    async def test():
        await example_endpoint()
        print(perf_monitor.get_endpoint_stats("test_endpoint"))

    # asyncio.run(test())