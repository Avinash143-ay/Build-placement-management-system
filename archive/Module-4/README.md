# Module 4: Custom Database Engine

## Status

The repository contains a from-scratch B+ tree implementation, table/database
helpers, notebooks, automated tests, and a reproducible benchmark.

## Components

- [`database/bplustree.py`](database/bplustree.py): insert, exact search, range
	query, update, delete, traversal, and Graphviz visualization.
- [`database/task2.py`](database/task2.py): small manual demonstration of the
	tree operations.
- [`database/task4.py`](database/task4.py): timing experiment for B+ tree versus
	a brute-force index.
- [`database/table.py`](database/table.py) and [`database/db_manager.py`](database/db_manager.py):
	custom table/database persistence helpers.

## Evidence

- [`database/test_bplustree.py`](database/test_bplustree.py) covers insertion,
	exact lookup, range queries, updates, and deletion.
- [`database/benchmark.py`](database/benchmark.py) benchmarks 10,000 deterministic
	records and saves environment metadata and raw timings to
	[`database/benchmark_results.json`](database/benchmark_results.json).
- The current run shows approximately 57x exact-lookup and 40x range-query
	speedups over a linear scan; insertion remains slower because the index pays a
	write-time maintenance cost.

## Local Demo

From `Module-4/database`:

```powershell
python run.py
```

The visualization path additionally requires Graphviz installed on the system.
