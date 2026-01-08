class BTreeNode:
    def __init__(self, t, leaf = False):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.children = []

class BTree:
    def __init__(self,t):
        self.t = t
        self.root = BTreeNode(t, leaf = True)

    def search(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and node.keys[i] == key:
            return node
        
        if node.leaf:
            return None
        return self.search(node.children[i], key)
    
    def insert(self, key):
        root = self.root

        if len(root.keys) == (2 * self.t) - 1:
            new_root = BTreeNode(self.t, leaf = False)
            new_root.children.append(root)
            self.split_child(new_root, 0)
            self.root = new_root

        self.insert_non_full(self.root, key)

    def insert_non_full(self, node, key):
        i = len(node.keys) - 1

        if node.leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1

            if len(node.children[i].keys) == (2 * self.t) - 1:
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1

            self.insert_non_full(node.children[i], key)

    def split_child(self, parent, i):
        t = self.t
        full_child = parent.children[i]
        new_child = BTreeNode(t, leaf= full_child.leaf)

        parent.keys.insert(i, full_child.keys[t - 1])
        parent.children.insert(i + 1, new_child)

        new_child.keys = full_child.keys[t:]
        full_child.keys = full_child.keys[:t-1]

        if not full_child.leaf:
            new_child.children = full_child.children[t:]
            full_child.children = full_child.children[:t]
    def traverse(self, node):
        for i in range(len(node.keys)):
            if not node.leaf:
                self.traverse(node.children[i])
            print(node.keys[i], end= " ")
        if not node.leaf:
            self.traverse(node.children[-1])

btree = BTree(t=3)
values = [10,20,5,6,12,30,7,17]
for v in values:
    btree.insert(v)

btree.traverse(btree.root)
print()

print(btree.search(btree.root, 12) is not None)  
print(btree.search(btree.root, 99) is not None)