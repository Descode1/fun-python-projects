class BPlusNode:
    def __init__(self, t, leaf= False):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.children = []
        self.next = None

class BPlusTree:
    def __init__(self, t):
        self.t = t
        self.root = BPlusNode(t, leaf=True)

    def search(self, key):
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]

        for i, k in enumerate(node.keys):
            if k == key:
                return node.children[i]
        return None
    
    def insert(self, key, value):
        root = self.root

        if len(root.keys) == (2 * self.t) - 1:
            new_root = BPlusNode(self.t)
            new_root.children.append(root)
            self.split_child(new_root, 0)
            self.root = new_root

        self.insert_non_full(self.root, key, value)
    
    def insert_non_full(self, node, key, value):
        if node.leaf:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1

            node.keys.insert(i, key)
            node.children.insert(i, value)
        else:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1

            if len(node.children[i].keys) == (2 * self.t) - 1:
                self.split_child(node, i)
                if key >= node.keys[i]:
                    i += 1

            self.insert_non_full(node.children[i], key, value)
        
    def split_child(self, parent, index):
        t = self.t 
        node = parent.children[index]
        new_node = BPlusNode(t, leaf=node.leaf)
        if node.leaf:
            new_node.keys = node.keys[t:]
            new_node.children = node.children[t:]
            node.keys = node.keys[:t]
            node.children = node.children[:t]

            new_node.next = node.next
            node.next = new_node

            parent.keys.insert(index, new_node.keys[0])
            parent.children.insert(index + 1, new_node)
        else:
            parent.keys.insert(index, node.keys[t - 1])
            new_node.keys = node.keys[t:]
            new_node.children = node.children[t:]
            node.keys = node.keys[:t - 1]
            node.children = node.children[:t]
            parent.children.insert(index + 1, new_node)

    def range_search(self, start, end):
        results = []
        node = self.root
        while not node.leaf:
            i = 0 
            while i < len(node.keys) and start >= node.keys[i]:
                i += 1
            node = node.children[i]
        while node:
            for i, key in enumerate(node.keys):
                if start <= key <= end:
                    results.append((key, node.children[i]))
                elif key > end:
                    return results
            node = node.next
        return results
        

tree = BPlusTree(t =3)
data = [10,20,5,6,12,30,7,17]
for x in data: 
    tree.insert(x, f"value-{x}")

print(tree.search(12))
print(tree.search(99))

print(tree.range_search(6,20))