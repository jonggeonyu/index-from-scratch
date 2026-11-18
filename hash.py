from tools import make_data
import random
import time

def make_table(m):
    buckets = []
    for _ in range(m):
        buckets.append([])
    return buckets

def insert(table, rec):
    m = len(table)
    table[rec[0]%m].append(rec)

def select_eq(table, key):
    m = len(table)
    bucket = table[key%m]
    if not bucket:
        return None
    for rec in bucket:
        if key == rec[0]:
            return rec
    return None

def select_range(table, low, high):
    m = len(table)
    lst = []
    for key in range(low, high, 1):
        for rec in table[key%m]:
            if rec[0] == key:
                lst.append(rec)
    return lst

def select_range_scan(table, low, high):
    # key 후보를 나열할 수 없을 때(문자열, 실수 등)의 방식:
    # 버킷 전체를 훑으며 범위 안인지 검사한다 → O(n)
    lst = []
    for bucket in table:
        for rec in bucket:
            if low <= rec[0] < high:
                lst.append(rec)
    return lst

def measure_insert(n):
    data = make_data(n)
    buckets = make_table(n)
    start = time.perf_counter()
    for rec in data:
        insert(buckets, rec)
    end = time.perf_counter()
    return end - start

def measure_select_eq(n):
    buckets = make_table(n)
    lst = make_data(n)
    for rec in lst:
        insert(buckets, rec)
    keys = []
    for _ in range(1000):
        keys.append(random.randint(0, n-1))
    start = time.perf_counter()
    for key in keys:
        select_eq(buckets, key)
    end = time.perf_counter()
    return (end - start) / 1000

def measure_select_range(n, width=100):
    buckets = make_table(n)
    lst = make_data(n)
    for rec in lst:
        insert(buckets, rec)
    keys = []
    for _ in range(1000):
        keys.append(random.randint(0, n-width))
    start = time.perf_counter()
    for i in range(1000):
        lst = select_range(buckets, keys[i], keys[i]+width)
    end = time.perf_counter()
    return (end - start) / 1000
