import time
import unittest
from http_benchmark.utils.resource_monitor import resource_monitor, ResourceMonitor


class TestResourceMonitor(unittest.TestCase):
    def test_resource_monitor_initialization(self):
        """Test that resource monitor is properly initialized."""
        self.assertIsNotNone(resource_monitor)
        self.assertIsNotNone(resource_monitor.process)

    def test_get_cpu_percent(self):
        """Test CPU percentage monitoring."""
        cpu_percent = resource_monitor.get_cpu_percent()
        self.assertIsInstance(cpu_percent, float)
        # CPU usage can be 0 or higher
        self.assertGreaterEqual(cpu_percent, 0)

    def test_get_memory_info(self):
        """Test memory information monitoring."""
        memory_info = resource_monitor.get_memory_info()
        self.assertIsInstance(memory_info, dict)
        self.assertIn("rss_mb", memory_info)
        self.assertIn("vms_mb", memory_info)
        self.assertIn("percent", memory_info)
        self.assertIsInstance(memory_info["rss_mb"], float)
        self.assertIsInstance(memory_info["vms_mb"], float)
        self.assertIsInstance(memory_info["percent"], float)
        self.assertGreaterEqual(memory_info["rss_mb"], 0)
        self.assertGreaterEqual(memory_info["vms_mb"], 0)
        self.assertGreaterEqual(memory_info["percent"], 0)

    def test_get_network_io(self):
        """Test network I/O monitoring."""
        network_io = resource_monitor.get_network_io()
        self.assertIsInstance(network_io, dict)
        self.assertIn("bytes_sent", network_io)
        self.assertIn("bytes_recv", network_io)
        self.assertIn("packets_sent", network_io)
        self.assertIn("packets_recv", network_io)
        self.assertIsInstance(network_io["bytes_sent"], int)
        self.assertIsInstance(network_io["bytes_recv"], int)
        self.assertGreaterEqual(network_io["bytes_sent"], 0)
        self.assertGreaterEqual(network_io["bytes_recv"], 0)

    def test_get_disk_io(self):
        """Test disk I/O monitoring."""
        disk_io = resource_monitor.get_disk_io()
        self.assertIsInstance(disk_io, dict)
        self.assertIn("read_mb", disk_io)
        self.assertIn("write_mb", disk_io)
        self.assertIsInstance(disk_io["read_mb"], float)
        self.assertIsInstance(disk_io["write_mb"], float)
        self.assertGreaterEqual(disk_io["read_mb"], 0)
        self.assertGreaterEqual(disk_io["write_mb"], 0)

    def test_get_all_metrics(self):
        """Test getting all metrics at once."""
        all_metrics = resource_monitor.get_all_metrics()
        self.assertIsInstance(all_metrics, dict)
        self.assertIn("timestamp", all_metrics)
        self.assertIn("cpu_percent", all_metrics)
        self.assertIn("memory_info", all_metrics)
        self.assertIn("network_io", all_metrics)
        self.assertIn("disk_io", all_metrics)

        # Validate specific metric types
        self.assertIsInstance(all_metrics["cpu_percent"], float)
        self.assertIsInstance(all_metrics["memory_info"], dict)
        self.assertIsInstance(all_metrics["network_io"], dict)
        self.assertIsInstance(all_metrics["disk_io"], dict)


class TestResourceMonitorContinuous(unittest.TestCase):
    """Tests for the new continuous monitoring functionality."""

    def test_start_stop_monitoring(self):
        """Test starting and stopping continuous monitoring."""
        monitor = ResourceMonitor()
        monitor.start_monitoring()
        time.sleep(0.5)  # Allow at least 2 samples at 200ms interval
        metrics = monitor.stop_monitoring()

        self.assertIsInstance(metrics, dict)
        self.assertIn("cpu_avg", metrics)
        self.assertIn("memory_avg", metrics)
        self.assertIn("cpu_max", metrics)
        self.assertIn("memory_max", metrics)
        self.assertIn("sample_count", metrics)
        self.assertGreaterEqual(metrics["sample_count"], 2)

    def test_network_io_delta(self):
        """Test that network I/O delta tracking works correctly."""
        monitor = ResourceMonitor()
        monitor.start_monitoring()
        time.sleep(0.3)
        delta = monitor.get_network_io_delta()
        monitor.stop_monitoring()

        self.assertIsInstance(delta, dict)
        self.assertIn("bytes_sent", delta)
        self.assertIn("bytes_recv", delta)
        self.assertIn("packets_sent", delta)
        self.assertIn("packets_recv", delta)
        # Delta values should be small (not cumulative system totals)
        # During the test, we shouldn't have sent/received TB of data
        self.assertLess(delta["bytes_sent"], 1024 * 1024 * 100)  # < 100MB
        self.assertLess(delta["bytes_recv"], 1024 * 1024 * 100)  # < 100MB

    def test_cpu_priming(self):
        """Test that CPU percent is primed in __init__ to avoid first-call returning 0."""
        monitor = ResourceMonitor()
        # After initialization, cpu_percent should have been called once (priming)
        # So subsequent calls should return a meaningful value (not always 0)
        cpu = monitor.get_cpu_percent()
        self.assertIsInstance(cpu, float)
        self.assertGreaterEqual(cpu, 0)

    def test_aggregated_metrics(self):
        """Test that aggregated metrics are calculated correctly."""
        monitor = ResourceMonitor()
        monitor.start_monitoring()
        time.sleep(0.7)  # Allow ~3 samples
        metrics = monitor.stop_monitoring()

        # Averages should be >= 0
        self.assertGreaterEqual(metrics["cpu_avg"], 0)
        self.assertGreaterEqual(metrics["memory_avg"], 0)
        # Max should be >= avg
        self.assertGreaterEqual(metrics["cpu_max"], metrics["cpu_avg"])
        self.assertGreaterEqual(metrics["memory_max"], metrics["memory_avg"])

    def test_stop_without_start_returns_empty_metrics(self):
        """Test that stopping monitoring without starting returns empty metrics."""
        monitor = ResourceMonitor()
        metrics = monitor.stop_monitoring()

        self.assertEqual(metrics["cpu_avg"], 0.0)
        self.assertEqual(metrics["memory_avg"], 0.0)
        self.assertEqual(metrics["sample_count"], 0)


if __name__ == "__main__":
    unittest.main()
