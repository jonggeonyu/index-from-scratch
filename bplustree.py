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