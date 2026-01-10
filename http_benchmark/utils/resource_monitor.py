"""Resource monitoring utilities for the HTTP benchmark framework."""

import psutil
import time
from typing import Dict, Any
from datetime import datetime


class ResourceMonitor:
    """Monitor system resources during benchmark execution."""

    def __init__(self):
        self.process = psutil.Process()

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
        # Get initial network stats
        psutil.net_io_counters()

        # Wait a bit to get a more accurate reading
        time.sleep(0.1)

        current_net = psutil.net_io_counters()

        return {
            "bytes_sent": current_net.bytes_sent,
            "bytes_recv": current_net.bytes_recv,
            "packets_sent": current_net.packets_sent,
            "packets_recv": current_net.packets_recv,
        }

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

    def start_monitoring(self) -> None:
        """Start resource monitoring."""
        # For now, just a placeholder - actual monitoring would be done in a separate thread
        pass

    def stop_monitoring(self) -> None:
        """Stop resource monitoring."""
        # For now, just a placeholder
        pass


# Global resource monitor instance
resource_monitor = ResourceMonitor()
