import unittest
from http_benchmark.utils.resource_monitor import resource_monitor


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
        self.assertIn('rss_mb', memory_info)
        self.assertIn('vms_mb', memory_info)
        self.assertIn('percent', memory_info)
        self.assertIsInstance(memory_info['rss_mb'], float)
        self.assertIsInstance(memory_info['vms_mb'], float)
        self.assertIsInstance(memory_info['percent'], float)
        self.assertGreaterEqual(memory_info['rss_mb'], 0)
        self.assertGreaterEqual(memory_info['vms_mb'], 0)
        self.assertGreaterEqual(memory_info['percent'], 0)

    def test_get_network_io(self):
        """Test network I/O monitoring."""
        network_io = resource_monitor.get_network_io()
        self.assertIsInstance(network_io, dict)
        self.assertIn('bytes_sent', network_io)
        self.assertIn('bytes_recv', network_io)
        self.assertIn('packets_sent', network_io)
        self.assertIn('packets_recv', network_io)
        self.assertIsInstance(network_io['bytes_sent'], int)
        self.assertIsInstance(network_io['bytes_recv'], int)
        self.assertGreaterEqual(network_io['bytes_sent'], 0)
        self.assertGreaterEqual(network_io['bytes_recv'], 0)

    def test_get_disk_io(self):
        """Test disk I/O monitoring."""
        disk_io = resource_monitor.get_disk_io()
        self.assertIsInstance(disk_io, dict)
        self.assertIn('read_mb', disk_io)
        self.assertIn('write_mb', disk_io)
        self.assertIsInstance(disk_io['read_mb'], float)
        self.assertIsInstance(disk_io['write_mb'], float)
        self.assertGreaterEqual(disk_io['read_mb'], 0)
        self.assertGreaterEqual(disk_io['write_mb'], 0)

    def test_get_all_metrics(self):
        """Test getting all metrics at once."""
        all_metrics = resource_monitor.get_all_metrics()
        self.assertIsInstance(all_metrics, dict)
        self.assertIn('timestamp', all_metrics)
        self.assertIn('cpu_percent', all_metrics)
        self.assertIn('memory_info', all_metrics)
        self.assertIn('network_io', all_metrics)
        self.assertIn('disk_io', all_metrics)
        
        # Validate specific metric types
        self.assertIsInstance(all_metrics['cpu_percent'], float)
        self.assertIsInstance(all_metrics['memory_info'], dict)
        self.assertIsInstance(all_metrics['network_io'], dict)
        self.assertIsInstance(all_metrics['disk_io'], dict)


if __name__ == '__main__':
    unittest.main()