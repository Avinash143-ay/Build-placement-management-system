from bplustree import BPlusTree

def test_bplus_tree():
    print("=== B+ Tree Testing Started ===")
    
    # Create tree with order 4
    tree = BPlusTree(order=4)

    # 1. Insert key-value pairs
    items = [(10, "a"), (20, "b"), (5, "c"), (6, "d"), (12, "e"),
             (30, "f"), (7, "g"), (17, "h")]
    print("\nInserting items:")
    for key, value in items:
        print(f"Inserting key {key} with value '{value}'")
        tree.insert(key, value)

    print("\nAll items after insertion:")
    print(tree.get_all())

    # 2. Search for existing and non-existing keys
    print("\nExact Search tests:")
    keys_to_search = [6, 17, 25]
    for key in keys_to_search:
        found, value = tree.search(key)
        if found:
            print(f"Key {key} found with value '{value}'")
        else:
            print(f"Key {key} not found.")

    # 3. Range Query
    print("\nRange Query (keys between 6 and 20):")
    result = tree.range_query(6, 20)
    print(result)

    # 4. Update a value
    print("\nUpdating key 12 to new value 'updated-e'")
    tree.update(12, "updated-e")
    print(tree.get_all())

    # 5. Delete keys and show tree after each
    keys_to_delete = [6, 7, 5, 10]
    print("\nDeleting keys one by one:")
    for key in keys_to_delete:
        print(f"Deleting key {key}")
        tree.delete(key)
        print("Current keys:", tree.get_all())

    # 6. Final tree visualization
    tree.visualize_tree("bplus_tree_test")

    print("\n=== B+ Tree Testing Completed ===")

# Run the test
test_bplus_tree()

