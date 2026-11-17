import random
import time

import linear
import hash
import btree
import bplustree

# 실험 설정: n은 고정하고 key 사이 간격(gap)만 바꾼다
N = 10**5
GAPS = [1, 10, 100, 1000]
COUNT = 100          # 범위 안에 들어가는 실제 레코드 수
REPEAT = 100         # select 반복 횟수 (gap=1000이면 해시가 오래 걸려서 100번)
HASH_M = 100003      # 해시 버킷 수: 소수라서 gap과 공약수가 없어 충돌이 몰리지 않는다


def make_sparse_data(n, gap):
    # id가 0, gap, 2*gap, ... 인 레코드 n개 (make_data와 같은 seed, shuffle)
    lst = []
    for i in range(n):
        key = i * gap
        lst.append((key, "user" + str(key)))
    random.seed(2400)
    random.shuffle(lst)
    return lst


# 자료구조마다 (만들기, 넣기, 등호 검색, 범위 검색)을 같은 모양으로 맞춘다
def linear_ops():
    return ([],
            linear.insert,
            linear.select_eq,
            linear.select_range)

def hash_ops():
    return (hash.make_table(HASH_M),
            hash.insert,
            hash.select_eq,
            hash.select_range)

def btree_ops():
    tree = btree.BTree()
    return (tree,
            lambda t, rec: t.insert(rec[0], rec[1]),
            lambda t, key: t.select_eq(key),
            lambda t, lo, hi: t.select_range(lo, hi))

def bplustree_ops():
    tree = bplustree.BPlusTree()
    return (tree,
            lambda t, rec: t.insert(rec[0], rec[1]),
            lambda t, key: t.select_eq(key),
            lambda t, lo, hi: t.select_range(lo, hi))


STRUCTURES = [
    ("Linear", linear_ops),
    ("Hash", hash_ops),
    ("B tree", btree_ops),
    ("B plus tree", bplustree_ops),
]


def measure_all(make_ops, gap):
    # 한 번 만든 구조로 insert, select_eq, select_range를 차례로 잰다
    data = make_sparse_data(N, gap)
    table, insert, select_eq, select_range = make_ops()

    start = time.perf_counter()
    for rec in data:
        insert(table, rec)
    t_insert = time.perf_counter() - start

    # 등호 검색: 실제로 있는 key만 고른다
    keys = []
    for _ in range(REPEAT):
        keys.append(random.randint(0, N - 1) * gap)
    start = time.perf_counter()
    for key in keys:
        select_eq(table, key)
    t_eq = (time.perf_counter() - start) / REPEAT

    # 범위 검색: 폭 COUNT*gap 안에는 항상 레코드가 정확히 COUNT개 있다
    width = COUNT * gap
    los = []
    for _ in range(REPEAT):
        los.append(random.randint(0, (N - COUNT) * gap))
    start = time.perf_counter()
    for lo in los:
        select_range(table, lo, lo + width)
    t_range = (time.perf_counter() - start) / REPEAT

    return t_insert, t_eq, t_range


def run(name, make_ops):
    labels = ["insert (total)", "select_eq (avg)", f"select_range {COUNT}rec"]
    results = []
    for gap in GAPS:
        results.append(measure_all(make_ops, gap))

    print()
    print(f"===== {name} (n={N:,}) =====")
    header = f"{'op':<22}" + "".join(f"{'gap=' + str(g):>14}" for g in GAPS)
    print(header)
    print("-" * 78)
    for i, label in enumerate(labels):
        row = f"{label:<22}"
        for r in results:
            row += f"{r[i]:>14.2e}"
        print(row, flush=True)


for name, make_ops in STRUCTURES:
    run(name, make_ops)
