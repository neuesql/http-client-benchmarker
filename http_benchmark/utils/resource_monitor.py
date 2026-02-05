"""Resource monitoring utilities for the HTTP benchmark framework."""

import psutil
import time
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime


class ResourceMonitor:
    """Monitor system resources during benchmark execution."""

    def __init__(self):
        self.process = psutil.Process()
        self._lock = threading.Lock()
        self._monitoring = False
        self._samples: List[Dict[str, Any]] = []
        self._monitor_thread: Optional[threading.Thread] = None
        self._initial_net_io: Optional[Any] = None
        # Prime CPU percent (first call returns 0)
        self.process.cpu_percent()

    def start_monitoring(self) -> None:
        """Start background monitoring thread."""
        self._initial_net_io = psutil.net_io_counters()
        with self._lock:
            self._samples = []
        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()

    def _monitor_loop(self) -> None:
        """Sample metrics every 200ms."""
        while self._monitoring:
            sample = {
                "cpu_percent": self.process.cpu_percent(),
                "memory_percent": self.process.memory_percent(),
                "timestamp": time.time()
            }
            with self._lock:
                self._samples.append(sample)
            time.sleep(0.2)

    def stop_monitoring(self) -> Dict[str, Any]:
        """Stop monitoring and return aggregated metrics."""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=1.0)
            self._monitor_thread = None
        return self._aggregate_metrics()

    def _aggregate_metrics(self) -> Dict[str, Any]:
        """Calculate averages from collected samples."""
        with self._lock:
            if not self._samples:
                return {"cpu_avg": 0.0, "memory_avg": 0.0, "cpu_max": 0.0, "memory_max": 0.0, "sample_count": 0}
            cpu_values = [s["cpu_percent"] for s in self._samples]
            mem_values = [s["memory_percent"] for s in self._samples]
            return {
                "cpu_avg": sum(cpu_values) / len(cpu_values),
                "memory_avg": sum(mem_values) / len(mem_values),
                "cpu_max": max(cpu_values),
                "memory_max": max(mem_values),
                "sample_count": len(self._samples)
            }

    def get_network_io_delta(self) -> Dict[str, int]:
        """Get network I/O delta since monitoring started."""
        try:
            current = psutil.net_io_counters()
            if self._initial_net_io:
                return {
                    "bytes_sent": current.bytes_sent - self._initial_net_io.bytes_sent,
                    "bytes_recv": current.bytes_recv - self._initial_net_io.bytes_recv,
                    "packets_sent": current.packets_sent - self._initial_net_io.packets_sent,
                    "packets_recv": current.packets_recv - self._initial_net_io.packets_recv,
                }
            return {"bytes_sent": 0, "bytes_recv": 0, "packets_sent": 0, "packets_recv": 0}
        except Exception:
            return {"bytes_sent": 0, "bytes_recv": 0, "packets_sent": 0, "packets_recv": 0}

    def get_cpu_percent(self) -> float:
        """Get current CPU usage percentage."""
        return self.process.cpu_percent()

    def get_memory_info(self) -> Dict[str, float]:
        """Get current memory usage information."""
        memory_info = self.process.memory_info()
        memory_percent = self.process.memory_percent()

        return {
            "rss_mb": memory_info.rss / 1024 / 1024,  # Resident Set Size in MB
            "vms_mb": memory_info.vms / 1024 / 1024,  # Virtual Memory Size in MB
            "percent": memory_percent,
        }

    def get_network_io(self) -> Dict[str, int]:
        """Get network I/O statistics."""
        try:
            current_net = psutil.net_io_counters()
            return {
                "bytes_sent": current_net.bytes_sent,
                "bytes_recv": current_net.bytes_recv,
                "packets_sent": current_net.packets_sent,
                "packets_recv": current_net.packets_recv,
            }
        except Exception:
            return {"bytes_sent": 0, "bytes_recv": 0, "packets_sent": 0, "packets_recv": 0}

    def get_disk_io(self) -> Dict[str, float]:
        """Get disk I/O statistics."""
        try:
            disk_io = psutil.disk_io_counters()
            if disk_io:
                return {
                    "read_mb": (disk_io.read_bytes / 1024 / 1024 if disk_io.read_bytes else 0.0),
                    "write_mb": (disk_io.write_bytes / 1024 / 1024 if disk_io.write_bytes else 0.0),
                }
            else:
                return {"read_mb": 0.0, "write_mb": 0.0}
        except Exception:
            return {"read_mb": 0.0, "write_mb": 0.0}

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all resource metrics at once."""
        return {
            "timestamp": datetime.now(),
            "cpu_percent": self.get_cpu_percent(),
            "memory_info": self.get_memory_info(),
            "network_io": self.get_network_io(),
            "disk_io": self.get_disk_io(),
        }


# Global resource monitor instance
resource_monitor = ResourceMonitor()
