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

    def find_path(self, key):
        node = self.root
        path = []
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            path.append(node)
            node = node.children[i]
        return node, path

    def insert(self, key, value):
        leaf, path = self.find_path(key)
        i = 0
        while i < len(leaf.keys) and key > leaf.keys[i]:
            i += 1
        leaf.keys.insert(i, key)
        leaf.values.insert(i, value)

    def split_leaf(self, leaf):
        mid = len(leaf.keys) // 2 
        right = Node(True)
        right.keys = leaf.keys[mid:]      
        right.values = leaf.values[mid:]
        leaf.keys = leaf.keys[:mid]        
        leaf.values = leaf.values[:mid]
        right.next = leaf.next             
        leaf.next = right                  
        up_key = right.keys[0]              
        return up_key, right

    def split_internal(self, node):
        mid = (len(node.keys) - 1) // 2     
        up_key = node.keys[mid]           
        right = Node(False)
        right.keys = node.keys[mid+1:]       
        right.children = node.children[mid+1:]
        node.keys = node.keys[:mid]          
        node.children = node.children[:mid+1]
        return up_key, right