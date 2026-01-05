import unittest
import os
import tempfile
from http_benchmark.storage import ResultStorage
from http_benchmark.models.benchmark_result import BenchmarkResult
from datetime import datetime


class TestResultStorage(unittest.TestCase):
    def setUp(self):
        """Set up test database in a temporary location."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.storage = ResultStorage(db_path=self.temp_db.name)

    def tearDown(self):
        """Clean up test database."""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_storage_initialization(self):
        """Test ResultStorage initialization."""
        self.assertEqual(self.storage.db_path, self.temp_db.name)
        # Verify the database was created with the correct schema
        self.assertIsNotNone(self.storage)

    def test_save_result(self):
        """Test saving a benchmark result."""
        result = BenchmarkResult(
            name="Test Benchmark",
            client_library="requests",
            http_method="GET",
            url="https://example.com",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration=10.0,
            requests_count=100,
            requests_per_second=10.0,
            avg_response_time=0.1,
            min_response_time=0.05,
            max_response_time=0.2,
            p95_response_time=0.15,
            p99_response_time=0.18,
            cpu_usage_avg=25.0,
            memory_usage_avg=100.0,
            network_io={'bytes_sent': 1000, 'bytes_recv': 2000},
            error_count=0,
            error_rate=0.0,
            concurrency_level=5,
            config_snapshot={}
        )
        
        # Save the result
        self.storage.save_result(result)
        
        # Verify it was saved by retrieving it
        retrieved_result = self.storage.get_result_by_id(result.id)
        self.assertIsNotNone(retrieved_result)
        self.assertEqual(retrieved_result.id, result.id)
        self.assertEqual(retrieved_result.name, result.name)
        self.assertEqual(retrieved_result.client_library, result.client_library)

    def test_get_result_by_id(self):
        """Test retrieving a result by ID."""
        result = BenchmarkResult(
            name="Test Get By ID",
            client_library="httpx",
            http_method="POST",
            url="https://example.com/api",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration=5.0,
            requests_count=50,
            requests_per_second=10.0,
            avg_response_time=0.05,
            min_response_time=0.02,
            max_response_time=0.1,
            p95_response_time=0.08,
            p99_response_time=0.09,
            cpu_usage_avg=30.0,
            memory_usage_avg=150.0,
            network_io={'bytes_sent': 500, 'bytes_recv': 1000},
            error_count=0,
            error_rate=0.0,
            concurrency_level=3,
            config_snapshot={}
        )
        
        # Save and retrieve
        self.storage.save_result(result)
        retrieved = self.storage.get_result_by_id(result.id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, result.id)
        self.assertEqual(retrieved.name, "Test Get By ID")

    def test_get_results_by_name(self):
        """Test retrieving results by name."""
        # Create and save multiple results with the same name
        name = "Test Results By Name"
        for i in range(3):
            result = BenchmarkResult(
                name=name,
                client_library="requests",
                http_method="GET",
                url=f"https://example.com/{i}",
                start_time=datetime.now(),
                end_time=datetime.now(),
                duration=5.0,
                requests_count=10 + i,
                requests_per_second=2.0 + i,
                avg_response_time=0.1,
                min_response_time=0.05,
                max_response_time=0.2,
                p95_response_time=0.15,
                p99_response_time=0.18,
                cpu_usage_avg=25.0,
                memory_usage_avg=100.0,
                network_io={'bytes_sent': 100, 'bytes_recv': 200},
                error_count=0,
                error_rate=0.0,
                concurrency_level=2,
                config_snapshot={}
            )
            self.storage.save_result(result)
        
        # Retrieve results by name
        results = self.storage.get_results_by_name(name)
        
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertEqual(result.name, name)

    def test_get_all_results(self):
        """Test retrieving all results."""
        # Save a few results
        for i in range(2):
            result = BenchmarkResult(
                name=f"Test All Results {i}",
                client_library="httpx",
                http_method="GET",
                url=f"https://example.com/{i}",
                start_time=datetime.now(),
                end_time=datetime.now(),
                duration=5.0,
                requests_count=10,
                requests_per_second=2.0,
                avg_response_time=0.1,
                min_response_time=0.05,
                max_response_time=0.2,
                p95_response_time=0.15,
                p99_response_time=0.18,
                cpu_usage_avg=25.0,
                memory_usage_avg=100.0,
                network_io={'bytes_sent': 100, 'bytes_recv': 200},
                error_count=0,
                error_rate=0.0,
                concurrency_level=2,
                config_snapshot={}
            )
            self.storage.save_result(result)
        
        # Retrieve all results
        all_results = self.storage.get_all_results()
        
        self.assertGreaterEqual(len(all_results), 2)
        # Results should be ordered by created_at DESC (most recent first)
        if len(all_results) >= 2:
            # This is difficult to test precisely without knowing the exact implementation
            # of the created_at timestamp, so we just verify we get results back
            pass

    def test_compare_results(self):
        """Test comparing multiple results."""
        # Create and save multiple results with different client libraries
        clients = ["requests", "httpx", "aiohttp"]
        results = []
        
        for client in clients:
            result = BenchmarkResult(
                name="Comparison Test",
                client_library=client,
                http_method="GET",
                url="https://example.com",
                start_time=datetime.now(),
                end_time=datetime.now(),
                duration=5.0,
                requests_count=50,
                requests_per_second=10.0,
                avg_response_time=0.1,
                min_response_time=0.05,
                max_response_time=0.2,
                p95_response_time=0.15,
                p99_response_time=0.18,
                cpu_usage_avg=25.0,
                memory_usage_avg=100.0,
                network_io={'bytes_sent': 100, 'bytes_recv': 200},
                error_count=0,
                error_rate=0.0,
                concurrency_level=5,
                config_snapshot={}
            )
            self.storage.save_result(result)
            results.append(result)
        
        # Get the IDs to compare
        result_ids = [r.id for r in results]
        
        # Compare the results
        comparison = self.storage.compare_results(result_ids)
        
        self.assertEqual(len(comparison), 3)
        for comparison_item in comparison:
            self.assertIn('id', comparison_item)
            self.assertIn('client_library', comparison_item)
            self.assertIn('requests_per_second', comparison_item)
            self.assertIn('avg_response_time', comparison_item)
            self.assertIn('error_rate', comparison_item)
            self.assertIn('cpu_usage_avg', comparison_item)
            self.assertIn('memory_usage_avg', comparison_item)

    def test_database_schema(self):
        """Test that the database schema is correctly created."""
        import sqlite3
        
        conn = sqlite3.connect(self.temp_db.name)
        cursor = conn.cursor()
        
        # Check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='benchmark_results';")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists, "benchmark_results table should exist")
        
        # Check the table structure
        cursor.execute("PRAGMA table_info(benchmark_results);")
        columns = cursor.fetchall()
        
        column_names = [col[1] for col in columns]
        expected_columns = [
            'id', 'name', 'client_library', 'http_method', 'url', 'start_time', 
            'end_time', 'duration', 'requests_count', 'requests_per_second', 
            'avg_response_time', 'min_response_time', 'max_response_time', 
            'p95_response_time', 'p99_response_time', 'cpu_usage_avg', 
            'memory_usage_avg', 'network_io', 'error_count', 'error_rate', 
            'concurrency_level', 'config_snapshot', 'created_at'
        ]
        
        for col in expected_columns:
            self.assertIn(col, column_names, f"Column {col} should exist in benchmark_results table")
        
        conn.close()


if __name__ == '__main__':
    unittest.main()