from tools import make_data
import random
import time

MAX_KEYS = 64

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

        # 1. 리프가 넘치지 않으면 끝
        if len(leaf.keys) <= MAX_KEYS:
            return
        up_key, right = self.split_leaf(leaf)
        left = leaf

        # 2. 부모로 올리기 (넘치면 위로 반복)
        while path:
            parent = path.pop()
            j = 0
            while j < len(parent.keys) and up_key >= parent.keys[j]:
                j += 1
            parent.keys.insert(j, up_key)
            parent.children.insert(j + 1, right)
            if len(parent.keys) <= MAX_KEYS:
                return
            up_key, right = self.split_internal(parent)
            left = parent

        # 3. 루트까지 분할됨 → 새 루트
        new_root = Node(False)
        new_root.keys = [up_key]
        new_root.children = [left, right]
        self.root = new_root

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

    def select_eq(self, key):
        leaf, _ = self.find_path(key)
        for i in range(len(leaf.keys)):
            if leaf.keys[i] == key:
                return (key, leaf.values[i])
        return None

    def select_range(self, low, high):
        lst = []
        leaf, _ = self.find_path(low)
        while leaf:
            for i in range(len(leaf.keys)):
                if leaf.keys[i] >= high:
                    return lst
                if leaf.keys[i] >= low:
                    lst.append((leaf.keys[i], leaf.values[i]))
            leaf = leaf.next
        return lst


# 트리 생성
def build_tree(n):
    tree = BPlusTree()
    for rec in make_data(n):
        tree.insert(rec[0], rec[1])
    return tree

# 측정 함수 3개
def measure_insert(n):
    data = make_data(n)
    tree = BPlusTree()
    start = time.perf_counter()
    for rec in data:
        tree.insert(rec[0], rec[1])
    end = time.perf_counter()
    return end - start

def measure_select_eq(n):
    tree = build_tree(n)
    keys = []
    for i in range(1000):
        keys.append(random.randint(0, n-1))
    start = time.perf_counter()
    for i in range(1000):
        tree.select_eq(keys[i])
    end = time.perf_counter()
    return (end - start) / 1000

def measure_select_range(n, width):
    tree = build_tree(n)
    keys = []
    for i in range(1000):
        keys.append(random.randint(0, n-width))
    start = time.perf_counter()
    for i in range(1000):
        tree.select_range(keys[i], keys[i]+width)
    end = time.perf_counter()
    return (end - start) / 1000