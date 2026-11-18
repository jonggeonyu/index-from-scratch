import random
import time

import linear
import hash
import btree
import bplustree

# 실험 설정: key 사이 간격(gap)은 고정하고 n만 늘린다 (measure_time.py와 같은 n)
SIZES = [10**3, 10**4, 10**5, 10**6]
GAP = 100            # key 사이 간격 (상수). 0, 100, 200, ... 처럼 띄엄띄엄 놓인다
COUNT = 100          # 범위 안에 들어가는 실제 레코드 수
REPEAT = 100         # select 반복 횟수


def next_prime(x):
    # x 이상인 가장 작은 소수
    while True:
        d = 2
        while d * d <= x and x % d != 0:
            d += 1
        if x >= 2 and d * d > x:
            return x
        x += 1


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
def linear_ops(n):
    return ([],
            linear.insert,
            linear.select_eq,
            linear.select_range)

def hash_ops(n):
    # 버킷 수: n 이상인 소수. m = n에 가깝게 유지하면서,
    # gap과 공약수가 없어서 충돌이 한 버킷에 몰리지 않는다
    return (hash.make_table(next_prime(n)),
            hash.insert,
            hash.select_eq,
            hash.select_range)

def btree_ops(n):
    tree = btree.BTree()
    return (tree,
            lambda t, rec: t.insert(rec[0], rec[1]),
            lambda t, key: t.select_eq(key),
            lambda t, lo, hi: t.select_range(lo, hi))

def bplustree_ops(n):
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


def measure_all(make_ops, n):
    # 한 번 만든 구조로 insert, select_eq, select_range를 차례로 잰다
    data = make_sparse_data(n, GAP)
    table, insert, select_eq, select_range = make_ops(n)

    start = time.perf_counter()
    for rec in data:
        insert(table, rec)
    t_insert = time.perf_counter() - start

    # 등호 검색: 실제로 있는 key만 고른다
    keys = []
    for _ in range(REPEAT):
        keys.append(random.randint(0, n - 1) * GAP)
    start = time.perf_counter()
    for key in keys:
        select_eq(table, key)
    t_eq = (time.perf_counter() - start) / REPEAT

    # 범위 검색: 폭 COUNT*GAP 안에는 항상 레코드가 정확히 COUNT개 있다
    width = COUNT * GAP
    los = []
    for _ in range(REPEAT):
        los.append(random.randint(0, (n - COUNT) * GAP))
    start = time.perf_counter()
    for lo in los:
        select_range(table, lo, lo + width)
    t_range = (time.perf_counter() - start) / REPEAT

    return t_insert, t_eq, t_range


def run(name, make_ops):
    labels = ["insert (total)", "select_eq (avg)", f"select_range {COUNT}rec"]
    print()
    print(f"===== {name} (gap={GAP}) =====")
    header = f"{'op':<22}" + "".join(f"{'n=' + format(n, ','):>14}" for n in SIZES)
    print(header)
    print("-" * 78)
    results = []
    for n in SIZES:
        results.append(measure_all(make_ops, n))
    for i, label in enumerate(labels):
        row = f"{label:<22}"
        for r in results:
            row += f"{r[i]:>14.2e}"
        print(row, flush=True)


if __name__ == "__main__":
    for name, make_ops in STRUCTURES:
        run(name, make_ops)
