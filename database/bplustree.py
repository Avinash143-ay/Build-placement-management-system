import bisect
from graphviz import Digraph

class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []  # for internal nodes
        self.values = []    # for leaf nodes
        self.next = None    # link to next leaf

class BPlusTree:
    def __init__(self, order=4):
        self.root = BPlusTreeNode(is_leaf=True)
        self.order = order
        self.min_keys = (order + 1) // 2

    def search(self, key):
        node = self.root
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
        for i, item in enumerate(node.keys):
            if item == key:
                return (True,node.values[i])
        return (False,None)

    def insert(self, key, value):
        root = self.root
        if len(root.keys) == self.order - 1:
            new_root = BPlusTreeNode()
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node, key, value):
        if node.is_leaf:
            idx = 0
            while idx < len(node.keys) and key >= node.keys[idx]:
                idx += 1
            node.keys.insert(idx, key)
            node.values.insert(idx, value)
        else:
            idx = 0
            while idx < len(node.keys) and key >= node.keys[idx]:
                idx += 1
            if len(node.children[idx].keys) == self.order - 1:
                self._split_child(node, idx)
                if key >= node.keys[idx]:
                    idx += 1
            self._insert_non_full(node.children[idx], key, value)

    def _split_child(self, parent, index):
        t = self.order
        node = parent.children[index]
        new_node = BPlusTreeNode(is_leaf=node.is_leaf)

        mid = (len(node.keys) + 1) // 2
        separator = node.keys[mid]
        parent.keys.insert(index, separator)
        parent.children.insert(index + 1, new_node)

        if node.is_leaf:
            new_node.keys = node.keys[mid:]
            node.keys = node.keys[:mid]
            new_node.values = node.values[mid:]
            node.values = node.values[:mid]
            new_node.next = node.next
            node.next = new_node
        else:
            new_node.keys = node.keys[mid + 1:]
            node.keys = node.keys[:mid]
            new_node.children = node.children[mid + 1:]
            node.children = node.children[:mid + 1]

    def range_query(self, start_key, end_key):
        node = self.root
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and start_key >= node.keys[i]:
                i += 1
            node = node.children[i]

        result = []
        while node:
            for i, key in enumerate(node.keys):
                if start_key <= key <= end_key:
                    result.append((key, node.values[i]))
                elif key > end_key:
                    return result
            node = node.next
        return result

    def delete(self, key):
        items = self.get_all()
        for index, (stored_key, _) in enumerate(items):
            if stored_key == key:
                items.pop(index)
                self.root = BPlusTreeNode(is_leaf=True)
                for remaining_key, value in items:
                    self.insert(remaining_key, value)
                return True
        return False

    def _delete(self, node, key):
        idx = bisect.bisect_left(node.keys, key)
        
        if node.is_leaf:
            if idx < len(node.keys) and node.keys[idx] == key:
                node.keys.pop(idx)
                node.values.pop(idx)
                return True
            return False
        else:
            if idx < len(node.keys) and node.keys[idx] == key:
                # Key found in internal node
                return self._delete_internal_node(node, key, idx)
            else:
                # Recurse into child
                if len(node.children[idx].keys) <= self.min_keys:
                    self._fix_underflow(node, idx)
                    # After fixing, idx might have changed
                    idx = bisect.bisect_left(node.keys, key)
                    if idx >= len(node.children):
                        idx = len(node.children) - 1
                
                return self._delete(node.children[idx], key)

    def _delete_internal_node(self, node, key, idx):
        # Find predecessor (max key in left subtree)
        predecessor = self._get_predecessor(node.children[idx])
        node.keys[idx] = predecessor  # Replace with predecessor
        # Now delete the predecessor from the leaf
        return self._delete(node.children[idx], predecessor)

    def _get_predecessor(self, node):
        """Find maximum key in the subtree rooted at this node"""
        while not node.is_leaf:
            node = node.children[-1]
        return node.keys[-1]

    def _fix_underflow(self, node, idx):
        """Fix underflow in node.children[idx]"""
        child = node.children[idx]
        
        # Try borrowing from left sibling
        if idx > 0 and len(node.children[idx - 1].keys) > self.min_keys:
            self._borrow_from_left(node, idx)
        # Try borrowing from right sibling
        elif idx < len(node.children) - 1 and len(node.children[idx + 1].keys) > self.min_keys:
            self._borrow_from_right(node, idx)
        # Must merge
        else:
            if idx > 0:
                self._merge(node, idx - 1)
            else:
                self._merge(node, idx)

    def _borrow_from_left(self, node, idx):
        child = node.children[idx]
        sibling = node.children[idx - 1]

        child.keys.insert(0, node.keys[idx - 1])
        node.keys[idx - 1] = sibling.keys.pop()

        if not child.is_leaf:
            child.children.insert(0, sibling.children.pop())

    def _borrow_from_right(self, node, idx):
        child = node.children[idx]
        sibling = node.children[idx + 1]

        child.keys.append(node.keys[idx])
        node.keys[idx] = sibling.keys.pop(0)

        if not child.is_leaf:
            child.children.append(sibling.children.pop(0))

    def _merge(self, node, idx):
        child = node.children[idx]
        sibling = node.children[idx + 1]

        child.keys.append(node.keys[idx])
        child.keys.extend(sibling.keys)
        if child.is_leaf:
            child.values.extend(sibling.values)
            child.next = sibling.next
        else:
            child.children.extend(sibling.children)

        node.keys.pop(idx)
        node.children.pop(idx + 1)

    def update(self, key, new_value):
        node = self.root
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]

        for i, item in enumerate(node.keys):
            if item == key:
                node.values[i] = new_value
                return True
        return False

    def get_all(self):
        result = []
        node = self.root
        # Traverse down to the leftmost leaf
        while not node.is_leaf:
            node = node.children[0]
        # Walk through the leaves and collect all key-value pairs
        while node:
            for key, value in zip(node.keys, node.values):
                result.append((key, value))
            node = node.next  # move to next leaf
        return result

    def visualize_tree(self,filename="bplustree"):
        """
        Create a visual representation of the B+ Tree using Graphviz.
        """
        dot = Digraph(format='png')  # Specify output format
        dot.attr(dpi='300') 
        self._add_nodes(dot, self.root)  # Add nodes recursively
        self._add_edges(dot, self.root)  # Add edges recursively
        dot.render(filename,format='png',cleanup=True)
        print(f"Tree visualization saved as {filename}.png")

    def _add_nodes(self, dot, node, parent_id=None):
        node_id = str(id(node))
        if node.is_leaf:
            label = "|".join(str(k) for k in node.keys)
            dot.node(node_id, label=label, shape='record', color='lightblue2', style='filled')
        else:
            label = "{" + " | ".join(f"<f{i}>{k}" for i, k in enumerate(node.keys)) + "}"
            dot.node(node_id, label=label, shape='record', color='lightgray', style='filled')
        if parent_id:
            dot.edge(parent_id, node_id)
        if not node.is_leaf:
            for child in node.children:
               self._add_nodes(dot, child, node_id)


    def _add_edges(self, dot, node):
         if not node.is_leaf:
          for child in node.children:
            self._add_edges(dot, child)

         