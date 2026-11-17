from tools import make_data

MAX_KEYS = 3

class Node:
    def __init__(self, is_leaf):
        # 모든 노드
        self.keys = []
        self.is_leaf = is_leaf
        # 내부 노드
        self.children = []
        # 리프 노드
        self.values = []
        self.next = None

class BPlusTree:
    def __init__(self):
        self.root = Node(True)

    def find_leaf(self, key):
        node = self.root
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
        return node
