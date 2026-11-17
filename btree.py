from tools import make_data
import random
import time

MAX_KEYS = 64

class Node:
    def __init__(self, is_leaf):
        # 모든 노드: B-트리는 내부 노드에도 데이터(values)가 있다
        self.keys = []
        self.values = []
        self.is_leaf = is_leaf
        # 내부 노드
        self.children = []
        # 리프 연결(next)은 없다

class BTree:
    def __init__(self):
        self.root = Node(True)

    def find_path(self, key):
        # insert용: 리프까지 내려가며 지나온 노드를 기록한다
        node = self.root
        path = []
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
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

        # 1. 넘치지 않으면 끝
        if len(leaf.keys) <= MAX_KEYS:
            return
        up_key, up_value, right = self.split(leaf)
        left = leaf

        # 2. 부모로 올리기 (넘치면 위로 반복)
        while path:
            parent = path.pop()
            j = 0
            while j < len(parent.keys) and up_key > parent.keys[j]:
                j += 1
            parent.keys.insert(j, up_key)
            parent.values.insert(j, up_value)
            parent.children.insert(j + 1, right)
            if len(parent.keys) <= MAX_KEYS:
                return
            up_key, up_value, right = self.split(parent)
            left = parent

        # 3. 루트까지 분할됨 → 새 루트
        new_root = Node(False)
        new_root.keys = [up_key]
        new_root.values = [up_value]
        new_root.children = [left, right]
        self.root = new_root

    def split(self, node):
        # 리프든 내부 노드든 규칙이 하나다: 가운데 key를 값과 함께 위로 "이동"
        mid = (len(node.keys) - 1) // 2
        up_key = node.keys[mid]
        up_value = node.values[mid]
        right = Node(node.is_leaf)
        right.keys = node.keys[mid+1:]
        right.values = node.values[mid+1:]
        node.keys = node.keys[:mid]
        node.values = node.values[:mid]
        if not node.is_leaf:
            right.children = node.children[mid+1:]
            node.children = node.children[:mid+1]
        return up_key, up_value, right

    def select_eq(self, key):
        # 내부 노드에서 찾으면 리프까지 내려가지 않고 바로 끝난다
        node = self.root
        while True:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if i < len(node.keys) and node.keys[i] == key:
                return (key, node.values[i])
            if node.is_leaf:
                return None
            node = node.children[i]

    def select_range(self, low, high):
        lst = []
        self.collect(self.root, low, high, lst)
        return lst

    def collect(self, node, low, high, lst):
        # 리프 연결이 없으므로 트리를 중위 순회(자식 → key → 자식 ...)한다
        i = 0
        while i < len(node.keys) and node.keys[i] < low:
            i += 1
        while True:
            if not node.is_leaf:
                self.collect(node.children[i], low, high, lst)
            if i == len(node.keys) or node.keys[i] >= high:
                return
            lst.append((node.keys[i], node.values[i]))
            i += 1


# 트리 생성
def build_tree(n):
    tree = BTree()
    for rec in make_data(n):
        tree.insert(rec[0], rec[1])
    return tree

# 측정 함수 3개
def measure_insert(n):
    data = make_data(n)
    tree = BTree()
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
