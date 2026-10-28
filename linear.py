from tools import make_data
import time

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
