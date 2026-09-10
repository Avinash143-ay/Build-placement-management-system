import json
import platform
import random
import sys
import time
from pathlib import Path

from bplustree import BPlusTree
from bruteforce import BruteForceIndex


def timed(action, repetitions=1):
    start = time.perf_counter()
    for _ in range(repetitions):
        action()
    return (time.perf_counter() - start) / repetitions


def benchmark(size=10000, seed=42):
    random_generator = random.Random(seed)
    keys = random_generator.sample(range(size * 10), size)
    lookup_keys = random_generator.sample(keys, min(1000, size))
    ranges = [(key, key + 250) for key in lookup_keys[:100]]

    bplus = BPlusTree(order=32)
    brute = BruteForceIndex()
    bplus_insert = timed(lambda: [bplus.insert(key, key) for key in keys])
    brute_insert = timed(lambda: [brute.insert(key, key) for key in keys])
    bplus_search = timed(lambda: [bplus.search(key) for key in lookup_keys])
    brute_search = timed(lambda: [brute.search(key) for key in lookup_keys])
    bplus_range = timed(lambda: [bplus.range_query(start, end) for start, end in ranges])
    brute_range = timed(lambda: [brute.range_query(start, end) for start, end in ranges])

    for key in lookup_keys[:100]:
        assert bplus.search(key) == (True, key)
        assert brute.search(key) == (True, key)

    metrics = {
        "size": size,
        "seed": seed,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "operations": {
            "insert": {"bplus_seconds": bplus_insert, "linear_seconds": brute_insert},
            "exact_search": {"bplus_seconds": bplus_search, "linear_seconds": brute_search},
            "range_query": {"bplus_seconds": bplus_range, "linear_seconds": brute_range},
        },
    }
    for values in metrics["operations"].values():
        values["speedup"] = values["linear_seconds"] / values["bplus_seconds"] if values["bplus_seconds"] else None
    return metrics


if __name__ == "__main__":
    output_path = Path(__file__).with_name("benchmark_results.json")
    results = benchmark()
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    print(f"Saved benchmark results to {output_path}")