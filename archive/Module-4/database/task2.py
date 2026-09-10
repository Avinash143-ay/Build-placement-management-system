import time
import tracemalloc

class PerformanceAnalyzer:
    def __init__(self, db1, db2):
        """
        Initialize with two database-like objects.
        db1, db2: should both have insert(), search(), and delete() methods
        """
        self.db1 = db1
        self.db2 = db2

    def measure_time(self, operation, *args, **kwargs):
        """
        Measure time taken for a single operation.
        operation: callable function (e.g., db.insert)
        *args, **kwargs: arguments to pass to the operation
        """
        start_time = time.perf_counter()
        operation(*args, **kwargs)
        end_time = time.perf_counter()
        return end_time - start_time

    def measure_memory(self, operation, *args, **kwargs):
        """
        Measure memory usage during an operation.
        Returns memory in kilobytes (KB).
        """
        tracemalloc.start()
        operation(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return peak / 1024  # Convert bytes to KB

    def compare_operations(self, keys, operation_type="insert"):
        """
        Compare time and memory for db1 and db2 on a batch of keys.
        operation_type: "insert", "search", or "delete"
        keys: list of keys to perform operations on
        """

        results = {}

        for db_name, db in [("BPlusTree", self.db1), ("BruteForceDB", self.db2)]:
            total_time = 0
            total_memory = 0

            for key in keys:
                if operation_type == "insert":
                    op = lambda: db.insert(key, f"Value_{key}")
                elif operation_type == "search":
                    op = lambda: db.search(key)
                elif operation_type == "delete":
                    op = lambda: db.delete(key)
                elif operation_type == "range_query":
                # Pick a small random range near the key
                    start_key = key
                    end_key = key + 5  # or randomize if you want
                    op = lambda: db.range_query(start_key, end_key)

                else:
                    raise ValueError("Invalid operation_type")

                total_time += self.measure_time(op)
                total_memory += self.measure_memory(op)

            avg_time = total_time / len(keys)
            avg_memory = total_memory / len(keys)

            results[db_name] = {
                "average_time_sec": avg_time,
                "average_memory_kb": avg_memory
            }

        return results
from bplustree import BPlusTree
from bruteforce import BruteForceIndex


# Create databases


bplus_tree = BPlusTree(order=4)
brute_force_db = BruteForceIndex()

# Create analyzer
analyzer = PerformanceAnalyzer(bplus_tree, brute_force_db)

# Prepare keys
keys = list(range(100))

# Compare insertion
insert_results = analyzer.compare_operations(keys, operation_type="insert")
print("Insertion Results:", insert_results)

# Compare searching
search_results = analyzer.compare_operations(keys, operation_type="search")
print("Search Results:", search_results)

# Compare deletion
delete_results = analyzer.compare_operations(keys, operation_type="delete")
print("Deletion Results:", delete_results)
# Compare range queries
range_query_results = analyzer.compare_operations(keys, operation_type="range_query")
print("Range Query Results:", range_query_results)

