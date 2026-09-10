import random

from database.bplustree import BPlusTree


def test_insert_search_and_range_query():
    tree = BPlusTree(order=6)
    for key in random.Random(7).sample(range(500), 120):
        tree.insert(key, str(key))
    items = tree.get_all()
    assert [key for key, _ in items] == sorted(key for key, _ in items)
    assert tree.search(items[40][0]) == (True, str(items[40][0]))
    assert all(100 <= key <= 200 for key, _ in tree.range_query(100, 200))


def test_update_and_delete_preserve_order():
    tree = BPlusTree(order=4)
    for key in range(80):
        tree.insert(key, key)
    assert tree.update(25, "updated")
    assert tree.search(25) == (True, "updated")
    for key in range(0, 80, 3):
        assert tree.delete(key)
    assert [key for key, _ in tree.get_all()] == [key for key in range(80) if key % 3]