from tools import make_data
import time
import random

def insert(table, rec):
    table.append(rec)

def select_eq(table, key):
    for rec in table:
        if rec[0] == key:
            return rec
    return None

def select_range(table, low, high):
    lst = []
    for rec in table:
        if low <= rec[0] < high:
            lst.append(rec)
    return lst

def measure_insert(n):
    data = make_data(n)
    table = []
    start = time.perf_counter()
    for rec in data:
        insert(table, rec)
    end = time.perf_counter()
    return end-start

def measure_select_eq(n):
    table = make_data(n)
    keys = []
    for i in range(1000):
        keys.append(random.randint(0,n-1))
    start = time.perf_counter()
    for i in range(1000):
        select_eq(table, keys[i])
    end = time.perf_counter()
    return (end-start)/1000

def measure_select_range(n):
    table = make_data(n)
    keys = []
    for i in range(1000):
        keys.append(random.randint(0,n-101))
    start = time.perf_counter()
    for i in range(1000):
        select_range(table, keys[i], keys[i]+100)
    end = time.perf_counter()
    return (end-start)/1000
