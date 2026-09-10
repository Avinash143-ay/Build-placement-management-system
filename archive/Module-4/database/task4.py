import random
import time
import matplotlib.pyplot as plt
from bplustree import BPlusTree
from bruteforce import BruteForceIndex

# Setup for experiment
sizes = list(range(1000, 10001, 1000))  # Sizes from 1000 to 10000
insert_times_bplus = []
insert_times_brute = []
search_times_bplus = []
search_times_brute = []
range_times_bplus = []
range_times_brute = []
delete_times_bplus = []
delete_times_brute = []

for size in sizes:
    print(f"Testing size: {size}")
    keys = random.sample(range(size * 10), size)  # random unique keys
    search_keys = random.sample(keys, min(100, size))  # pick 100 random keys to search
    delete_keys = random.sample(keys, min(100, size))  # pick 100 random keys to delete
    range_queries = [(random.randint(0, size * 5), random.randint(size * 5, size * 10)) for _ in range(10)]

    # Initialize Data Structures
    bplus = BPlusTree(order=6)
    brute = BruteForceIndex()

    # Insertion Timing
    start = time.time()
    for key in keys:
        bplus.insert(key, str(key))
    insert_times_bplus.append(time.time() - start)

    start = time.time()
    for key in keys:
        brute.insert(key, str(key))
    insert_times_brute.append(time.time() - start)

    # Search Timing
    start = time.time()
    for key in search_keys:
        bplus.search(key)
    search_times_bplus.append(time.time() - start)

    start = time.time()
    for key in search_keys:
        brute.search(key)
    search_times_brute.append(time.time() - start)

    # Range Query Timing
    start = time.time()
    for start_key, end_key in range_queries:
        bplus.range_query(start_key, end_key)
    range_times_bplus.append(time.time() - start)

    start = time.time()
    for start_key, end_key in range_queries:
        brute_range = [item for item in brute.get_all() if start_key <= item[0] <= end_key]
    range_times_brute.append(time.time() - start)

    # Deletion Timing
    start = time.time()
    for key in delete_keys:
        if bplus.search(key) is not None:
          bplus.delete(key)
    delete_times_bplus.append(time.time() - start)

    start = time.time()
    for key in delete_keys:
        if brute.search(key) is not None:
          brute.delete(key)
    delete_times_brute.append(time.time() - start)

# Plotting Results
plt.figure(figsize=(16, 12))

# Insertion Times
plt.subplot(2, 2, 1)
plt.plot(sizes, insert_times_bplus, label="B+ Tree Insert", marker='o')
plt.plot(sizes, insert_times_brute, label="Brute Force Insert", marker='x')
plt.xlabel("Number of Elements")
plt.ylabel("Time (seconds)")
plt.title("Insertion Time Comparison")
plt.legend()

# Search Times
plt.subplot(2, 2, 2)
plt.plot(sizes, search_times_bplus, label="B+ Tree Search", marker='o')
plt.plot(sizes, search_times_brute, label="Brute Force Search", marker='x')
plt.xlabel("Number of Elements")
plt.ylabel("Time (seconds)")
plt.title("Search Time Comparison")
plt.legend()

# Range Query Times
plt.subplot(2, 2, 3)
plt.plot(sizes, range_times_bplus, label="B+ Tree Range Query", marker='o')
plt.plot(sizes, range_times_brute, label="Brute Force Range Query", marker='x')
plt.xlabel("Number of Elements")
plt.ylabel("Time (seconds)")
plt.title("Range Query Time Comparison")
plt.legend()

# Deletion Times
plt.subplot(2, 2, 4)
plt.plot(sizes, delete_times_bplus, label="B+ Tree Delete", marker='o')
plt.plot(sizes, delete_times_brute, label="Brute Force Delete", marker='x')
plt.xlabel("Number of Elements")
plt.ylabel("Time (seconds)")
plt.title("Deletion Time Comparison")
plt.legend()

plt.tight_layout()
plt.show()
