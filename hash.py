from tools import make_data
import random
import time

def make_table(m):
    buckets = []
    for i in range(m):
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